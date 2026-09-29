"""Безопасное оформление текстов из админки и формирование адресов."""
import re
import unicodedata

from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.text import slugify

_SLUG_RE = re.compile(r"^[^\W_]+(?:-[^\W_]+)*$", re.UNICODE)


def make_slug(value, lang="ru"):
    """ЧПУ: для RU — кириллица, для EN — латиница (раздел 2 дополнения SEO)."""
    value = unicodedata.normalize("NFKC", str(value or "")).strip().lower()
    if lang == "en":
        return slugify(value)[:120].strip("-")
    value = value.replace("ё", "е")
    value = re.sub(r"[^\w\s-]", " ", value, flags=re.UNICODE).replace("_", " ")
    value = re.sub(r"[\s-]+", "-", value).strip("-")
    return value[:120].strip("-")


def is_valid_slug(value):
    return bool(value) and bool(_SLUG_RE.match(value)) and value == value.lower()


def render_brand(text, brand):
    """Подстановка поля бренда {brand} — ссылка на «Общие настройки → Бренд»."""
    return (text or "").replace("{brand}", brand or "")


_INLINE_BOLD = re.compile(r"\*\*(.+?)\*\*")
_INLINE_LINK = re.compile(r"\[([^\]]+)\]\(((?:/|https?://)[^\s)]+)\)")


def _inline(text):
    text = escape(text)
    text = _INLINE_BOLD.sub(r"<strong>\1</strong>", text)
    text = _INLINE_LINK.sub(r'<a href="\2">\1</a>', text)
    return text


def rich_text(source, brand=""):
    """Простая разметка без выполняемого кода.

    Абзацы разделяются пустой строкой. «## Заголовок» — подзаголовок,
    строки «- пункт» — список, **жирный**, [текст](/адрес/) — ссылка.
    Любой HTML экранируется.
    """
    source = render_brand(source, brand).replace("\r\n", "\n").strip()
    if not source:
        return ""
    html = []
    for block in re.split(r"\n\s*\n", source):
        lines = [line.rstrip() for line in block.strip().split("\n") if line.strip()]
        if not lines:
            continue
        if len(lines) == 1 and lines[0].startswith("### "):
            html.append(f"<h3>{_inline(lines[0][4:].strip())}</h3>")
        elif len(lines) == 1 and lines[0].startswith("## "):
            html.append(f"<h2>{_inline(lines[0][3:].strip())}</h2>")
        elif all(line.lstrip().startswith(("- ", "• ")) for line in lines):
            items = "".join(f"<li>{_inline(line.lstrip()[2:].strip())}</li>" for line in lines)
            html.append(f"<ul>{items}</ul>")
        else:
            if lines[0].startswith("## "):
                html.append(f"<h2>{_inline(lines[0][3:].strip())}</h2>")
                lines = lines[1:]
            if lines:
                html.append("<p>" + "<br>".join(_inline(line) for line in lines) + "</p>")
    return mark_safe("\n".join(html))


def plain_text(source, brand="", limit=None):
    """Текст без разметки — для description и анонсов."""
    text = render_brand(source, brand)
    text = _INLINE_LINK.sub(r"\1", text)
    text = text.replace("**", "")
    text = re.sub(r"^#+\s*", "", text, flags=re.M)
    text = re.sub(r"^[-•]\s+", "", text, flags=re.M)
    text = re.sub(r"\s+", " ", text).strip()
    if limit and len(text) > limit:
        cut = text[:limit].rsplit(" ", 1)[0].rstrip(",;:—-")
        text = cut + "…"
    return text
