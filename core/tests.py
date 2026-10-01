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
        self.assertIn(q("/отзывы/"), xml)  # есть стартовые отзывы
        from content.models import Review

        Review.objects.all().delete()
        self.assertNotIn(q("/отзывы/"), self.client.get("/sitemap.xml").content.decode())  # пустой раздел отзывов не попадает в карту
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
        self.assertEqual(abroad.count(), 20)  # 10 ближнего зарубежья + 10 городов Китая
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

    def test_city_landing_pages_and_address_map(self):
        from content.models import CityLanding
        from geo.models import City

        call_command("import_cities", stdout=io.StringIO())
        Page.objects.get_or_create(kind="cities", defaults={"title_ru": "Города", "title_en": "Cities", "slug_ru": "города",
                                                           "slug_en": "cities", "published": True})
        kazan = City.objects.get(name_ru="Казань")
        landing = CityLanding.objects.create(city=kazan, name_ru="Казань", name_en="Kazan", name_in_ru="в Казани",
                                             title_ru="Картины в Казани", title_en="Paintings in Kazan",
                                             body_ru="Свой текст о Казани.", delivery_ru="Отправляем в Казань через СДЭК.",
                                             published=True)
        self.assertEqual(landing.url("ru"), "/города/казань/")
        r = self.client.get(quote(landing.url("ru")))
        self.assertContains(r, "Картины в Казани")
        self.assertContains(r, "СДЭК")
        self.assertNotContains(r, "yandex.ru/map-widget")  # без адреса карты нет
        self.assertEqual(self.client.get(landing.url("en")).status_code, 200)
        self.assertIn(quote(landing.url("ru")), self.client.get("/sitemap.xml").content.decode())
        # адрес и координаты → карта с точкой (координаты через точку, не по локали)
        landing.address_ru, landing.address_lat, landing.address_lng = "ул. Баумана, 1", Decimal("55.790000"), Decimal("49.120000")
        landing.save()
        r = self.client.get(quote(landing.url("ru")))
        self.assertContains(r, "yandex.ru/map-widget")
        self.assertContains(r, "49.120000%2C55.790000")
        # ссылка на страницу города в данных карты продаж (отметка — только у подтверждённой продажи)
        kazan.sale_confirmed = kazan.visible = True
        kazan.save()
        r = self.client.get(quote(Page.objects.get(kind="delivery").url("ru")))
        self.assertContains(r, "\\u0433\\u043e\\u0440\\u043e\\u0434\\u0430")  # «города» в JSON-ссылке
        # черновик недоступен посетителю
        landing.published = False
        landing.save()
        self.assertEqual(self.client.get(quote(landing.url("ru"))).status_code, 404)
        # карта с адресом на странице контактов
        s = SiteSettings.get()
        s.address_ru, s.address_lat, s.address_lng = "Москва, ул. Пример, 1", Decimal("55.75"), Decimal("37.61")
        s.save()
        self.assertContains(self.client.get(quote(Page.objects.get(kind="contacts").url("ru"))), "yandex.ru/map-widget")

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


@override_settings(MEDIA_ROOT=TMP + "/media-map", PRIVATE_MEDIA_ROOT=TMP + "/private-map", ALLOWED_HOSTS=["testserver"])
class ContentMapTests(TestCase):
    """ТЗ 1.3, приложение Е: карта наполнения, заголовки статей, временное меню, IndexNow, фавикон."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_site", site="a", verbosity=0, stdout=io.StringIO())

    def page(self, kind):
        return Page.objects.get(kind=kind)

    def test_images_follow_content_map_without_baked_text(self):
        from content.models import StudioImage

        home = self.page("home")
        self.assertTrue(home.banner_image.name.endswith("mirame_home_hero_desktop.jpg"))  # утверждённый hero A
        self.assertTrue(home.banner_image_mobile.name.endswith("mirame_home_hero_mobile.jpg"))
        self.assertTrue(self.page("about").image.name.endswith("mirame_about_studio.jpg"))
        self.assertTrue(self.page("custom").image.name.endswith("mirame_custom_order.jpg"))
        self.assertTrue(self.page("delivery").image.name.endswith("mirame_delivery.jpg"))
        self.assertTrue(SiteSettings.get().certificate_image.name.endswith("mirame_gift_certificate.jpg"))
        self.assertFalse(StudioImage.objects.exists())  # у МираМе отдельной галереи мастерской нет
        covers = {"картина-в-интерьере": "mirame_article_01_interer", "готовая-или-на-заказ": "mirame_article_02_gotovaya_ili_zakaz",
                  "как-заказать-картину": "mirame_article_03_kak_zakazat"}
        for slug, name in covers.items():
            article = Article.objects.get(slug_ru=slug)
            self.assertIn(name, article.cover.name)
            self.assertTrue(article.cover_alt_ru and article.cover_alt_en)
            width, height = Image.open(article.cover.path).size
            self.assertAlmostEqual(width / height, 16 / 9, delta=0.02)
        self.assertEqual(list(Category.objects.filter(cover="").values_list("slug_ru", flat=True)), [])  # v5: у всех рубрик есть обложка из комплекта
        # главный hero грузится приоритетно и без alt-набивки; у обложек рубрик подпись — текст HTML
        html = self.client.get("/").content.decode()
        self.assertIn('fetchpriority="high"', html)
        self.assertIn("mirame_category_", html)
        self.assertTrue(all(page.t.image_alt for page in (self.page("about"), self.page("custom"), self.page("delivery"))))

    def test_delivery_image_sits_inside_article_block(self):
        html = self.client.get(q(self.page("delivery").url("ru"))).content.decode()
        self.assertIn('class="text-page delivery-article has-aside"', html)
        self.assertIn('class="text-aside"', html)
        self.assertIn("mirame_delivery", html)

    def test_about_has_single_figure_and_footer_has_no_extra_links(self):
        about = self.client.get(q("/о-нас/")).content.decode()
        self.assertNotIn("studio-grid", about)
        self.assertEqual(about.count('class="about-media"'), 1)
        home = self.client.get("/").content.decode()
        self.assertNotIn("Все контакты", home)
        # пустая колонка контактов не выводится
        self.assertNotIn("footer-contacts", home)

    def test_article_headings_and_internal_links(self):
        import re

        import seed.a.articles as a
        import seed.d.articles as d

        expected = {
            "картина-в-интерьере": "Как выбрать картину для интерьера — и не спрашивать разрешения у дивана",
            "готовая-или-на-заказ": "Готовая картина или картина на заказ: что выбрать?",
            "как-заказать-картину": "Как заказать картину, если пока не знаете, какую хотите",
        }
        for slug, title in expected.items():
            article = Article.objects.get(slug_ru=slug)
            self.assertEqual(article.title_ru, title)
            html = self.client.get(q(article.url("ru"))).content.decode()
            self.assertEqual(html.count("<h1"), 1)
            self.assertIn(f">{title}</h1>", html)
        d_titles = {art["slug_ru"]: art["title_ru"] for art in d.ARTICLES[:3]}
        self.assertEqual(d_titles["картина-в-интерьере"], "Как выбрать картину для интерьера: пространство, формат и композиция")
        self.assertEqual(d_titles["что-подготовить-для-заказа"], "Какие сведения подготовить для заказа картины: сюжет, размер и срок")
        # 2–4 внутренние ссылки по смыслу в каждой из трех статей обоих сайтов, RU и EN
        for module in (a, d):
            for art in module.ARTICLES[:3]:
                for lang in ("ru", "en"):
                    links = re.findall(r"\]\((/[^)]*)\)", art[f"body_{lang}"])
                    self.assertTrue(2 <= len(links) <= 4, (art["slug_ru"], lang, links))
                    if lang == "en":
                        self.assertTrue(all(link.startswith("/en/") for link in links), links)

    def test_article_jsonld_and_open_graph(self):
        article = Article.objects.get(slug_ru="картина-в-интерьере")
        html = self.client.get(q(article.url("ru"))).content.decode()
        self.assertIn('"@type": "Article"', html)
        self.assertIn('"author": {"@type": "Organization"', html)
        for key in ('"headline"', '"image"', '"datePublished"', '"dateModified"'):
            self.assertIn(key, html)
        self.assertIn('property="og:image" content="http', html)
        self.assertIn("mirame_article_01_interer", html)
        self.assertIn('"@type": "BreadcrumbList"', html)
        self.assertIn('"@type": "Organization"', self.client.get("/").content.decode())

    def test_temporary_guides_menu_item_can_be_hidden(self):
        from content.models import MenuItem

        item = MenuItem.objects.get(page__kind="guides")
        self.assertTrue(item.visible)
        self.assertEqual(item.label_ru, "Полезные статьи")
        self.assertFalse(item.in_footer)  # в футере ссылка «Полезное» уже есть
        html = self.client.get("/").content.decode()
        self.assertEqual(html.count("Полезные статьи"), 1)
        guides = self.page("guides")
        r = self.client.get(q(guides.url("ru")))
        self.assertContains(r, "Как выбрать картину для интерьера")
        item.visible = False
        item.save()
        self.assertNotIn("Полезные статьи", self.client.get("/").content.decode())
        self.assertEqual(self.client.get(q(guides.url("ru"))).status_code, 200)  # страницы и адреса не меняются

    def test_public_map_has_no_service_labels(self):
        import re

        html = self.client.get(q(self.page("delivery").url("ru"))).content.decode()
        visible = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", html, flags=re.S).lower()
        self.assertIsNone(re.search(r"\b(debug|demo|test)\b|демо|тестов|координат", visible))
        self.assertIn("leaflet", html.lower())  # атрибуция провайдера карты сохраняется

    def test_brand_favicon_is_served(self):
        r = self.client.get("/favicon.ico")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r["Content-Type"], "image/x-icon")
        html = self.client.get("/").content.decode()
        self.assertIn("favicon.svg", html)
        self.assertIn("apple-touch-icon", html)

    def test_indexnow_is_off_by_default_and_sends_on_publish_and_delete(self):
        from unittest import mock

        from core import indexnow

        sent = []

        class Inline:
            def __init__(self, target, args=(), daemon=None):
                self.target, self.args = target, args

            def start(self):
                self.target(*self.args)

        settings = SiteSettings.get()
        self.assertFalse(settings.indexnow_enabled)
        with mock.patch.object(indexnow, "send", side_effect=sent.append), mock.patch.object(indexnow.threading, "Thread", Inline):
            with self.captureOnCommitCallbacks(execute=True):
                Article.objects.create(slug_ru="проверка-indexnow-0", slug_en="indexnow-check-0", title_ru="Проверка", title_en="Check", published=True)
            self.assertEqual(sent, [])  # выключено — ничего не уходит
            settings.base_url = "https://mirame.example"
            settings.indexnow_enabled = True
            settings.clean()
            settings.save()
            key = SiteSettings.get().indexnow_key
            self.assertRegex(key, r"^[0-9a-f]{32}$")
            r = self.client.get(f"/{key}.txt")
            self.assertEqual((r.status_code, r.content.decode()), (200, key))
            self.assertEqual(self.client.get("/" + "a" * 32 + ".txt").status_code, 404)
            indexnow._recent.clear()
            with self.captureOnCommitCallbacks(execute=True):
                art = Article.objects.create(slug_ru="проверка-indexnow", slug_en="indexnow-check", title_ru="Проверка", title_en="Check", published=True)
            self.assertEqual(len(sent), 1)
            data = sent[0]
            self.assertEqual((data["host"], data["key"], data["keyLocation"]), ("mirame.example", key, f"https://mirame.example/{key}.txt"))
            self.assertIn("https://mirame.example" + art.url("ru"), data["urlList"])
            self.assertIn("https://mirame.example" + art.url("en"), data["urlList"])
            # черновик не отправляется
            indexnow._recent.clear()
            with self.captureOnCommitCallbacks(execute=True):
                Article.objects.create(slug_ru="черновик-indexnow", slug_en="indexnow-draft", title_ru="Черновик", title_en="Draft", published=False)
            self.assertEqual(len(sent), 1)
            # удаление тоже сообщается
            indexnow._recent.clear()
            path = art.url("ru")
            with self.captureOnCommitCallbacks(execute=True):
                art.delete()
            self.assertEqual(len(sent), 2)
            self.assertIn("https://mirame.example" + path, sent[1]["urlList"])

    def test_indexnow_requires_site_address(self):
        from django.core.exceptions import ValidationError

        settings = SiteSettings.get()
        settings.indexnow_enabled = True
        settings.base_url = ""
        with self.assertRaises(ValidationError):
            settings.clean()


class ApprovedPackageTests(TestCase):
    def test_six_article_covers_are_distinct_and_16_9(self):
        import hashlib
        from pathlib import Path as P

        import seed.a.articles as a
        import seed.d.articles as d

        seen = set()
        for mod, site in ((a, "a"), (d, "d")):
            for art in mod.ARTICLES[:3]:
                path = P("seed") / site / "media" / art["cover"]
                self.assertTrue(path.exists(), path)
                self.assertEqual(Image.open(path).size, (1600, 900))
                digest = hashlib.md5(path.read_bytes()).hexdigest()
                self.assertNotIn(digest, seen)  # ни одна обложка не повторяется
                seen.add(digest)
        self.assertEqual(len(seen), 6)


class TypicalCityPagesTests(TestCase):
    def test_typical_city_pages_use_correct_case_forms(self):
        from content.models import CityLanding

        call_command("seed_site", verbosity=0)
        self.assertEqual(CityLanding.objects.count(), 38)  # 18 авторских + 20 типовых (города России от 500 тыс.)
        cases = {
            "Набережные Челны": ("в Набережных Челнах", "в Набережные Челны", "Набережных Челнов"),
            "Махачкала": ("в Махачкале", "в Махачкалу", "Махачкалы"),
            "Владивосток": ("во Владивостоке", "во Владивосток", "Владивостока"),
            "Кемерово": ("в Кемерове", "в Кемерово", "Кемерова"),
            "Тольятти": ("в Тольятти", "в Тольятти", "Тольятти"),
        }
        for name, (prep, acc, gen) in cases.items():
            page = CityLanding.objects.get(name_ru=name)
            self.assertEqual(page.title_ru, f"Картины {prep}")
            self.assertEqual(page.name_in_ru, prep)
            self.assertIn(acc, page.delivery_ru)
            self.assertIn(acc, page.body_ru)
            self.assertIn(gen, page.body_ru)
            r = self.client.get(page.path_ru)
            self.assertEqual(r.status_code, 200)
            self.assertContains(r, f"Картины {prep}")
        # все города России от 500 тыс., кроме Севастополя, имеют страницы
        from geo.models import City

        names = set(CityLanding.objects.values_list("name_ru", flat=True))
        big = set(City.objects.filter(country_code="RU", population__gte=500_000).values_list("name_ru", flat=True))
        big |= {"Тольятти", "Ижевск", "Барнаул", "Махачкала", "Иркутск", "Хабаровск", "Ульяновск", "Владивосток", "Ярославль", "Оренбург", "Томск",
                "Кемерово", "Набережные Челны", "Новокузнецк", "Рязань", "Астрахань", "Пенза", "Липецк", "Балашиха", "Киров"}
        self.assertTrue(big <= names, big - names)


class StarterReviewsTests(TestCase):
    def test_starter_reviews_are_seeded_per_site(self):
        from content.models import Review

        call_command("seed_site", verbosity=0)
        reviews = list(Review.objects.order_by("order"))
        self.assertEqual(len(reviews), 10)
        self.assertTrue(all(r.published and r.photo and r.text_en and r.city_ru for r in reviews))
        call_command("seed_site", verbosity=0)  # повторный запуск не плодит дубли
        self.assertEqual(Review.objects.count(), 10)
        self.assertTrue(all(r.date and r.date.year >= 2023 for r in reviews))
        html = self.client.get(q("/отзывы/")).content.decode()
        self.assertIn(reviews[0].text_ru[:30], html)
        self.assertIn("review-photo" if "review-photo" in html else "review-featured", html)


class AdminLayoutTests(TestCase):
    """Рабочие экраны админки по макетам: меню, рубрики, города, карточка картины."""

    def setUp(self):
        from django.contrib.auth.models import User

        self.client.force_login(User.objects.create_superuser("boss2", "b2@example.com", "x"))

    def test_menu_editor_saves_order_visibility_and_delete(self):
        from content.models import MenuItem

        call_command("seed_site", verbosity=0)
        items = list(MenuItem.objects.order_by("order", "id"))
        self.assertGreaterEqual(len(items), 3)
        r = self.client.get("/admin/content/menuitem/")
        self.assertContains(r, "data-menu-editor")
        self.assertContains(self.client.get("/admin/content/menuitem/?table=1"), "action-select")  # прежняя таблица доступна
        first, second, third = items[:3]
        data = {"menu_editor": "1", "row": [second.pk, first.pk, third.pk], f"visible_{second.pk}": "on", f"label_ru_{second.pk}": "Новая надпись",
                f"delete_{third.pk}": "on"}
        self.assertEqual(self.client.post("/admin/content/menuitem/", data).status_code, 302)
        second.refresh_from_db(), first.refresh_from_db()
        self.assertEqual((second.order, first.order), (0, 10))
        self.assertEqual(second.label_ru, "Новая надпись")
        self.assertTrue(second.visible)
        self.assertFalse(first.visible)  # флажок снят — пункт скрыт
        self.assertFalse(MenuItem.objects.filter(pk=third.pk).exists())

    def test_menu_flags_and_footer_flag_are_preserved(self):
        from content.models import MenuItem

        call_command("seed_site", verbosity=0)
        item = MenuItem.objects.filter(in_footer=True).first()
        before = (item.in_footer, item.label_en)
        data = {"menu_editor": "1", "row": [item.pk], f"visible_{item.pk}": "on", f"footer_present_{item.pk}": "1", f"footer_{item.pk}": "on",
                "flags": "1", "menu_in_header": "on"}  # «Повторять в подвале» снят
        self.client.post("/admin/content/menuitem/", data)
        item.refresh_from_db()
        self.assertEqual((item.in_footer, item.label_en), before)  # скрытые поля строки не потеряны
        settings_obj = SiteSettings.get()
        self.assertTrue(settings_obj.menu_in_header)
        self.assertFalse(settings_obj.menu_in_footer)
        self.assertFalse(any(m for m in self.client.get("/").context["footer_menu"]))

    def test_category_tree_layout_and_table_fallback(self):
        call_command("seed_site", verbosity=0)
        cat = Category.objects.filter(parent=None).order_by("order").first()
        r = self.client.get("/admin/catalog/category/")
        self.assertEqual(r.status_code, 302)
        self.assertIn(f"/{cat.pk}/change/", r["Location"])
        page = self.client.get(r["Location"])
        self.assertContains(page, "data-cat-tree")
        self.assertContains(page, cat.name_ru)
        self.assertEqual(self.client.get("/admin/catalog/category/?table=1").status_code, 200)
        self.assertContains(self.client.get("/admin/catalog/category/add/"), "data-cat-tree")

    def test_city_map_screen_saves_marks(self):
        from geo.models import City

        city = City.objects.create(name_ru="Тестоград", name_en="Testgrad", country_code="RU", country_ru="Россия", country_en="Russia",
                                   latitude=Decimal("55.75"), longitude=Decimal("37.61"), sale_confirmed=False, visible=True)
        self.assertNotIn(f'"id": {city.pk},', self.client.get("/admin/geo/city/map/").content.decode())
        found = self.client.get("/admin/geo/city/map/search/?q=тестог").json()["results"]
        self.assertEqual(found[0]["id"], city.pk)
        self.assertIsInstance(found[0]["lat"], float)
        data = {"row": [city.pk], f"on_{city.pk}": "1", f"visible_{city.pk}": "1", f"caption_ru_{city.pk}": "Картины в Тестограде"}
        self.assertEqual(self.client.post("/admin/geo/city/map/", data).status_code, 302)
        city.refresh_from_db()
        self.assertTrue(city.sale_confirmed)
        self.assertEqual(city.caption_ru, "Картины в Тестограде")
        self.assertIn(f'"id": {city.pk},', self.client.get("/admin/geo/city/map/").content.decode())
        self.assertEqual(self.client.get("/admin/geo/city/").status_code, 200)  # справочник остался

    def test_painting_form_renders_with_meta(self):
        call_command("seed_site", verbosity=0)
        painting = Painting.objects.create(title_ru="Форма", category=Category.objects.first(), status=Painting.AVAILABLE)
        r = self.client.get(f"/admin/catalog/painting/{painting.pk}/change/")
        self.assertContains(r, "data-painting-meta")
        self.assertContains(r, "Фото, состояние, рубрика, цена и описание")


class ChineseVersionTests(TestCase):
    """Китайская версия: аддитивный слой /zh/, прежние RU/EN-страницы не меняются."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_site", verbosity=0)

    def test_zh_pages_are_chinese_and_have_switcher(self):
        import re

        r = self.client.get("/zh/")
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        self.assertIn('<html lang="zh"', html)
        self.assertRegex(re.search(r"<h1[^>]*>([^<]*)", html).group(1), r"[一-鿿]")
        self.assertIn('hreflang="ru"', html)
        self.assertIn("English", html)

    def test_ru_and_en_link_to_zh(self):
        for path in ("/", "/en/"):
            html = self.client.get(path).content.decode()
            self.assertIn('hreflang="zh"', html)
            self.assertIn("/zh/", html)

    def test_articles_translated_and_cities_listed(self):
        from content.models import Article
        from core.zh import zh_has

        articles = list(Article.objects.filter(published=True))
        self.assertGreaterEqual(len(articles), 1)
        self.assertTrue(all(zh_has(a) and a.url("zh").startswith("/zh/") for a in articles))
        self.assertEqual(self.client.get(articles[0].url("zh")).status_code, 200)
        self.assertEqual(self.client.get("/zh/cities/").status_code, 200)

    def test_sitemap_and_labels(self):
        sm = self.client.get("/sitemap.xml").content.decode()
        self.assertIn("/zh/china/", sm)
        self.assertIn('hreflang="zh"', sm)
        from core.labels_zh import LABELS_ZH

        self.assertGreater(len(LABELS_ZH), 150)

    def test_china_landing(self):
        import re

        from core.models import Translation
        from geo.models import City

        city = City.objects.create(country_code="CN", country_ru="Китай", name_ru="Пекин", latitude=39.9, longitude=116.4,
                                   sale_confirmed=True, visible=True)
        Translation.objects.create(target=f"geo.city:{city.pk}", field="name", text="北京")
        r = self.client.get("/zh/china/")
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        self.assertRegex(re.search(r"<h1[^>]*>([^<]*)", html).group(1), r"[\u4e00-\u9fff]")
        self.assertEqual(html.count("data-geo-city"), 1)
        self.assertIn("北京", html)
        self.assertIn('rel="canonical" href="http://testserver/zh/china/"', html)
        self.assertNotIn("/zh/china/", self.client.get("/").content.decode().replace("hreflang", ""))  # RU-страницы не ссылаются на лэндинг

    def test_untranslated_zh_page_is_404(self):
        self.assertEqual(self.client.get("/zh/no-such-page/").status_code, 404)

    def test_language_hint_script_only_on_ru_en(self):
        self.assertIn("lang-hint.js", self.client.get("/").content.decode())
        self.assertIn("lang-hint.js", self.client.get("/en/").content.decode())
        self.assertNotIn("lang-hint.js", self.client.get("/zh/").content.decode())


class CityGeoTests(TestCase):
    """Автоопределение города РФ: только RU, только активный лендинг, без редиректов и догадок."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_site", verbosity=0)
        from content.models import CityLanding

        cls.landing = CityLanding.objects.filter(published=True).first()
        assert cls.landing is not None

    def geo(self, country="RU", city=None, ua="Mozilla/5.0", **extra):
        headers = {"HTTP_X_GEO_COUNTRY": country, "HTTP_X_GEO_CITY": city if city is not None else self.landing.name_ru, "HTTP_USER_AGENT": ua}
        return self.client.get("/geo/city/", **headers, **extra)

    def test_off_by_default(self):
        self.assertEqual(self.geo().json(), {})

    def test_ru_city_with_active_landing(self):
        with override_settings(GEO_PROVIDER="headers"):
            data = self.geo().json()
            self.assertEqual(data["name"], self.landing.name_ru)
            self.assertEqual(data["url"], self.landing.url("ru"))
            self.assertNotIn("sale", data)
            self.assertEqual(self.geo().headers["Cache-Control"], "private, no-store")

    def test_other_country_unknown_city_bot_do_nothing(self):
        with override_settings(GEO_PROVIDER="headers"):
            self.assertEqual(self.geo(country="DE").json(), {})
            self.assertEqual(self.geo(city="").json(), {})
            self.assertEqual(self.geo(city="Бердск").json(), {})  # лендинга нет — ничего не предлагаем и не создаём
            self.assertEqual(self.geo(ua="Mozilla/5.0 (compatible; YandexBot/3.0)").json(), {})

    def test_english_name_and_explicit_alias(self):
        with override_settings(GEO_PROVIDER="headers"):
            self.assertEqual(self.geo(city=self.landing.name_en)["Content-Type"].split(";")[0], "application/json")
            self.assertTrue(self.geo(city=self.landing.name_en).json())
            self.assertEqual(self.geo(city="Neizvestny").json(), {})
            self.landing.geo_aliases = "Alias Town"
            self.landing.save()
            self.assertTrue(self.geo(city="alias town").json())

    def test_cloudflare_provider_headers(self):
        with override_settings(GEO_PROVIDER="cloudflare"):
            r = self.client.get("/geo/city/", HTTP_CF_IPCOUNTRY="RU", HTTP_CF_IPCITY=self.landing.name_en or self.landing.name_ru)
            self.assertTrue(r.json())

    def test_landing_has_config_and_no_redirect(self):
        r = self.client.get(self.landing.url("ru"), HTTP_X_GEO_COUNTRY="RU", HTTP_X_GEO_CITY="Другой")
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        self.assertIn('id="city-geo"', html)
        self.assertIn("city-geo.js", html)
        self.assertNotIn("city-geo.js", self.client.get("/").content.decode())
        en = self.landing.url("en")
        if en:
            self.assertNotIn("city-geo.js", self.client.get(en).content.decode())

    def test_picker_lists_only_flagged_active(self):
        from core import geo_detect

        total = len(geo_detect.picker_items())
        self.landing.show_in_picker = False
        self.landing.save()
        self.assertEqual(len(geo_detect.picker_items()), total - 1)

    def test_provider_is_replaceable(self):
        from core import geo_detect

        for name, cls in (("cloudflare", geo_detect.CloudflareProvider), ("headers", geo_detect.CustomHeadersProvider), ("sypex", geo_detect.SypexProvider)):
            with override_settings(GEO_PROVIDER=name):
                self.assertIsInstance(geo_detect.get_provider(), cls)
        with override_settings(GEO_PROVIDER="sypex"):  # файл базы ещё не подключён — сайт работает, предложений нет
            self.assertEqual(self.geo().json(), {})
        with override_settings(GEO_PROVIDER=""):
            self.assertIsNone(geo_detect.get_provider())

    def test_city_form_script_only_on_ru_pages(self):
        self.assertIn("city-form.js", self.client.get("/").content.decode())
        self.assertNotIn("city-form.js", self.client.get("/en/").content.decode())
        self.assertNotIn("city-form.js", self.client.get("/zh/").content.decode())
