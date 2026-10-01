/* Город в форме заказа на страницах, которые не являются городскими: подставляется сохранённый выбор
   (selected_city), если он есть. На городских страницах город берётся из самой страницы (city-geo.js не вмешивается). */
(function () {
  "use strict";
  if (document.getElementById("city-geo")) return;
  var m = document.cookie.match(/(?:^|; )selected_city_name=([^;]*)/);
  var name = m ? decodeURIComponent(m[1]) : "";
  if (!name) return;
  Array.prototype.forEach.call(document.querySelectorAll("[data-order]:not([data-city])"), function (el) { el.setAttribute("data-city", name); });
  var inline = document.querySelector("form input[name=city]");
  if (inline && !inline.value && !inline.closest("dialog")) inline.value = name;
})();
