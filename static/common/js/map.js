/* Карта «География наших продаж»: векторные контуры стран + подтвержденные города.
   Внешние тайлы не нужны; если в настройках указан адрес тайлов, он подключается как подложка. */
(function () {
  "use strict";
  if (!window.L) return;
  document.querySelectorAll("[data-sales-map]").forEach(function (el) {
    var dataEl = document.getElementById(el.getAttribute("data-cities"));
    var cities = dataEl ? JSON.parse(dataEl.textContent) : [];
    var css = getComputedStyle(el);
    var v = function (name, fallback) { return (css.getPropertyValue(name) || "").trim() || fallback; };
    var map = L.map(el, { scrollWheelZoom: false, worldCopyJump: false, zoomSnap: 0.25, attributionControl: true });
    map.attributionControl.setPrefix('<a href="https://leafletjs.com">Leaflet</a>');
    var tiles = el.getAttribute("data-tiles");
    if (tiles) {
      L.tileLayer(tiles, { maxZoom: 12, attribution: el.getAttribute("data-attribution") }).addTo(map);
    } else {
      map.attributionControl.addAttribution("Natural Earth");
    }
    var markers = {};
    var panelCity = el.parentNode.querySelector("[data-geo-selected]");
    var panelCaption = el.parentNode.querySelector("[data-geo-selected-caption]");
    var select = function (c) {
      if (panelCity) panelCity.textContent = c.name;
      if (panelCaption) panelCaption.textContent = c.caption || "";
    };
    var drawCities = function () {
      cities.forEach(function (c) {
        var m = L.circleMarker([c.lat, c.lng], {
          radius: 6, weight: 2, color: v("--map-marker-ring", "#ffffff"), fillColor: v("--map-marker", "#1c497e"), fillOpacity: 1,
        }).addTo(map);
        m.bindTooltip(c.name, { permanent: true, direction: "right", offset: [8, 0], className: "geo-label" });
        m.on("click", function () { select(c); });
        markers[c.lat + "," + c.lng] = { marker: m, city: c };
      });
    };
    fetch(el.getAttribute("data-geo")).then(function (r) { return r.json(); }).then(function (geo) {
      var land = L.geoJSON(geo, {
        style: { color: v("--map-stroke", "#9fbfdc"), weight: 1, fillColor: v("--map-land", "#dcebf6"), fillOpacity: 1 },
        interactive: false,
      }).addTo(map);
      var bounds = land.getBounds();
      map.fitBounds(bounds, { padding: [12, 12] });
      map.setMaxBounds(bounds.pad(0.4));
      drawCities();
    }).catch(function () {
      map.setView([58, 80], 2.5);
      drawCities();
    });

    var root = el.closest(".geo-section") || document;
    root.querySelectorAll("[data-geo-focus]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var li = btn.closest("[data-geo-city]");
        var item = markers[li.getAttribute("data-lat") + "," + li.getAttribute("data-lng")];
        if (!item) return;
        map.setView(item.marker.getLatLng(), Math.max(map.getZoom(), 4));
        select(item.city);
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
        if (item) item.marker.setStyle({ opacity: show ? 1 : 0.25, fillOpacity: show ? 1 : 0.25 });
      });
    };
    if (search) search.addEventListener("input", filter);
    if (country) country.addEventListener("change", filter);
  });
})();
