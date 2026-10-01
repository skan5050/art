/* «Города продаж»: список отметок, выбранная точка и превью карты на контурах стран (без внешних тайлов). */
(function () {
  "use strict";
  var form = document.querySelector("[data-city-editor]");
  if (!form || !window.L) return;
  var box = form.querySelector("[data-city-map]");
  /* Карта создается, когда у контейнера уже есть размер (иначе Leaflet считает границы по нулю). */
  var start = function () {
    if (!box.clientWidth) return false;
    init();
    return true;
  };
  function init() {
  var cities = JSON.parse(document.getElementById("city-rows-data").textContent);
  var byId = {};
  var listEl = form.querySelector("[data-city-rows]");
  var hiddenEl = form.querySelector("[data-city-hidden]");
  var foundEl = form.querySelector("[data-city-found]");
  var pointEl = form.querySelector("[data-city-point]");
  var countEl = form.querySelector("[data-city-count]");
  var css = getComputedStyle(form);
  var v = function (n, f) { return (css.getPropertyValue(n) || "").trim() || f; };
  var colors = { marker: v("--pl-marker", "#1c497e"), ring: v("--pl-marker-ring", "#fff"), hot: v("--pl-marker-hot", "#e3bf58"),
    land: v("--pl-land", "#dcebf6"), stroke: v("--pl-stroke", "#9fbfdc") };
  var map = L.map(form.querySelector("[data-city-map]"), { scrollWheelZoom: false, attributionControl: false, zoomSnap: 0.25 });
  map.setView([58, 80], 2);
  var markers = {};
  var selected = null;

  function el(tag, attrs, text) {
    var e = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (text) e.textContent = text;
    return e;
  }
  function hid(name, value) { var i = el("input", { type: "hidden", name: name }); i.value = value; return i; }

  function paint(c) {
    var m = markers[c.id];
    if (!m) return;
    var on = c.on && c.visible;
    m.setStyle({ opacity: on ? 1 : 0, fillOpacity: on ? 1 : 0 });
    var hot = selected === c.id;
    m.setStyle({ fillColor: hot ? colors.hot : colors.marker, weight: hot ? 3 : 2 });
    m.setRadius(hot ? 9 : 6);
  }
  function count() {
    var n = cities.filter(function (c) { return c.on && c.visible; }).length;
    countEl.textContent = "Отмечено на карте: " + n;
  }
  function addMarker(c) {
    if (markers[c.id] || c.lat == null || c.lng == null) return;
    var m = L.circleMarker([c.lat, c.lng], { radius: 6, weight: 2, color: colors.ring, fillColor: colors.marker, fillOpacity: 1 }).addTo(map);
    m.bindTooltip(c.name, { direction: "right", offset: [8, 0], className: "pl-label" });
    m.on("click", function () { select(c.id); });
    markers[c.id] = m;
    paint(c);
  }
  function select(id) {
    var prev = selected;
    selected = id;
    if (prev && byId[prev]) { paint(byId[prev]); byId[prev].li.classList.remove("is-active"); if (markers[prev]) { markers[prev].unbindTooltip(); markers[prev].bindTooltip(byId[prev].name, { direction: "right", offset: [8, 0], className: "pl-label" }); } }
    var c = byId[id];
    c.li.classList.add("is-active");
    paint(c);
    pointEl.hidden = false;
    pointEl.querySelector("[data-point-name]").value = c.name + (c.country ? ", " + c.country : "");
    pointEl.querySelector("[data-point-name]").setAttribute("data-city-id", c.id);
    pointEl.querySelector("[data-point-caption-ru]").value = c.caption_ru || "";
    pointEl.querySelector("[data-point-caption-en]").value = c.caption_en || "";
    pointEl.querySelector("[data-point-visible]").checked = !!(c.on && c.visible);
    if (markers[id]) { markers[id].bringToFront(); markers[id].unbindTooltip(); markers[id].bindTooltip(c.name, { permanent: true, direction: "right", offset: [8, 0], className: "pl-label" }).openTooltip(); }
  }
  function bindPoint() {
    var bind = function (sel, fn) { pointEl.querySelector(sel).addEventListener("input", fn); pointEl.querySelector(sel).addEventListener("change", fn); };
    bind("[data-point-caption-ru]", function (e) { var c = byId[selected]; if (c) { c.caption_ru = e.target.value; c.inputs.cru.value = c.caption_ru; } });
    bind("[data-point-caption-en]", function (e) { var c = byId[selected]; if (c) { c.caption_en = e.target.value; c.inputs.cen.value = c.caption_en; } });
    bind("[data-point-visible]", function (e) {
      var c = byId[selected];
      if (!c) return;
      c.on = e.target.checked;
      c.visible = true;
      c.inputs.on.value = c.on ? "1" : "";
      c.inputs.vis.value = "1";
      c.cb.checked = c.on;
      paint(c); count();
    });
  }
  function addRow(c, isNew) {
    if (byId[c.id]) return byId[c.id];
    byId[c.id] = c;
    c.visible = c.visible !== false;
    var li = el("li", { "class": "pl-city-row", "data-name": (c.name || "").toLowerCase() });
    var lab = el("label", { "class": "pl-check" });
    var cb = el("input", { type: "checkbox" });
    cb.checked = !!c.on;
    lab.appendChild(cb);
    lab.appendChild(el("span", {}, c.name));
    var pick = el("button", { type: "button", "class": "pl-row-pick", title: "Показать точку" }, c.country || "");
    li.appendChild(lab);
    li.appendChild(pick);
    listEl.appendChild(li);
    var box = el("div");
    var inputs = { on: hid("on_" + c.id, c.on ? "1" : ""), vis: hid("visible_" + c.id, c.visible ? "1" : ""),
      cru: hid("caption_ru_" + c.id, c.caption_ru || ""), cen: hid("caption_en_" + c.id, c.caption_en || "") };
    box.appendChild(hid("row", c.id));
    Object.keys(inputs).forEach(function (k) { box.appendChild(inputs[k]); });
    hiddenEl.appendChild(box);
    c.li = li; c.inputs = inputs; c.cb = cb;
    cb.addEventListener("change", function () { c.on = cb.checked; if (c.on) { c.visible = true; inputs.vis.value = "1"; } inputs.on.value = c.on ? "1" : ""; paint(c); count(); if (selected === c.id) pointEl.querySelector("[data-point-visible]").checked = c.on; });
    pick.addEventListener("click", function () { select(c.id); if (markers[c.id]) map.setView(markers[c.id].getLatLng(), Math.max(map.getZoom(), 4)); });
    if (isNew) { c.on = true; cb.checked = true; inputs.on.value = "1"; cities.push(c); }
    addMarker(c);
    return c;
  }
  cities.forEach(function (c) { addRow(c, false); });
  bindPoint();
  count();

  var loaded = false;
  fetch(form.getAttribute("data-geo")).then(function (r) { return r.json(); }).then(function (geo) {
    var land = L.geoJSON(geo, { style: { color: colors.stroke, weight: 1, fillColor: colors.land, fillOpacity: 1 }, interactive: false }).addTo(map);
    map.invalidateSize();
    map.fitBounds(land.getBounds(), { padding: [10, 10], animate: false });
    loaded = true;
    if (cities.length) select(cities[0].id);
  }).catch(function () { map.setView([58, 80], 2.5); if (cities.length) select(cities[0].id); });
  window.addEventListener("resize", function () { map.invalidateSize(); });
  var pts = cities.filter(function (c) { return c.lat != null; });
  if (!pts.length) map.setView([58, 80], 2.5);

  /* Поиск города в справочнике: найденный город добавляется в список отмеченных */
  var modeD = form.getAttribute("data-mode") === "d";
  var q = modeD ? pointEl.querySelector("[data-point-name]") : form.querySelector("[data-city-q]");
  if (modeD) { pointEl.hidden = false; pointEl.querySelector(".pl-point-found").appendChild(foundEl); q.addEventListener("focus", function () { q.select(); }); }
  var timer = null;
  q.addEventListener("input", function () {
    var text = q.value.trim().toLowerCase();
    if (!modeD) listEl.querySelectorAll(".pl-city-row").forEach(function (li) { li.hidden = !!text && li.getAttribute("data-name").indexOf(text) === -1; });
    clearTimeout(timer);
    if (text.length < 2) { foundEl.hidden = true; return; }
    timer = setTimeout(function () {
      fetch(form.getAttribute("data-search-url") + "?q=" + encodeURIComponent(text)).then(function (r) { return r.json(); }).then(function (data) {
        foundEl.textContent = "";
        data.results.filter(function (c) { return !byId[c.id]; }).forEach(function (c) {
          var li = el("li");
          var b = el("button", { type: "button" }, "+ " + c.name + (c.region ? ", " + c.region : "") + " — " + c.country);
          b.addEventListener("click", function () { var row = addRow(c, true); foundEl.hidden = true; if (!modeD) { q.value = ""; q.dispatchEvent(new Event("input")); } select(row.id); if (markers[row.id]) map.setView(markers[row.id].getLatLng(), Math.max(map.getZoom(), 4)); count(); });
          li.appendChild(b); foundEl.appendChild(li);
        });
        foundEl.hidden = !foundEl.children.length;
      });
    }, 250);
  });
  }
  if (!start()) {
    var ro = new ResizeObserver(function () { if (start()) ro.disconnect(); });
    ro.observe(box);
  }
})();
