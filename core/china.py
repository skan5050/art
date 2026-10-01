"""Отдельный китайский лэндинг «Картины из России для Китая» (/zh/china/).

Только китайская версия: страницы на RU/EN не затрагиваются. Тексты — по тону сайта
(A — тёплый, D — деловой) и в рамках действующих условий доставки: CDEK или другой
перевозчик по согласованию, стоимость доставки отдельно, сроки и формальности уточняются.
"""
from django.conf import settings as dj_settings
from django.http import Http404
from django.shortcuts import render

from content.views import _map_cities
from core.i18n import current_lang
from core.models import SiteSettings
from core.seo import build_meta, organization_jsonld

PATH = "/zh/china/"

CONTENT = {
    "a": {
        "kicker": "致中国的朋友",
        "title": "来自俄罗斯的画作，寄往中国的家",
        "intro": "画不需要签证，但需要合适的包装和商量好的路线。我们把现成的画作和按您想法创作的作品，寄给中国的朋友。",
        "seo_title": "寄往中国的俄罗斯画作：现货与定制",
        "seo_description": "现货与定制画作，可商定发往中国城市。我们一起确认路线、承运人、包装与运费。",
        "sections": [
            ("为什么选择我们的画作", "色彩、质感和一点点温暖：风景、抽象、动物与鸟类，以及按您的构想创作的作品。目录里是现成的作品，也可以先聊聊您想在墙上看到什么。"),
            ("如何订购", "1. 在目录中选择画作，或描述您的想法。\n2. 告诉我们收货的城市，我们一起确认路线与承运人。\n3. 确认包装、费用和付款方式。\n4. 画作准备好后交给运输公司。"),
            ("关于配送", "我们通过 CDEK 或与您商定的运输公司发货。运费不含在画作价格内，由客户另行支付，金额取决于路线、打包后作品的参数和承运商的条件。前往中国的路线是否可行、需要哪些手续和大致时间，会在发货前单独确认——我们不会承诺大画瞬间传送。"),
            ("语言没有问题", "您可以用中文留言，写下城市、喜欢的题材和期望的尺寸。我们会尽快回复，并陪您把细节一一商量清楚。"),
        ],
        "map_title": "中国的这些城市，已经有我们画作的故事",
        "map_text": "这些城市和我们有一段小小的共同故事。每一个标记，都是一幅作品找到主人的地方。",
        "cta_text": "告诉我们您的城市和想要的画作",
        "cta_button": "洽谈订单",
    },
    "d": {
        "kicker": "中国方向",
        "title": "面向中国的画作供应：现货与定制",
        "intro": "向中国城市发送现有作品及定制画作。承运人、路线和费用在发货前与客户逐项商定。",
        "seo_title": "向中国发送画作：条件与流程",
        "seo_description": "现货与定制画作发往中国城市：商定承运人、包装、运费与手续，费用与画作价格分开。",
        "sections": [
            ("作品范围", "目录中的现货作品，以及按客户要求制作的定制作品。每件作品的材质、尺寸和装裱信息在作品页面列出。"),
            ("流程", "1. 选择作品，或提交定制需求。\n2. 提供收货城市，确认路线与承运人。\n3. 商定包装、费用和付款方式。\n4. 作品移交承运人。"),
            ("配送条件", "通过 CDEK 或经客户同意的其他运输公司发货。运费由客户另行支付，不包含在画作价格之内，依据路线、打包后作品的尺寸和重量及承运人条件确定。对于发往中国的方向，所选路线的可行性、所需手续和时间另行确认。不适用于所有方向的统一固定运价。"),
            ("沟通语言", "可使用中文提交申请。请注明收货城市、作品或题材，以及预计的尺寸，以便确定运输方案。"),
        ],
        "map_title": "销售地图：中国城市",
        "map_text": "地图显示已确认的销售记录，而不是配送范围。地图上没有您的城市，并不妨碍就配送提出咨询。",
        "cta_text": "咨询配送至中国城市",
        "cta_button": "商定配送",
    },
}


def china_view(request):
    if dj_settings.SITE_THEME not in CONTENT:
        raise Http404
    lang = current_lang()
    content = CONTENT[dj_settings.SITE_THEME]
    settings = SiteSettings.get()

    from content.models import Page

    delivery = Page.objects.filter(kind="delivery", published=True).first()
    home = Page.objects.filter(kind="home").first()
    request.switch_urls = {"ru": delivery.url("ru") if delivery else "/", "en": delivery.url("en") if delivery and delivery.has_lang("en") else "/en/"}
    request.alternate_urls = {}
    crumbs = [{"label": "首页", "href": home.url(lang) if home else "/zh/"}, {"label": content["kicker"], "href": PATH}]
    meta = build_meta(request, None, h1=content["title"], fallback_description=content["seo_description"], breadcrumbs=crumbs,
                      jsonld_extra=organization_jsonld(request))
    meta["title"] = f"{settings.brand(lang)} | {content['seo_title']}"
    meta["description"] = content["seo_description"]
    meta["canonical"] = settings.absolute(PATH, request)
    meta["og"].update({"title": content["seo_title"], "description": content["seo_description"], "url": meta["canonical"]})
    cities = [c for c in _map_cities("zh") if c["code"] == "CN"]
    return render(request, "pages/china.html", {
        "c": content, "crumbs": crumbs, "meta": meta, "cities": cities, "page": delivery,
        "geo_attribution": 'Cities: <a href="https://www.geonames.org/">GeoNames</a> (CC BY 4.0)',
    })
