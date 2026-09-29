"""Проверки по критериям приемки ТЗ (разделы 13.x) и дополнения SEO 1.3."""
import io
import json
import shutil
import tempfile
from decimal import Decimal
from urllib.parse import quote

from django.core.management import call_command
from django.test import TestCase, override_settings
from PIL import Image

from catalog.models import Category, Painting, PaintingSize
from content.models import Article, Page
from core.models import Redirect, SiteSettings, StandardSize
from importapi.models import ApiKey, ImportLog, ImportRecord
from leads.models import Lead

TMP = tempfile.mkdtemp(prefix="art-test-")


def q(path):
    return quote(path)


def png_bytes(size=(40, 30), fmt="PNG"):
    buf = io.BytesIO()
    Image.new("RGB", size, (30, 80, 140)).save(buf, fmt)
    return buf.getvalue()


@override_settings(MEDIA_ROOT=TMP + "/media", PRIVATE_MEDIA_ROOT=TMP + "/private", ALLOWED_HOSTS=["testserver"])
class SiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_site", site="a", verbosity=0, stdout=io.StringIO())
        cls.sea = Category.objects.get(slug_ru="море")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TMP, ignore_errors=True)

    def painting(self, **kw):
        data = {"title_ru": "Тихий залив", "title_en": "Quiet bay", "category": self.sea, "published": True}
        data.update(kw)
        p = Painting(**data)
        p.full_clean()
        p.save()
        return p

    # --- Адреса, языки, SEO ---
    def test_cyrillic_urls_and_en_prefix(self):
        about = Page.objects.get(kind="about")
        self.assertEqual(about.path_ru, "/о-нас/")
        self.assertEqual(about.path_en, "/en/about/")
        self.assertEqual(self.client.get(q("/о-нас/")).status_code, 200)
        self.assertEqual(self.client.get("/en/about/").status_code, 200)
        child = Category.objects.get(slug_ru="дети")
        self.assertEqual(child.path_ru, "/каталог/портрет-и-фигура/дети/")

    def test_hreflang_and_self_canonical(self):
        html = self.client.get(q("/о-нас/")).content.decode()
        self.assertIn('hreflang="en" href="http://testserver/en/about/"', html)
        self.assertIn('<link rel="canonical" href="http://testserver/%D0%BE-%D0%BD%D0%B0%D1%81/">', html)
        en = self.client.get("/en/about/").content.decode()
        self.assertIn('<link rel="canonical" href="http://testserver/en/about/">', en)

    def test_title_uses_brand_prefix_and_updates_with_brand(self):
        html = self.client.get(q("/о-нас/")).content.decode()
        self.assertIn("<title>МираМе | О нас</title>", html)
        s = SiteSettings.get()
        s.brand_name_ru = "НовоеИмя"
        s.save()
        html = self.client.get(q("/о-нас/")).content.decode()
        self.assertIn("<title>НовоеИмя | О нас</title>", html)

    def test_domain_setting_applies_everywhere(self):
        s = SiteSettings.get()
        s.base_url = "https://example-art.ru"
        s.save()
        html = self.client.get(q("/о-нас/")).content.decode()
        self.assertIn('href="https://example-art.ru/en/about/"', html)
        self.assertIn("Sitemap: https://example-art.ru/sitemap.xml", self.client.get("/robots.txt").content.decode())
        self.assertIn("<loc>https://example-art.ru/</loc>", self.client.get("/sitemap.xml").content.decode())

    def test_slug_change_creates_301_without_chains(self):
        about = Page.objects.get(kind="about")
        about.slug_ru = "о-мастерской"
        about.save()
        about.slug_ru = "кто-мы"
        about.save()
        r = self.client.get(q("/о-нас/"))
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r["Location"], q("/кто-мы/"))
        self.assertEqual(Redirect.objects.get(old_path="/о-мастерской/").new_path, "/кто-мы/")

    def test_category_rename_redirects_children_and_deleted_page_404(self):
        parent = Category.objects.get(slug_ru="портрет-и-фигура")
        parent.slug_ru = "портреты"
        parent.save()
        r = self.client.get(q("/каталог/портрет-и-фигура/дети/"))
        self.assertEqual(r["Location"], q("/каталог/портреты/дети/"))
        article = Article.objects.first()
        path = article.path_ru
        article.delete()
        self.assertEqual(self.client.get(q(path)).status_code, 404)

    def test_sitemap_follows_publication_and_excludes_empty(self):
        xml = self.client.get("/sitemap.xml").content.decode()
        self.assertNotIn(q("/каталог/море/"), xml)  # пустая рубрика
        self.assertNotIn(q("/отзывы/"), xml)  # пустой раздел отзывов
        p = self.painting()
        xml = self.client.get("/sitemap.xml").content.decode()
        self.assertIn(q(p.path_ru), xml)
        self.assertIn(q("/каталог/море/"), xml)
        p.published = False
        p.save()
        self.assertNotIn(q(p.path_ru), self.client.get("/sitemap.xml").content.decode())

    def test_empty_category_is_noindex(self):
        html = self.client.get(q("/каталог/море/")).content.decode()
        self.assertIn('content="noindex, follow"', html)

    def test_robots_disallow_all_needs_confirmation(self):
        from django.core.exceptions import ValidationError

        s = SiteSettings.get()
        s.robots_txt = "User-agent: *\nDisallow: /\n"
        with self.assertRaises(ValidationError):
            s.full_clean()

    def test_pagination_urls_and_self_canonical(self):
        for i in range(30):
            self.painting(title_ru=f"Работа {i}", title_en=f"Work {i}")
        r = self.client.get(q("/каталог/море/") + "?page=2")
        html = r.content.decode()
        self.assertEqual(r.status_code, 200)
        self.assertIn('?page=2">', html.split('rel="canonical"')[1][:200])
        self.assertIn("страница 2", html)
        self.assertEqual(self.client.get(q("/каталог/море/") + "?page=5").status_code, 404)
        self.assertEqual(self.client.get(q("/каталог/море/") + "?page=1").status_code, 301)
        more = self.client.get(q("/каталог/море/") + "?page=2", HTTP_X_REQUESTED_WITH="fetch").json()
        self.assertIn("art-card", more["html"])

    def test_no_fake_price_in_jsonld(self):
        p = self.painting(status=Painting.AVAILABLE)
        html = self.client.get(q(p.path_ru)).content.decode()
        self.assertNotIn('"price"', html)
        self.assertIn("Стоимость по запросу", html)

    # --- Каталог и картины ---
    def test_category_cannot_be_own_descendant(self):
        from django.core.exceptions import ValidationError

        parent = Category.objects.get(slug_ru="животные-и-птицы")
        child = Category.objects.get(slug_ru="птицы")
        parent.parent = child
        with self.assertRaises(ValidationError):
            parent.full_clean()

    def test_sold_keeps_url_and_appears_in_sold(self):
        p = self.painting(status=Painting.AVAILABLE)
        url = p.path_ru
        p.status = Painting.SOLD
        p.save()
        self.assertEqual(p.path_ru, url)
        r = self.client.get(q(url))
        self.assertEqual(r.status_code, 200)
        self.assertIn("Заказать похожую", r.content.decode())
        self.assertIn(q(url), self.client.get(q("/проданные-картины/")).content.decode().replace(url, q(url)))

    def test_common_description_does_not_overwrite_individual(self):
        from core.models import SharedBlock

        own = self.painting(description_mode=Painting.DESC_OWN, description_ru="Свой текст")
        shared = self.painting(title_ru="Другая", title_en="Other")
        block = SharedBlock.objects.get(key="painting-description")
        block.text_ru = "Новый общий текст"
        block.save()
        self.assertEqual(own.description("ru"), "Свой текст")
        self.assertEqual(shared.description("ru"), "Новый общий текст")

    def test_sizes_inherit_common_list_and_custom_list_is_independent(self):
        self.assertEqual(StandardSize.objects.count(), 20)
        inherited = self.painting(status=Painting.CUSTOM)
        own = self.painting(title_ru="Своя", title_en="Own", status=Painting.CUSTOM, sizes_mode=Painting.SIZES_OWN)
        PaintingSize.objects.create(painting=own, width=Decimal("45"), height=Decimal("65"))
        StandardSize.objects.filter(width=20, height=30).update(visible=False)
        self.assertEqual(len(inherited.desired_sizes()), 19)
        self.assertEqual([o["label"] for o in own.desired_sizes()], ["45 × 65"])

    # --- Заявки ---
    def lead_post(self, **extra):
        data = {"name": "Анна", "contact_method": "phone", "contact": "+7 999 000-11-22", "lang": "ru", "consent": "1"}
        data.update(extra)
        data = {k: v for k, v in data.items() if v is not None}
        return self.client.post("/lead/", data, HTTP_X_REQUESTED_WITH="fetch")

    def test_import_cities_enables_regional_centers_and_major_cities(self):
        from geo.major_cities import MAJOR_CITIES, THRESHOLD
        from geo.models import City

        call_command("import_cities", stdout=io.StringIO())
        shown = City.objects.filter(sale_confirmed=True, visible=True)
        abroad = shown.exclude(country_code="RU")
        self.assertEqual(abroad.count(), 10)
        self.assertTrue(all(c.population > THRESHOLD for c in abroad))
        # все центры субъектов РФ из справочника, включая добавленные вручную
        self.assertEqual(shown.filter(country_code="RU").count(), City.objects.filter(country_code="RU", is_admin_center=True).count())
        self.assertTrue(shown.filter(name_ru="Гатчина").exists() and shown.filter(name_ru="Анадырь").exists())
        self.assertTrue(set(MAJOR_CITIES) <= set(shown.values_list("source_id", flat=True)))
        krasnodar = shown.get(name_ru="Краснодар")
        self.assertIn("Росстат", krasnodar.population_date)
        # Ручная правка владельца не перезаписывается
        krasnodar.visible, krasnodar.manually_edited = False, True
        krasnodar.save()
        call_command("map_major_cities", stdout=io.StringIO())
        self.assertFalse(City.objects.get(pk=krasnodar.pk).visible)
        r = self.client.get(Page.objects.get(kind="delivery").url("ru"))
        self.assertContains(r, "Тюмень")
        self.assertContains(r, "Ташкент")

    def test_admin_dashboard_and_robots_validation(self):
        from django.contrib.auth.models import User

        from core.admin import robots_problems
        from core.models import ROBOTS_DEFAULT

        user = User.objects.create_superuser("boss", "boss@example.com", "x")
        self.client.force_login(user)
        self.lead_post(idempotency_key="dash")
        r = self.client.get("/admin/")
        self.assertContains(r, "Сегодня в мастерской")
        self.assertContains(r, "Анна")  # последняя заявка на рабочем экране
        self.assertContains(r, "Готовность сайта")
        self.assertEqual(robots_problems(ROBOTS_DEFAULT), [])
        problems = robots_problems("Disallow: /x\nUser-agent *\nFoo: bar")
        self.assertEqual(len(problems), 4)  # до User-agent, без двоеточия, неизвестная директива, нет User-agent
        settings_obj = SiteSettings.get()
        r = self.client.get(f"/admin/core/sitesettings/{settings_obj.pk}/change/")
        self.assertEqual(r.status_code, 200)

    def test_audit_content_reports_missing_translation(self):
        from core.models import Label

        Label.objects.create(key="audit.test", group="Тест", value_ru="Только по-русски", value_en="")
        out = io.StringIO()
        call_command("audit_content", stdout=out)
        self.assertIn("audit.test", out.getvalue())
        self.assertIn("нет версии EN", out.getvalue())
        self.assertIn("Проверено страниц:", out.getvalue())

    def test_lead_requires_consent_when_enabled(self):
        s = SiteSettings.get()
        s.consent_checkbox = True
        s.save()
        r = self.lead_post(consent=None, idempotency_key="c1")
        self.assertEqual(r.status_code, 400)
        self.assertIn("consent", r.json()["errors"])
        r = self.lead_post(idempotency_key="c2")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(Lead.objects.get().consent_given)

    def test_lead_context_from_server_and_size_saved(self):
        p = self.painting(status=Painting.SOLD)
        size = StandardSize.objects.get(width=40, height=60)
        r = self.lead_post(kind="painting", painting_id=p.pk, size_choice="standard", size_id=f"s{size.pk}",
                           size_orientation="horizontal", idempotency_key="k1")
        self.assertEqual(r.status_code, 200, r.content)
        lead = Lead.objects.get()
        self.assertEqual(lead.kind, "similar")  # статус определяет сервер
        self.assertEqual((lead.size_width, lead.size_height), (Decimal("60.0"), Decimal("40.0")))
        size.width, size.height = 50, 70
        size.save()
        lead.refresh_from_db()
        self.assertEqual(lead.size_width, Decimal("60.0"))

    def test_lead_idempotent_and_requires_one_contact(self):
        self.assertEqual(self.lead_post(idempotency_key="same").status_code, 200)
        self.assertEqual(self.lead_post(idempotency_key="same").status_code, 200)
        self.assertEqual(Lead.objects.count(), 1)
        r = self.lead_post(contact="", idempotency_key="x2")
        self.assertEqual(r.status_code, 400)
        self.assertIn("contact", r.json()["errors"])

    def test_lead_rejects_fake_image_and_bad_custom_size(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        fake = SimpleUploadedFile("x.jpg", b"<html>not an image</html>", content_type="image/jpeg")
        r = self.lead_post(file=fake, idempotency_key="f1")
        self.assertEqual(r.status_code, 400)
        r = self.lead_post(size_choice="custom", size_width="-5", size_height="abc", idempotency_key="f2")
        self.assertIn("size_custom", r.json()["errors"])
        ok = SimpleUploadedFile("room.png", png_bytes(), content_type="image/png")
        self.assertEqual(self.lead_post(file=ok, size_choice="custom", size_width="45,5", size_height="65", idempotency_key="f3").status_code, 200)
        lead = Lead.objects.get()
        self.assertEqual(lead.attachments.count(), 1)
        self.assertEqual(lead.size_width, Decimal("45.5"))

    # --- API импорта ---
    def api(self, method, path, token, **kw):
        return getattr(self.client, method)(path, HTTP_AUTHORIZATION=f"Bearer {token}", secure=True, **kw)

    def test_api_upload_idempotent_and_scoped(self):
        key, token = ApiKey.issue("Тест")
        self.assertNotIn(token.split("_", 2)[2], key.secret_hash)
        cats = self.api("get", "/api/v1/import/categories", token).json()["categories"]
        self.assertTrue(any(c["id"] == self.sea.pk for c in cats))
        from django.core.files.uploadedfile import SimpleUploadedFile

        def upload(ext_id, content, cat=self.sea.pk, purpose="photo"):
            f = SimpleUploadedFile("a.png", content, content_type="image/png")
            return self.api("post", "/api/v1/import/images", token,
                            data={"external_id": ext_id, "category_id": cat, "purpose": purpose, "file": f})

        r = upload("IMG-1", png_bytes())
        self.assertEqual(r.status_code, 201, r.content)
        self.assertEqual(upload("IMG-1", png_bytes()).json()["duplicate"], True)
        self.assertEqual(ImportRecord.objects.count(), 1)
        self.assertEqual(upload("IMG-1", png_bytes((50, 50))).status_code, 409)
        self.assertEqual(upload("IMG-2", png_bytes(), cat=999999).status_code, 404)
        self.assertEqual(upload("IMG-3", b"GIF89a....").status_code, 415)
        self.assertEqual(upload("IMG-4", png_bytes(), purpose="cover").status_code, 403)
        self.assertFalse(Painting.objects.exists())  # без права карточек не создаются
        self.assertEqual(self.api("get", "/api/v1/import/results/IMG-1", token).json()["state"], "accepted")
        key.revoke()
        self.assertEqual(self.api("get", "/api/v1/import/categories", token).status_code, 401)
        self.assertFalse(ImportLog.objects.filter(message__contains=token).exists())

    def test_api_rejects_other_site_or_garbage_token(self):
        self.assertEqual(self.api("get", "/api/v1/import/categories", "imp_deadbeef_xxx").status_code, 401)
        self.assertEqual(self.client.get("/api/v1/import/categories", secure=True).status_code, 401)
