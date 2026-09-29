from django import template
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

from core.i18n import current_lang, tr
from core.images import dimensions, thumbnail_url
from core.labels_runtime import label
from core.models import SharedBlock, SiteSettings
from core.text import plain_text, render_brand, rich_text

register = template.Library()


@register.simple_tag
def t(key):
    """Надпись интерфейса из админки: {% t "btn.order" %}."""
    return label(key)


@register.simple_tag
def shared(key):
    """Сквозной блок: {% shared "delivery-short" as block %}."""
    block = SharedBlock.objects.filter(key=key, visible=True).first()
    return block


@register.filter
def tr_field(obj, field):
    return tr(obj, field) if obj is not None else ""


@register.filter
def rich(value):
    return rich_text(value, SiteSettings.get().brand(current_lang()))


@register.filter
def brandify(value):
    return render_brand(value, SiteSettings.get().brand(current_lang()))


@register.filter
def plain(value, limit=None):
    return plain_text(value, SiteSettings.get().brand(current_lang()), int(limit) if limit else None)


@register.filter
def sizes_json(options):
    import json

    return json.dumps([
        {"id": o["id"], "label": o["label"], "square": o["square"]} for o in (options or [])
    ], ensure_ascii=False)


@register.filter
def pairs(text):
    """Строки «Заголовок | текст» → список пар для блоков шагов и преимуществ."""
    result = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        head, _, tail = line.partition("|")
        result.append({"title": head.strip(), "text": tail.strip()})
    return result


@register.simple_tag
def status_label(painting):
    return label(f"status.{painting.status}")


@register.simple_tag
def picture(image, widths="480,960", sizes="100vw", alt="", cls="", lazy=True, style="", fetchpriority=""):
    """Адаптивное изображение без обрезки: srcset из уменьшенных версий."""
    if not image:
        return ""
    dims = dimensions(image)
    widths = [int(w) for w in str(widths).split(",") if w.strip()]
    sources = []
    for w in widths:
        if dims and w > dims[0] and sources:
            break
        url = thumbnail_url(image, w)
        if url:
            sources.append((url, min(w, dims[0]) if dims else w))
    if not sources:
        return ""
    src = sources[-1][0] if len(sources) == 1 else sources[min(1, len(sources) - 1)][0]
    srcset = ", ".join(f"{url} {w}w" for url, w in sources)
    attrs = {
        "src": src,
        "srcset": srcset,
        "sizes": sizes,
        "alt": alt or "",
        "decoding": "async",
    }
    if dims:
        attrs["width"], attrs["height"] = dims
    if cls:
        attrs["class"] = cls
    if style:
        attrs["style"] = style
    if lazy and lazy != "False":
        attrs["loading"] = "lazy"
    if fetchpriority:
        attrs["fetchpriority"] = fetchpriority
    return format_html("<img {}>", format_html_join(" ", '{}="{}"', attrs.items()))


@register.simple_tag
def img_url(image, width=1600):
    return thumbnail_url(image, int(width)) if image else ""


@register.simple_tag(takes_context=True)
def page_url(context, kind):
    page = context.get("site_pages", {}).get(kind)
    return page.url() if page else ""


@register.simple_tag
def icon(name, cls="icon"):
    """Встроенные SVG-значки (декоративные, aria-hidden)."""
    paths = ICONS.get(name)
    if not paths:
        return ""
    return mark_safe(
        f'<svg class="{cls}" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false">{paths}</svg>'
    )


ICONS = {
    "mail": '<path fill="none" stroke="currentColor" stroke-width="1.6" d="M3 6h18v12H3z"/><path fill="none" stroke="currentColor" stroke-width="1.6" d="m3 7 9 6 9-6"/>',
    "chat": '<path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" d="M4 5h16v11H9l-5 4z"/>',
    "gift": '<path fill="none" stroke="currentColor" stroke-width="1.6" d="M4 10h16v10H4zM3 7h18v3H3zM12 7v13M12 7c-1.5-3-5-3.5-5-1.2C7 7 9 7 12 7zm0 0c1.5-3 5-3.5 5-1.2C17 7 15 7 12 7z"/>',
    "menu": '<path stroke="currentColor" stroke-width="1.8" stroke-linecap="round" d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path stroke="currentColor" stroke-width="1.8" stroke-linecap="round" d="m6 6 12 12M18 6 6 18"/>',
    "arrow": '<path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" d="M4 12h15m-5-5 5 5-5 5"/>',
    "telegram": '<path fill="currentColor" d="M21.4 4.3 2.9 11.4c-1.2.5-1.2 1.2-.2 1.5l4.7 1.5 1.8 5.6c.2.6.4.8.8.8.4 0 .6-.2.9-.5l2.3-2.2 4.7 3.5c.9.5 1.5.2 1.7-.8l3.1-14.6c.3-1.3-.5-1.9-1.3-1.5zM8.9 14l8.9-5.6c.4-.3.8-.1.5.2l-7.3 6.6-.3 3.2z"/>',
    "whatsapp": '<path fill="currentColor" d="M12 2.2A9.8 9.8 0 0 0 3.6 17l-1.4 4.8 5-1.3A9.8 9.8 0 1 0 12 2.2zm0 17.8c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.1 8.1 0 1 1 12 20zm4.5-6c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1-.7-.3-2-1-2.9-2.6-.2-.4.2-.4.6-1.2.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/>',
    "max": '<path fill="currentColor" d="M12 2.5a9.5 9.5 0 0 0-8.1 14.4L3 21l4.3-1a9.5 9.5 0 1 0 4.7-17.5zm-3 13V8.5h1.6l1.4 2.6 1.4-2.6H15v7h-1.5v-4.4L12 13.8l-1.5-2.7v4.4z"/>',
    "vk": '<path fill="currentColor" d="M12.8 17.5c-5.6 0-8.8-3.9-9-10.3h2.8c.1 4.7 2.2 6.7 3.8 7.1V7.2h2.6v4.1c1.6-.2 3.3-2 3.9-4.1h2.6c-.4 2.5-2.3 4.3-3.6 5.1 1.3.6 3.5 2.3 4.3 5.2h-2.9c-.6-1.9-2.1-3.4-4.3-3.6v3.6z"/>',
    "viber": '<path fill="currentColor" d="M12 2C7 2 3.5 3.6 3.5 10c0 3.4 1 5.6 3 6.8V21l3-2.6c.8.1 1.6.2 2.5.2 5 0 8.5-1.6 8.5-8.6S17 2 12 2zm3.8 12.4c-.4.6-1.3 1-2 .8-2.6-.8-4.6-2.7-5.6-5.3-.2-.7.2-1.6.8-2 .3-.2.7-.2 1 .1l1 1.4c.2.3.2.7-.1 1l-.4.4c.5 1.2 1.4 2.1 2.6 2.6l.4-.4c.3-.3.7-.3 1-.1l1.4 1c.2.1.2.4-.1.5z"/>',
    "email": '<path fill="none" stroke="currentColor" stroke-width="1.6" d="M3 6h18v12H3z"/><path fill="none" stroke="currentColor" stroke-width="1.6" d="m3 7 9 6 9-6"/>',
    "phone": '<path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" d="M6.5 3h3l1.5 4.5-2 1.5a11 11 0 0 0 6 6l1.5-2 4.5 1.5v3a2 2 0 0 1-2 2A16.5 16.5 0 0 1 4.5 5a2 2 0 0 1 2-2z"/>',
    "search": '<circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path stroke="currentColor" stroke-width="1.6" stroke-linecap="round" d="m16 16 4.5 4.5"/>',
    "zoom": '<circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path stroke="currentColor" stroke-width="1.6" stroke-linecap="round" d="m16 16 4.5 4.5M11 8v6M8 11h6"/>',
}
