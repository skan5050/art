/* Автоопределение города для городских страниц (только посетители из РФ; решает сервер, /geo/city/).
   IP — лишь предложение: переход и запоминание города происходят после клика посетителя.
   В форме заказа город страницы важнее сохранённого selected_city; IP — только предложение. */
(function () {
  "use strict";
  var cfgEl = document.getElementById("city-geo");
  if (!cfgEl) return;
  var cfg;
  try { cfg = JSON.parse(cfgEl.textContent); } catch (e) { return; }
  var current = cfg.current, cities = cfg.cities || [], COOKIE = "selected_city", DAYS = cfg.days || 30;
  var byKey = {};
  cities.concat([current]).forEach(function (c) { byKey[c.key] = c; });

  function readCookie() {
    var m = document.cookie.match(new RegExp("(?:^|; )" + COOKIE + "=([^;]*)"));
    return m ? decodeURIComponent(m[1]) : "";
  }
  function saveCity(key) {
    var c = byKey[key];
    document.cookie = COOKIE + "_name=" + encodeURIComponent(c ? c.name : "") + "; max-age=" + DAYS * 86400 + "; path=/; SameSite=Lax" + (location.protocol === "https:" ? "; Secure" : "");
    document.cookie = COOKIE + "=" + encodeURIComponent(key) + "; max-age=" + DAYS * 86400 + "; path=/; SameSite=Lax" + (location.protocol === "https:" ? "; Secure" : "");
  }

  // Город в форме заказа на городской странице — всегда город этой страницы (его выставляет шаблон);
  // выбранный ранее город сюда не вмешивается, ручной ввод в форме не меняет selected_city.
  var saved = byKey[readCookie()];
  if (saved) return;  // город уже выбран или подтверждён — не спрашиваем
  try { if (sessionStorage.getItem("city-geo-closed")) return; } catch (e) {}

  fetch(cfg.endpoint, { credentials: "same-origin", headers: { Accept: "application/json" } })
    .then(function (r) { return r.ok ? r.json() : {}; })
    .then(function (guess) { if (guess && guess.key) show(guess); })
    .catch(function () {});  // геобаза недоступна — страница работает как обычно

  function el(tag, text, css) {
    var n = document.createElement(tag);
    if (text) n.textContent = text;
    if (css) n.style.cssText = css;
    return n;
  }

  function show(guess) {
    var same = guess.key === current.key;
    var compact = window.matchMedia("(max-width: 640px)").matches;
    var bar = el("div", "", "position:relative;display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;justify-content:center;padding:8px 40px 8px 16px;" +
      "background:var(--surface,#f3f8fc);color:var(--text,#13253a);border-bottom:1px solid var(--line,#d9e5f0);font-size:14px;line-height:1.4");
    bar.className = "city-geo-bar";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", cfg.labels.region);
    bar.appendChild(el("span", cfg.labels.ask.replace("{city}", guess.name), "font-weight:600"));

    function button(label, primary, handler) {
      var b = el("button", label, "font:inherit;font-weight:600;cursor:pointer;border-radius:4px;padding:4px 12px;min-height:30px;" +
        (primary ? "background:var(--primary,#1c497e);color:var(--primary-ink,#fff);border:1px solid var(--primary,#1c497e)" : "background:transparent;color:inherit;border:1px solid var(--line,#999)"));
      b.type = "button";
      b.addEventListener("click", handler);
      bar.appendChild(b);
      return b;
    }
    function done() { bar.remove(); }

    if (same) {
      button(compact ? cfg.labels.yes_short : cfg.labels.yes, true, function () { saveCity(current.key); done(); });
    } else {
      button(cfg.labels.go.replace("{city}", guess.name), true, function () { saveCity(guess.key); location.href = guess.url; });
      button(cfg.labels.stay.replace("{city}", current.name), false, function () { saveCity(current.key); done(); });
    }
    var other = button(compact ? cfg.labels.other_short : cfg.labels.other, false, function () { picker.hidden = !picker.hidden; if (!picker.hidden) search.focus(); });
    other.setAttribute("aria-expanded", "false");

    var close = el("button", "×", "position:absolute;right:8px;top:50%;transform:translateY(-50%);background:none;border:0;color:inherit;font-size:22px;line-height:1;cursor:pointer;padding:4px 10px");
    close.type = "button";
    close.setAttribute("aria-label", cfg.labels.close);
    close.addEventListener("click", function () { try { sessionStorage.setItem("city-geo-closed", "1"); } catch (e) {} done(); });
    bar.appendChild(close);

    // Простой список-поиск российских городских страниц, без отдельного справочника.
    var picker = el("div", "", "flex-basis:100%;max-width:420px;margin:0 auto");
    picker.hidden = true;
    var search = el("input", "", "width:100%;font:inherit;padding:6px 10px;border:1px solid var(--line,#999);border-radius:4px;background:#fff;color:#111");
    search.type = "search";
    search.placeholder = cfg.labels.search;
    search.setAttribute("aria-label", cfg.labels.search);
    var list = el("ul", "", "list-style:none;margin:6px 0 0;padding:0;max-height:200px;overflow:auto;text-align:left");
    cities.forEach(function (c) {
      var li = el("li");
      var b = el("button", c.name, "display:block;width:100%;text-align:left;font:inherit;background:none;border:0;color:inherit;padding:5px 8px;cursor:pointer");
      b.type = "button";
      b.setAttribute("data-city-key", c.key);
      b.addEventListener("click", function () {
        saveCity(c.key);
        if (c.key === current.key) done(); else location.href = c.url;
      });
      li.appendChild(b);
      li.setAttribute("data-name", c.name.toLowerCase());
      list.appendChild(li);
    });
    search.addEventListener("input", function () {
      var q = search.value.trim().toLowerCase().replace(/ё/g, "е");
      Array.prototype.forEach.call(list.children, function (li) { li.hidden = q && li.getAttribute("data-name").replace(/ё/g, "е").indexOf(q) === -1; });
    });
    picker.appendChild(search); picker.appendChild(list);
    bar.appendChild(picker);
    document.body.insertBefore(bar, document.body.firstChild);
  }
})();
