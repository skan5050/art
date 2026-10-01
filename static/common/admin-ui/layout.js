/* Раскладки админки по макетам: меню сайта, рубрики, карточка картины, вкладки разделов (D). Формы и сохранение — штатные. */
(function () {
  "use strict";
  /* D: боковое меню по умолчанию свернуто (макет — вкладки); открывается кнопкой в шапке */
  try {
    if ((getComputedStyle(document.documentElement).getPropertyValue("--pl-tabs") || "").trim() === "1" && localStorage.getItem("sidebarDesktopOpen") === null) {
      localStorage.setItem("sidebarDesktopOpen", "0");
    }
  } catch (e) { /* хранилище недоступно */ }
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
    var addUrl = (tree.querySelector(".pl-btn-ghost") || {}).href || "#";
    var page = el("div", "pl-page pl-cats");
    var head = el("header", "pl-head");
    var hd = el("div");
    hd.appendChild(el("h1", "pl-title", "Рубрики каталога"));
    hd.appendChild(el("p", "pl-lede", "Вложенность, порядок, обложки и описания редактируются здесь."));
    head.appendChild(hd);
    var addTop = el("a", "pl-btn pl-btn-accent pl-add-top", "Добавить рубрику →");
    addTop.href = addUrl;
    head.appendChild(addTop);
    f.parentNode.insertBefore(page, tree);
    page.appendChild(head);
    var split = el("div", "pl-split");
    page.appendChild(split);
    split.appendChild(tree);
    var right = el("div", "pl-split-main");
    split.appendChild(right);
    var nameInput = f.querySelector("#id_name_ru");
    var h2 = el("h2", "pl-h2", nameInput && nameInput.value ? nameInput.value : "Новая рубрика");
    if (nameInput) nameInput.addEventListener("input", function () { h2.textContent = nameInput.value || "Новая рубрика"; });
    right.appendChild(h2);
    right.appendChild(f);
    var inner = f.querySelector(":scope > div.flex");
    if (inner) {
      var sets = inner.querySelectorAll(":scope > fieldset");
      if (sets.length >= 3) {
        var grid = el("div", "pl-cat-grid");
        inner.insertBefore(grid, sets[0]);
        [sets[0], sets[1], sets[2]].forEach(function (n, i) { n.classList.add("pl-cat-" + i); grid.appendChild(n); });
        var coverFile = sets[1].querySelector('input[type="file"]');
        if (coverFile) {
          var pick = el("button", "pl-btn pl-btn-ghost", "Выбрать фото");
          pick.type = "button";
          pick.addEventListener("click", function () { coverFile.click(); });
          sets[1].appendChild(pick);
        }
      }
      var actions = el("div", "pl-bottom-actions pl-cat-actions");
      var save = el("button", "pl-btn pl-btn-main", "Сохранить рубрику");
      save.type = "button";
      save.addEventListener("click", function () {
        var btn = document.querySelector('input[name="_continue"], button[name="_continue"]') || document.querySelector('input[name="_save"], button[name="_save"]');
        if (btn) btn.click(); else f.requestSubmit();
      });
      actions.appendChild(save);
      inner.appendChild(actions);
    }
  }

  var cssVar = function (name) { return (getComputedStyle(document.documentElement).getPropertyValue(name) || "").trim(); };

  /* Картина: фото слева, поля справа */
  function paintingLayout() {
    var f = document.querySelector("#painting_form");
    var meta = document.querySelector("[data-painting-meta]");
    if (!f || f.classList.contains("pl-painting")) return;
    var inner = f.querySelector(":scope > div.flex");
    if (!inner) return;
    f.classList.add("pl-painting");
    var modeD = cssVar("--pl-photo-mode") === "d";
    var photos = inner.querySelector("#images-group");
    var preview = meta && meta.getAttribute("data-preview");
    var titleInput = f.querySelector("#id_title_ru");
    var submit = function () {
      var btn = document.querySelector('input[name="_continue"], button[name="_continue"]') || document.querySelector('input[name="_save"], button[name="_save"]');
      if (btn) btn.click(); else f.requestSubmit();
    };
    var previewLink = function (cls) {
      var pv = el("a", cls, "Предпросмотр");
      if (preview) { pv.href = preview; pv.target = "_blank"; pv.rel = "noopener"; } else { pv.href = "#"; pv.hidden = true; }
      return pv;
    };
    var saveBtn = function (cls, text) { var b = el("button", cls, text); b.type = "button"; b.addEventListener("click", submit); return b; };

    /* заголовок карточки: название, «Предпросмотр» и «Сохранить» справа (макет D) */
    var head = el("div", "pl-painting-head");
    var h = el("h1", "pl-title", titleInput && titleInput.value ? titleInput.value : (meta && meta.getAttribute("data-title")) || "Новая картина");
    head.appendChild(h);
    var top = el("div", "pl-head-actions");
    top.appendChild(previewLink("pl-link"));
    top.appendChild(saveBtn("pl-btn pl-btn-accent", "Сохранить →"));
    head.appendChild(top);
    if (titleInput) titleInput.addEventListener("input", function () { h.textContent = titleInput.value || "Новая картина"; });

    var side = el("aside", "pl-photos");
    var frame = el("div", "pl-photo-frame");
    var url = meta ? meta.getAttribute("data-photo") : "";
    if (url) { var img = el("img"); img.src = url; img.alt = ""; frame.appendChild(img); } else { frame.appendChild(el("span", "", "Фото не добавлено")); }
    side.appendChild(frame);
    side.appendChild(el("p", "pl-cap", "Основное фото"));
    var addRow = function (caption) {
      if (!photos) return;
      var link = photos.querySelector("a.add-row");
      if (!link) return;
      var before = photos.querySelectorAll('input[type="file"][name$="-image"]:not([name*="__prefix__"])').length;
      link.click();
      setTimeout(function () {
        var inputs = photos.querySelectorAll('input[type="file"][name$="-image"]:not([name*="__prefix__"])');
        var last = inputs[inputs.length - 1];
        if (!last || inputs.length === before) return;
        var cap = photos.querySelector('input[name="' + last.name.replace(/-image$/, "-caption_ru") + '"]');
        if (cap && caption && !cap.value) cap.value = caption;
        last.scrollIntoView({ behavior: "smooth", block: "center" });
        last.click();
      }, 60);
    };
    var replace = function () {
      var first = photos && photos.querySelector('input[type="file"][name^="images-0-"]');
      if (first) { first.click(); return; }
      addRow("");
    };
    if (modeD) {
      var tiles = el("div", "pl-photo-tiles");
      [["+ Фото", ""], ["+ Деталь", "Деталь"], ["+ Интерьер", "В интерьере"]].forEach(function (t) {
        var b = el("button", "pl-tile", t[0]); b.type = "button";
        b.addEventListener("click", function () { addRow(t[1]); });
        tiles.appendChild(b);
      });
      side.appendChild(tiles);
    } else {
      var rep = el("button", "pl-btn pl-btn-ghost", "Заменить фото"); rep.type = "button"; rep.addEventListener("click", replace);
      var add = el("button", "pl-btn pl-btn-ghost", "+ Добавить фото"); add.type = "button"; add.addEventListener("click", function () { addRow(""); });
      side.appendChild(rep);
      side.appendChild(add);
      side.appendChild(el("p", "pl-note", "Изображение показывается целиком. Порядок фото меняется перетаскиванием."));
    }
    if (photos) side.appendChild(photos);

    var fields = el("div", "pl-fields");
    var sets = [];
    inner.querySelectorAll(":scope > fieldset, :scope > .aligned").forEach(function (n) { sets.push(n); });
    sets.forEach(function (n) { fields.appendChild(n); });

    /* «Использовать общее описание» — флажок вместо переключателя режима */
    var radios = f.querySelectorAll('input[type="radio"][name="description_mode"]');
    if (radios.length) {
      var own = f.querySelector('input[type="radio"][name="description_mode"][value="own"]');
      var common = f.querySelector('input[type="radio"][name="description_mode"][value="template"]');
      var row = radios[0].closest(".field-row, .form-row");
      var box = el("div", "pl-common");
      var lab = el("label", "pl-check");
      var cb = el("input"); cb.type = "checkbox"; cb.checked = !!(common && common.checked);
      lab.appendChild(cb); lab.appendChild(el("span", "", "Использовать общее описание"));
      box.appendChild(lab);
      box.appendChild(el("p", "pl-note", "Выключите, чтобы задать индивидуальный текст этой картины."));
      cb.addEventListener("change", function () { var r = cb.checked ? common : own; if (r) { r.checked = true; r.dispatchEvent(new Event("change", { bubbles: true })); } });
      if (row) { row.insertAdjacentElement("beforebegin", box); row.hidden = true; }
    }

    var bottom = el("div", "pl-bottom-actions");
    bottom.appendChild(saveBtn("pl-btn pl-btn-main", "Сохранить"));
    bottom.appendChild(previewLink("pl-btn pl-btn-ghost"));
    fields.appendChild(bottom);

    var grid = el("div", "pl-painting-grid");
    grid.appendChild(side);
    grid.appendChild(fields);
    inner.insertBefore(grid, inner.firstChild);
    inner.insertBefore(head, grid);
  }

  ready(function () {
    tabs();
    menuEditor();
    if (has("model-category") && has("change-form")) categoryLayout();
    if (has("model-painting") && has("change-form")) paintingLayout();
  });
})();
