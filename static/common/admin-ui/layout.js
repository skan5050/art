/* Раскладки админки по макетам: меню сайта, рубрики, карточка картины, вкладки разделов (D). Формы и сохранение — штатные. */
(function () {
  "use strict";
  var ready = function (fn) { if (document.readyState !== "loading") fn(); else document.addEventListener("DOMContentLoaded", fn); };
  var body = function () { return document.body; };
  var has = function (cls) { return body().classList.contains(cls); };
  var el = function (tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text) e.textContent = text; return e; };

  /* Вкладки разделов под верхней полосой (макет D) */
  function tabs() {
    if ((getComputedStyle(document.documentElement).getPropertyValue("--pl-tabs") || "").trim() !== "1") return;
    var anchor = document.querySelector('a[href*="catalog/painting/"]');
    var main = document.querySelector("#main");
    if (!anchor || !main || document.querySelector(".pl-tabs")) return;
    var base = anchor.getAttribute("href").split("catalog/painting/")[0];
    var items = [["Обзор", base, /^$/], ["Картины", base + "catalog/painting/", /catalog\/painting/], ["Рубрики", base + "catalog/category/", /catalog\/category/],
      ["Меню", base + "content/menuitem/", /content\/menuitem/], ["Города", base + "geo/city/map/", /geo\/city/], ["Отзывы", base + "content/review/", /content\/review/],
      ["Заявки", base + "leads/lead/", /leads\/lead/], ["Настройки", base + "core/sitesettings/", /core\/sitesettings/]];
    var rest = location.pathname.indexOf(base) === 0 ? location.pathname.slice(base.length) : "";
    var nav = el("nav", "pl-tabs");
    nav.setAttribute("aria-label", "Разделы");
    items.forEach(function (it) {
      var a = el("a", "", it[0]);
      a.href = it[1];
      var on = it[0] === "Обзор" ? rest === "" : it[2].test(rest);
      if (on) { a.className = "is-current"; a.setAttribute("aria-current", "page"); }
      nav.appendChild(a);
    });
    var header = main.firstElementChild;
    header.insertAdjacentElement("afterend", nav);
  }

  /* Меню сайта: перетаскивание строк и живой предпросмотр */
  function menuEditor() {
    var form = document.querySelector("[data-menu-editor]");
    if (!form) return;
    var list = form.querySelector("[data-menu-rows]");
    var preview = form.querySelector("[data-menu-preview]");
    var dragging = null;
    function render() {
      preview.textContent = "";
      list.querySelectorAll("[data-row]").forEach(function (row) {
        var vis = row.querySelector("[data-menu-visible]").checked;
        var del = row.querySelector("[data-menu-delete]").checked;
        row.classList.toggle("is-off", !vis);
        row.classList.toggle("is-deleted", del);
        if (!vis || del) return;
        var input = row.querySelector("[data-menu-label]");
        var span = el("span", "", input.value.trim() || input.placeholder);
        preview.appendChild(span);
      });
    }
    list.addEventListener("dragstart", function (e) {
      var row = e.target.closest && e.target.closest("[data-row]");
      if (!row || e.target.closest("input")) { e.preventDefault(); return; }
      dragging = row; row.classList.add("is-drag");
      e.dataTransfer.effectAllowed = "move";
      try { e.dataTransfer.setData("text/plain", ""); } catch (x) { /* Firefox */ }
    });
    list.addEventListener("dragover", function (e) {
      if (!dragging) return;
      e.preventDefault();
      var over = e.target.closest("[data-row]");
      if (!over || over === dragging) return;
      var r = over.getBoundingClientRect();
      list.insertBefore(dragging, e.clientY < r.top + r.height / 2 ? over : over.nextSibling);
    });
    list.addEventListener("dragend", function () { if (dragging) dragging.classList.remove("is-drag"); dragging = null; render(); });
    form.addEventListener("input", render);
    form.addEventListener("change", render);
    render();
  }

  /* Рубрики: дерево слева, свойства справа */
  function categoryLayout() {
    var tree = document.querySelector("[data-cat-tree]");
    var f = document.querySelector("#category_form");
    if (!tree || !f || tree.parentElement.classList.contains("pl-split")) return;
    var split = el("div", "pl-split");
    f.parentNode.insertBefore(split, tree);
    split.appendChild(tree);
    var right = el("div", "pl-split-main");
    split.appendChild(right);
    right.appendChild(f);
  }

  /* Картина: фото слева, поля справа */
  function paintingLayout() {
    var f = document.querySelector("#painting_form");
    var meta = document.querySelector("[data-painting-meta]");
    if (!f || f.classList.contains("pl-painting")) return;
    var inner = f.querySelector(":scope > div.flex");
    if (!inner) return;
    f.classList.add("pl-painting");
    var photos = inner.querySelector("#images-group");
    var side = el("aside", "pl-photos");
    var frame = el("div", "pl-photo-frame");
    var url = meta ? meta.getAttribute("data-photo") : "";
    if (url) { var img = el("img"); img.src = url; img.alt = ""; frame.appendChild(img); } else { frame.appendChild(el("span", "", "Фото не добавлено")); }
    side.appendChild(frame);
    side.appendChild(el("p", "pl-cap", "Основное фото"));
    var add = el("button", "pl-btn pl-btn-ghost", "+ Добавить фото");
    add.type = "button";
    add.addEventListener("click", function () {
      var link = photos && photos.querySelector(".add-row a, a.add-row, [class*='add-row'] a, button.add-row");
      if (link) link.click();
      if (photos) photos.scrollIntoView({ behavior: "smooth", block: "center" });
    });
    side.appendChild(add);
    side.appendChild(el("p", "pl-note", "Изображение показывается целиком. Порядок фото меняется в списке ниже."));
    if (photos) side.appendChild(photos);
    var fields = el("div", "pl-fields");
    var sets = [];
    inner.querySelectorAll(":scope > fieldset, :scope > .aligned").forEach(function (n) { sets.push(n); });
    sets.forEach(function (n) { fields.appendChild(n); });
    var grid = el("div", "pl-painting-grid");
    grid.appendChild(side);
    grid.appendChild(fields);
    inner.insertBefore(grid, inner.firstChild);
    var preview = meta && meta.getAttribute("data-preview");
    if (preview) {
      var pv = el("a", "pl-btn pl-btn-ghost", "Предпросмотр");
      pv.href = preview; pv.target = "_blank"; pv.rel = "noopener";
      fields.appendChild(pv);
    }
  }

  ready(function () {
    tabs();
    menuEditor();
    if (has("model-category") && has("change-form")) categoryLayout();
    if (has("model-painting") && has("change-form")) paintingLayout();
  });
})();
