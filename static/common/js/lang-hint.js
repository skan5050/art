/* Мягкая подсказка языка. Язык браузера всегда решает сам: ru → русский, en → English, zh → 中文, любой другой → English;
   страна IP не учитывается. Только если язык браузера определить нельзя — запасной вариант по стране IP.
   Показывается плашка со ссылкой на нужную версию (если у страницы есть перевод); язык сам не меняется, закрытие запоминается. */
(function () {
  "use strict";
  var page = (document.documentElement.lang || "ru").toLowerCase();
  var langs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ""];
  var first = String(langs[0] || "").trim().toLowerCase();

  if (/^[a-z]{2,3}([-_]|$)/.test(first)) {
    // Язык браузера всегда решает сам и полностью определяет предложение; страна IP не учитывается.
    // ru → русский, en → English, zh → 中文, любой другой корректный язык → English.
    var wanted = first.indexOf("zh") === 0 ? "zh" : first.indexOf("ru") === 0 ? "ru" : "en";
    if (wanted !== page) offer(wanted);
    return;
  }
  // Язык браузера определить невозможно (пусто или невалидно) — запасной вариант по стране IP:
  // RU → русский, CN → 中文, другая известная страна → English, неизвестная — ничего. Только предложение.
  fetch("/geo/lang/", { credentials: "same-origin", headers: { Accept: "application/json" } })
    .then(function (r) { return r.ok ? r.json() : {}; })
    .then(function (d) { if (d && (d.lang === "zh" || d.lang === "en" || d.lang === "ru") && d.lang !== page) offer(d.lang); })
    .catch(function () {});

  function offer(target) {
  var link = document.querySelector('link[rel="alternate"][hreflang="' + target + '"]');
  if (!link) return;
  var KEY = "lang-hint-" + target + "-closed";
  try { if (localStorage.getItem(KEY)) return; } catch (e) {}

  var T = {
    ru: { ask: "Открыть русскую версию? ", go: "Перейти на русский сайт", close: "Закрыть", label: "Язык" },
    zh: { ask: "切换到中文版？ ", go: "查看中文网站", close: "关闭 / Close", label: "语言 / Language" },
    en: { ask: "Prefer English? ", go: "View the English site", close: "Close", label: "Language" }
  }[target];
  var bar = document.createElement("div");
  bar.className = "lang-hint";
  bar.setAttribute("role", "region");
  bar.setAttribute("aria-label", T.label);
  var text = document.createElement("span");
  text.textContent = T.ask;
  var go = document.createElement("a");
  go.href = link.href;
  go.hreflang = target;
  go.lang = target;
  go.textContent = T.go;
  var close = document.createElement("button");
  close.type = "button";
  close.setAttribute("aria-label", T.close);
  close.textContent = "×";
  close.addEventListener("click", function () {
    try { localStorage.setItem(KEY, "1"); } catch (e) {}
    bar.remove();
  });
  bar.appendChild(text); bar.appendChild(go); bar.appendChild(close);
  bar.style.cssText = "display:flex;gap:12px;align-items:center;justify-content:center;flex-wrap:wrap;padding:8px 40px 8px 16px;position:relative;" +
    "background:var(--primary,#1c497e);color:var(--primary-ink,#fff);font:14px/1.4 var(--font-body,inherit)";
  go.style.cssText = "color:inherit;font-weight:700;text-decoration:underline;text-underline-offset:3px";
  close.style.cssText = "position:absolute;right:8px;top:50%;transform:translateY(-50%);background:none;border:0;color:inherit;font-size:22px;line-height:1;cursor:pointer;padding:4px 10px";
  document.body.insertBefore(bar, document.body.firstChild);
  }
})();
