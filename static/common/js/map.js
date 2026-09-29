/* Карта «География наших продаж»: векторные контуры стран + подтвержденные города.
   Внешние тайлы не нужны; если в настройках указан адрес тайлов, он подключается как подложка.
   Интерактив: подсветка города, строки списка и страны при наведении; по клику — подсказка
   по доставке с условиями, ссылками СДЭК и кнопкой обращения с уже указанным городом. */
(function () {
  "use strict";
  if (!window.L) return;
  var esc = function (s) { return String(s || "").replace(/[&<>"']/g, function (ch) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]; }); };

  document.querySelectorAll("[data-sales-map]").forEach(function (el) {
    var dataEl = document.getElementById(el.getAttribute("data-cities"));
    var cities = dataEl ? JSON.parse(dataEl.textContent) : [];
    var t = el.dataset;
    var css = getComputedStyle(el);
    var v = function (name, fallback) { return (css.getPropertyValue(name) || "").trim() || fallback; };
    var colors = {
      marker: v("--map-marker", "#1c497e"), ring: v("--map-marker-ring", "#ffffff"), hot: v("--map-marker-hot", "#e3bf58"),
      land: v("--map-land", "#dcebf6"), landHot: v("--map-land-hot", "#c6ddf0"), stroke: v("--map-stroke", "#9fbfdc"),
    };
    var map = L.map(el, { scrollWheelZoom: false, worldCopyJump: false, zoomSnap: 0.25, attributionControl: true });
    map.attributionControl.setPrefix('<a href="https://leafletjs.com">Leaflet</a>');
    map.attributionControl.addAttribution('Города: <a href="https://www.geonames.org/" target="_blank" rel="noopener">GeoNames</a> (CC BY 4.0)');
    var tiles = el.getAttribute("data-tiles");
    if (tiles) {
      L.tileLayer(tiles, { maxZoom: 12, attribution: el.getAttribute("data-attribution") }).addTo(map);
    } else {
      map.attributionControl.addAttribution("Natural Earth");
    }

    var root = el.closest(".geo-section") || document;
    var markers = {};
    var selected = null;
    var keyOf = function (c) { return c.lat + "," + c.lng; };
    var liOf = function (c) { return root.querySelector('[data-geo-city][data-lat="' + c.lat + '"][data-lng="' + c.lng + '"]'); };
    var panel = {
      city: root.querySelector("[data-geo-selected]"),
      caption: root.querySelector("[data-geo-selected-caption]"),
      discuss: root.querySelector("[data-geo-discuss]"),
      landing: root.querySelector("[data-geo-landing]"),
      landingLink: root.querySelector("[data-geo-landing-link]"),
    };

    /* Подсказка по доставке в город (всплывающее окно на карте) */
    var popupHtml = function (c) {
      var links = [];
      if (t.officesUrl) links.push('<a href="' + esc(t.officesUrl) + '" target="_blank" rel="noopener nofollow">' + esc(t.tOffices) + ' ↗</a>');
      if (t.calcUrl) links.push('<a href="' + esc(t.calcUrl) + '" target="_blank" rel="noopener nofollow">' + esc(t.tCalc) + ' ↗</a>');
      if (c.landing) links.push('<a href="' + esc(c.landing) + '">' + esc(t.tCityPage) + ' →</a>');
      return '<div class="geo-pop">' +
        '<p class="geo-pop-city">' + esc(c.name) + '<span>' + esc(c.country) + '</span></p>' +
        '<p class="geo-pop-caption">' + esc(c.caption || t.tCityNote) + '</p>' +
        '<p class="geo-pop-title">' + esc(t.tHintTitle) + '</p>' +
        '<p class="geo-pop-text">' + esc(t.tHint) + '</p>' +
        (links.length ? '<p class="geo-pop-links">' + links.join("") + '</p>' : "") +
        (t.calcUrl ? '<p class="geo-pop-note">' + esc(t.tNote) + '</p>' : "") +
        '<a class="btn btn-primary btn-block geo-pop-btn" href="' + esc(t.orderUrl) + '" data-order data-kind="delivery" data-city="' + esc(c.name) + '">' + esc(t.tDiscuss) + '</a>' +
        '</div>';
    };

    var paint = function (item, state) {
      var on = state === "hot" || state === "selected";
      item.marker.setStyle({ fillColor: on ? colors.hot : colors.marker, color: colors.ring, weight: on ? 3 : 2 });
      item.marker.setRadius(state === "selected" ? 9 : state === "hot" ? 8 : 6);
      var tip = item.marker.getTooltip() && item.marker.getTooltip().getElement();
      if (tip) { tip.classList.toggle("is-hot", state === "hot"); tip.classList.toggle("is-active", state === "selected"); }
      var li = liOf(item.city);
      if (li) { li.classList.toggle("is-hot", state === "hot"); li.classList.toggle("is-active", state === "selected"); }
    };
    var hover = function (c, on) {
      var item = markers[keyOf(c)];
      if (!item) return;
      if (on) { item.marker.bringToFront(); paint(item, selected === c ? "selected" : "hot"); }
      else paint(item, selected === c ? "selected" : "");
      declutter();
    };
    var select = function (c, withPopup) {
      var prev = selected;
      selected = c;
      if (prev && markers[keyOf(prev)]) paint(markers[keyOf(prev)], "");
      var item = markers[keyOf(c)];
      if (item) { paint(item, "selected"); if (withPopup) item.marker.openPopup(); }
      if (panel.city) panel.city.textContent = c.name;
      if (panel.caption) panel.caption.textContent = c.caption || panel.caption.getAttribute("data-default") || "";
      if (panel.discuss) panel.discuss.setAttribute("data-city", c.name);
      if (panel.landing) { panel.landing.hidden = !c.landing; if (c.landing && panel.landingLink) panel.landingLink.href = c.landing; }
      declutter();
    };

    /* Подписи не должны наезжать друг на друга: выбранный и подсвеченный город в приоритете,
       затем более крупные; остальные подписи скрываются до приближения (точки остаются). */
    var declutter = function () {
      var placed = [];
      var prio = function (item) {
        var tip = item.marker.getTooltip().getElement();
        return tip && (tip.classList.contains("is-hot") || tip.classList.contains("is-active")) ? 0 : 1;
      };
      Object.keys(markers).map(function (k) { return markers[k]; })
        .sort(function (a, b) { return (prio(a) - prio(b)) || (a.city.rank - b.city.rank); })
        .forEach(function (item) {
          var tip = item.marker.getTooltip().getElement();
          if (!tip) return;
          if (item.hidden) { tip.style.visibility = "hidden"; return; }
          tip.style.visibility = "";
          var box = tip.closest(".leaflet-container").getBoundingClientRect();
          var hits = function (r) {
            if (r.left < box.left + 2 || r.right > box.right - 2 || r.top < box.top || r.bottom > box.bottom) return true;
            return placed.some(function (p) { return !(r.right + 2 < p.left || r.left - 2 > p.right || r.bottom + 1 < p.top || r.top - 1 > p.bottom); });
          };
          tip.style.marginLeft = "";
          var r = tip.getBoundingClientRect();
          if (hits(r)) {  // справа тесно — пробуем слева от точки
            tip.style.marginLeft = -(r.width + 18) + "px";
            r = tip.getBoundingClientRect();
          }
          if (hits(r)) { tip.style.marginLeft = ""; tip.style.visibility = "hidden"; } else placed.push(r);
        });
    };
    map.on("zoomend moveend", function () { window.requestAnimationFrame(declutter); });

    var drawCities = function () {
      cities.forEach(function (c) {
        var m = L.circleMarker([c.lat, c.lng], {
          radius: 6, weight: 2, color: colors.ring, fillColor: colors.marker, fillOpacity: 1, className: "geo-dot",
        }).addTo(map);
        m.bindTooltip(c.name, { permanent: true, direction: "right", offset: [8, 0], className: "geo-label" });
        m.bindPopup(function () { return popupHtml(c); }, { className: "geo-popup", maxWidth: 300, minWidth: 240, autoPanPadding: [20, 20] });
        m.on("mouseover", function () { hover(c, true); });
        m.on("mouseout", function () { hover(c, false); });
        m.on("click", function () { select(c, false); });
        markers[keyOf(c)] = { marker: m, city: c };
      });
      window.requestAnimationFrame(declutter);
    };

    fetch(el.getAttribute("data-geo")).then(function (r) { return r.json(); }).then(function (geo) {
      var land = L.geoJSON(geo, {
        style: { color: colors.stroke, weight: 1, fillColor: colors.land, fillOpacity: 1 },
        onEachFeature: function (feature, layer) {  // подсветка страны при наведении
          layer.on("mouseover", function () { layer.setStyle({ fillColor: colors.landHot }); });
          layer.on("mouseout", function () { layer.setStyle({ fillColor: colors.land }); });
        },
      }).addTo(map);
      var bounds = land.getBounds();
      map.fitBounds(bounds, { padding: [12, 12] });
      map.setMaxBounds(bounds.pad(0.4));
      drawCities();
    }).catch(function () {
      map.setView([58, 80], 2.5);
      drawCities();
    });

    /* Список городов: наведение подсвечивает точку, клик — приближает и открывает подсказку */
    root.querySelectorAll("[data-geo-city]").forEach(function (li) {
      var get = function () { return markers[li.getAttribute("data-lat") + "," + li.getAttribute("data-lng")]; };
      li.addEventListener("mouseenter", function () { var it = get(); if (it) hover(it.city, true); });
      li.addEventListener("mouseleave", function () { var it = get(); if (it) hover(it.city, false); });
      var btn = li.querySelector("[data-geo-focus]");
      btn.addEventListener("focus", function () { var it = get(); if (it) hover(it.city, true); });
      btn.addEventListener("blur", function () { var it = get(); if (it) hover(it.city, false); });
      btn.addEventListener("click", function () {
        var it = get();
        if (!it) return;
        map.setView(it.marker.getLatLng(), Math.max(map.getZoom(), 4));
        select(it.city, true);
      });
    });
    var search = root.querySelector("[data-geo-search]");
    var country = root.querySelector("[data-geo-country]");
    var filter = function () {
      var q = search ? search.value.trim().toLowerCase() : "";
      var cc = country ? country.value : "";
      root.querySelectorAll("[data-geo-city]").forEach(function (li) {
        var show = (!q || li.getAttribute("data-name").indexOf(q) !== -1) && (!cc || li.getAttribute("data-country") === cc);
        li.hidden = !show;
        var item = markers[li.getAttribute("data-lat") + "," + li.getAttribute("data-lng")];
        if (item) { item.hidden = !show; item.marker.setStyle({ opacity: show ? 1 : 0.25, fillOpacity: show ? 1 : 0.25 }); }
      });
      declutter();
    };
    if (search) search.addEventListener("input", filter);
    if (country) country.addEventListener("change", filter);
  });
})();
