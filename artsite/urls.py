from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from core import views as core_views
from importapi import views as api_views
from leads import views as lead_views

admin.site.site_header = "Управление сайтом"
admin.site.site_title = "Админка"
admin.site.index_title = "Сегодня в мастерской"

from core.china import china_view  # noqa: E402

urlpatterns = [
    path(settings.ADMIN_PATH + "private/<path:path>", core_views.private_file, name="private-file"),
    path(settings.ADMIN_PATH, admin.site.urls),
    path("robots.txt", core_views.robots_txt, name="robots"),
    path("sitemap.xml", core_views.sitemap_xml, name="sitemap"),
    path("favicon.ico", core_views.favicon_ico, name="favicon"),
    re_path(r"^(?P<key>[A-Za-z0-9-]{8,64})\.txt$", core_views.indexnow_key, name="indexnow-key"),
    path("zh/china/", china_view, name="china"),
    path("lead/", lead_views.submit, name="lead-submit"),
    path("api/v1/import/categories", api_views.categories, name="api-categories"),
    path("api/v1/import/images", api_views.upload_image, name="api-upload"),
    path("api/v1/import/results/<path:external_id>", api_views.result, name="api-result"),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
    re_path(r"^(?P<path>.*)$", core_views.dispatch, name="dispatch"),
]

handler404 = "core.views.not_found"
