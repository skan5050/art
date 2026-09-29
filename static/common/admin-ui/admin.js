/* Счетчики длины SEO-полей: рекомендации Яндекса для Title и Description. */
(function () {
  "use strict";
  var RULES = [
    { re: /^(id_)?(seo_title|og_title)_(ru|en)$/, min: 10, max: 60, note: "Title: до 60 символов (к нему добавится название сайта)" },
    { re: /^(id_)?(seo_description|og_description)_(ru|en)$/, min: 70, max: 160, note: "Description: 70–160 символов" },
  ];
  function attach(input) {
    var rule = RULES.filter(function (r) { return r.re.test(input.id || input.name || ""); })[0];
    if (!rule || input.dataset.seoCounter) return;
    input.dataset.seoCounter = "1";
    var out = document.createElement("span");
    out.className = "seo-counter";
    input.insertAdjacentElement("afterend", out);
    var update = function () {
      var n = input.value.trim().length;
      out.textContent = n ? (n + " симв. · " + rule.note) : ("Пусто — будет использован SEO-шаблон · " + rule.note);
      out.classList.toggle("is-warn", n > 0 && n < rule.min);
      out.classList.toggle("is-bad", n > rule.max);
    };
    input.addEventListener("input", update);
    update();
  }
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("input[type=text], textarea").forEach(attach);
  });
})();
