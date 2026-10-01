/* Мягкая подсказка языка: если браузер посетителя на китайском, а страница русская или английская,
   сверху показывается плашка со ссылкой на китайскую версию. Язык сам не меняется; закрытие запоминается. */
(function () {
  "use strict";
  var KEY = "lang-hint-zh-closed";
  var link = document.querySelector('link[rel="alternate"][hreflang="zh"]');
  if (!link || document.documentElement.lang === "zh") return;
  var langs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ""];
  var first = String(langs[0] || "").toLowerCase();
  if (first.indexOf("zh") !== 0) return;  // китайский должен быть основным языком браузера
  try { if (localStorage.getItem(KEY)) return; } catch (e) {}

  var bar = document.createElement("div");
  bar.className = "lang-hint";
  bar.setAttribute("role", "region");
  bar.setAttribute("aria-label", "语言 / Language");
  var text = document.createElement("span");
  text.textContent = "切换到中文版？ ";
  var go = document.createElement("a");
  go.href = link.href;
  go.hreflang = "zh";
  go.lang = "zh";
  go.textContent = "查看中文网站";
  var close = document.createElement("button");
  close.type = "button";
  close.setAttribute("aria-label", "关闭 / Close");
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
})();
