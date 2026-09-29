/* Карта «География наших продаж»: только подтвержденные города; число в группе — число городов. */
(function () {
  "use strict";
  var el = document.querySelector("[data-sales-map]");
  var dataEl = document.getElementById("sales-cities");
  if (!el || !dataEl || !window.L) return;
  var cities = JSON.parse(dataEl.textContent);
  var countLabel = el.getAttribute("data-count-label") || "";
  var map = L.map(el, { scrollWheelZoom: false, worldCopyJump: true });
  map.attributionControl.setPrefix('<a href="https://leafletjs.com">Leaflet</a>');
  L.tileLayer(el.getAttribute("data-tiles"), { maxZoom: 12, attribution: el.getAttribute("data-attribution") }).addTo(map);
  var group = L.markerClusterGroup ? L.markerClusterGroup({
    showCoverageOnHover: false,
    iconCreateFunction: function (cluster) {
      var n = cluster.getChildCount();
      return L.divIcon({ html: '<div><span>' + n + '</span></div>', className: "marker-cluster marker-cluster-small",
        iconSize: L.point(40, 40) });
    }
  }) : L.featureGroup();
  var markers = {};
  cities.forEach(function (c) {
    var m = L.marker([c.lat, c.lng], { title: c.name, alt: c.name });
    var popup = document.createElement("div");
    var strong = document.createElement("strong"); strong.textContent = c.name; popup.appendChild(strong);
    if (c.caption) { var p = document.createElement("div"); p.textContent = c.caption; popup.appendChild(p); }
    m.bindPopup(popup);
    group.addLayer(m);
    markers[c.lat + "," + c.lng] = m;
  });
  map.addLayer(group);
  if (cities.length) {
    map.fitBounds(group.getBounds(), { padding: [30, 30], maxZoom: 6 });
  } else {
    map.setView([56, 70], 3);
  }
  document.querySelectorAll("[data-geo-focus]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var li = btn.closest("[data-geo-city]");
      var key = li.getAttribute("data-lat") + "," + li.getAttribute("data-lng");
      var m = markers[key];
      if (!m) return;
      if (group.zoomToShowLayer) { group.zoomToShowLayer(m, function () { m.openPopup(); }); } else { map.setView(m.getLatLng(), 7); m.openPopup(); }
      el.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  });
  var search = document.querySelector("[data-geo-search]");
  if (search) {
    search.addEventListener("input", function () {
      var q = search.value.trim().toLowerCase();
      document.querySelectorAll("[data-geo-city]").forEach(function (li) {
        li.hidden = q && li.getAttribute("data-name").indexOf(q) === -1;
      });
      document.querySelectorAll(".geo-country").forEach(function (g) {
        g.hidden = !g.querySelector("[data-geo-city]:not([hidden])");
      });
    });
  }
})();
