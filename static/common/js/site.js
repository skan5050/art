/* Поведение сайта. Без внешних библиотек; содержание доступно и без JavaScript. */
(function () {
  "use strict";

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  /* ---------- Меню: компактный режим по содержимому, а не только по ширине экрана ---------- */
  var nav = $("[data-nav]");
  if (nav) {
    var menu = $("[data-menu]", nav);
    var toggle = $("[data-nav-toggle]", nav);
    var measure = function () {
      nav.classList.remove("is-compact");
      nav.classList.add("is-measuring");
      var items = $$("li", menu);
      var overflow = menu.scrollWidth > menu.clientWidth + 1;
      if (!overflow && items.length > 1) {
        overflow = items[items.length - 1].offsetTop > items[0].offsetTop + 4;
      }
      nav.classList.remove("is-measuring");
      nav.classList.toggle("is-compact", overflow);
      if (!overflow) { nav.classList.remove("is-open"); toggle.setAttribute("aria-expanded", "false"); }
    };
    toggle.addEventListener("click", function () {
      var open = !nav.classList.contains("is-open");
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        nav.classList.remove("is-open"); toggle.setAttribute("aria-expanded", "false"); toggle.focus();
      }
    });
    var timer;
    window.addEventListener("resize", function () { clearTimeout(timer); timer = setTimeout(measure, 80); });
    if (document.fonts && document.fonts.ready) { document.fonts.ready.then(measure); }
    measure();

    /* Липкое меню: при прокрутке закрепляется вверху, становится компактнее, в A появляется мини-логотип */
    var stuck = false;
    var onScroll = function () {
      var now = nav.getBoundingClientRect().top <= 0 && window.scrollY > 4;
      if (now !== stuck) {
        stuck = now;
        nav.classList.toggle("is-stuck", now);
        document.body.classList.toggle("nav-stuck", now);
        measure();
      }
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Выпадающее меню мессенджеров ---------- */
  $$("[data-dropdown]").forEach(function (dd) {
    var btn = $("[data-dropdown-toggle]", dd);
    var panel = $("[data-dropdown-panel]", dd);
    var close = function () { panel.hidden = true; btn.setAttribute("aria-expanded", "false"); };
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = panel.hidden;
      panel.hidden = !open;
      btn.setAttribute("aria-expanded", String(open));
      if (open) { var first = $("a", panel); if (first) first.focus(); }
    });
    document.addEventListener("click", function (e) { if (!dd.contains(e.target)) close(); });
    dd.addEventListener("keydown", function (e) { if (e.key === "Escape") { close(); btn.focus(); } });
  });

  /* ---------- Поле желаемого размера ---------- */
  function setupSize(form) {
    var field = $("[data-size-field]", form);
    if (!field) return;
    var select = $("[data-size-select]", field);
    var choice = $("[data-size-choice]", field);
    var sizeId = $("[data-size-id]", field);
    var orient = $("[data-size-orientation]", field);
    var custom = $("[data-size-custom]", field);
    var sync = function () {
      var v = select.value;
      var opt = select.options[select.selectedIndex];
      var isStd = v && v !== "custom" && v !== "undecided";
      choice.value = isStd ? "standard" : v;
      sizeId.value = isStd ? v : "";
      orient.hidden = !(isStd && opt && opt.getAttribute("data-square") === "0");
      custom.hidden = v !== "custom";
      if (orient.hidden) $$("input", orient).forEach(function (r) { r.checked = false; });
    };
    select.addEventListener("change", sync);
    form._setSizes = function (list) {
      var group = $("[data-size-options]", select);
      if (!group) return;
      if (!form._defaultSizes) form._defaultSizes = group.innerHTML;
      if (list) {
        var unit = document.documentElement.lang === "en" ? "cm" : "см";
        group.innerHTML = "";
        list.forEach(function (s) {
          var o = document.createElement("option");
          o.value = s.id; o.textContent = s.label + " " + unit;
          o.setAttribute("data-square", s.square ? "1" : "0");
          group.appendChild(o);
        });
      } else {
        group.innerHTML = form._defaultSizes;
      }
      select.value = ""; sync();
    };
    form._selectSize = function (value) { select.value = value || ""; sync(); };
    sync();
  }

  /* ---------- Способ связи, номинал сертификата, вложение ---------- */
  function setupContact(form) {
    var input = $("[data-contact-input]", form);
    var method = $("[data-contact-method]", form);
    var update = function () {
      if (!method || !input) return;
      var opt = method.options[method.selectedIndex];
      var v = method.value;
      input.placeholder = opt ? (opt.getAttribute("data-placeholder") || "") : "";
      input.type = v === "email" ? "email" : (v === "phone" || v === "whatsapp" ? "tel" : "text");
      input.autocomplete = v === "email" ? "email" : (v === "phone" || v === "whatsapp" ? "tel" : "off");
    };
    if (method) method.addEventListener("change", update);
    update();
    var amount = $("[data-cert-amount]", form);
    var customInput = $("[data-cert-custom]", form);
    if (amount && customInput) {
      amount.addEventListener("change", function () { customInput.hidden = amount.value !== "custom"; });
    }
    var file = $("[data-file-input]", form);
    var fileLabel = $("[data-file-label]", form);
    if (file && fileLabel) {
      var initial = fileLabel.textContent;
      file.addEventListener("change", function () {
        fileLabel.textContent = file.files && file.files[0] ? file.files[0].name : initial;
      });
    }
  }

  function uuid() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return "k" + Date.now().toString(36) + Math.random().toString(36).slice(2);
  }

  /* ---------- Отправка формы: успех показывается только после сохранения на сервере ---------- */
  function clearErrors(form) {
    $$("[data-error-for]", form).forEach(function (el) { el.hidden = true; el.textContent = ""; });
    $$(".has-error", form).forEach(function (el) { el.classList.remove("has-error"); });
    var status = $("[data-form-status]", form); status.hidden = true; status.textContent = "";
  }

  function showErrors(form, errors, message) {
    var first = null;
    Object.keys(errors || {}).forEach(function (key) {
      var slot = $('[data-error-for="' + key + '"]', form);
      if (!slot) return;
      slot.textContent = errors[key]; slot.hidden = false;
      var field = slot.closest(".field"); if (field) field.classList.add("has-error");
      if (!first) first = field && $("input:not([type=hidden]), select, textarea", field);
    });
    var status = $("[data-form-status]", form);
    status.textContent = message || ""; status.hidden = !message;
    (first || status).focus && (first || status).focus();
  }

  /* Цели аналитики: клик по телефону и мессенджеру — отдельно от успешной заявки */
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a) return;
    var href = a.getAttribute("href") || "";
    var goal = href.indexOf("tel:") === 0 ? "phone_click" : (/t\.me|wa\.me|whatsapp|max\.ru|vk\.com|viber/.test(href) ? "messenger_click" : "");
    if (!goal) return;
    try { if (window.ym && window.ART_METRIKA_ID) ym(window.ART_METRIKA_ID, "reachGoal", goal); } catch (err) {}
    try { if (window.gtag) gtag("event", goal); } catch (err) {}
  });

  function reachGoal() {
    try { if (window.ym && window.ART_METRIKA_ID) ym(window.ART_METRIKA_ID, "reachGoal", "lead_sent"); } catch (e) {}
    try { if (window.gtag) gtag("event", "generate_lead"); } catch (e) {}
  }

  function setupForm(form) {
    setupSize(form);
    setupContact(form);
    var keyField = $("[data-field=idempotency_key]", form);
    keyField.value = uuid();
    form.addEventListener("focusin", function () { document.body.classList.add("form-focus"); });
    form.addEventListener("focusout", function () { document.body.classList.remove("form-focus"); });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form._busy) return;
      clearErrors(form);
      if (!window.fetch) { form.submit(); return; }
      var btn = $("[data-submit]", form);
      var label = btn.textContent;
      form._busy = true; btn.disabled = true; btn.textContent = btn.getAttribute("data-sending");
      fetch(form.action, {
        method: "POST", body: new FormData(form), credentials: "same-origin",
        headers: { "X-Requested-With": "fetch" }
      }).then(function (r) {
        return r.json().catch(function () { return { ok: false }; }).then(function (data) { data._status = r.status; return data; });
      }).then(function (data) {
        if (data.ok) {
          reachGoal();
          form.dispatchEvent(new CustomEvent("lead:sent", { bubbles: true, detail: data }));
          var modal = form.closest("[data-order-modal]");
          if (!modal) {
            var box = document.createElement("div");
            box.className = "flash flash-success"; box.setAttribute("role", "status"); box.tabIndex = -1;
            box.textContent = data.message;
            form.replaceWith(box); box.focus();
          }
        } else {
          showErrors(form, data.errors, data.message || "Ошибка");
          keyField.value = data._status >= 500 ? keyField.value : uuid();
        }
      }).catch(function () {
        showErrors(form, {}, form.getAttribute("data-network-error") || (document.documentElement.lang === "en" ? "Could not send the request. Your text is still in the form — please try again." : "Не удалось отправить заявку. Текст остался в форме — попробуйте еще раз."));
      }).then(function () {
        form._busy = false; btn.disabled = false; btn.textContent = label;
      });
    });
  }
  $$("[data-order-form]").forEach(setupForm);

  /* ---------- Модальное окно заказа с контекстом страницы ---------- */
  var modal = $("[data-order-modal]");
  if (modal && typeof modal.showModal === "function") {
    var form = $("[data-order-form]", modal);
    var success = $("[data-modal-success]", modal);
    var body = $("[data-modal-body]", modal);
    var lastTrigger = null;
    var field = function (n) { return $('[data-field="' + n + '"]', form); };

    var open = function (trigger) {
      lastTrigger = trigger;
      var kind = trigger.getAttribute("data-kind") || "general";
      var status = trigger.getAttribute("data-status") || "";
      if (kind === "painting" && status === "sold") kind = "similar";
      field("kind").value = kind;
      field("painting_id").value = trigger.getAttribute("data-painting") || "";
      field("category_id").value = trigger.getAttribute("data-category") || "";
      field("source_url").value = location.pathname;
      var title = modal.getAttribute("data-title-" + kind) || modal.getAttribute("data-title-general");
      $("[data-modal-title]", modal).textContent = title;
      var ctx = trigger.getAttribute("data-context-name");
      var ctxBox = $("[data-form-context]", form);
      ctxBox.hidden = !ctx; $("[data-form-context-name]", form).textContent = ctx || "";
      $("[data-form-context-meta]", form).textContent = trigger.getAttribute("data-context-meta") || "";
      var thumb = $("[data-form-context-img]", form), thumbSrc = trigger.getAttribute("data-thumb");
      if (thumb) { thumb.hidden = !thumbSrc; if (thumbSrc) thumb.src = thumbSrc; }
      $("[data-similar-note]", form).hidden = kind !== "similar";
      var sampleNote = $("[data-sample-note]", form);
      if (sampleNote) sampleNote.hidden = kind !== "painting";
      $("[data-cert-fields]", form).hidden = kind !== "certificate";
      $$("[data-optional-field]", form).forEach(function (f) { f.hidden = kind === "certificate"; });
      modal.classList.toggle("has-context", !!ctx);
      var sizeField = $("[data-size-field]", form);
      if (sizeField) sizeField.hidden = kind === "certificate" || kind === "delivery" || kind === "question" || (kind === "painting" && status === "available");
      if (form._setSizes) {
        var raw = trigger.getAttribute("data-sizes");
        form._setSizes(raw ? JSON.parse(raw) : null);
        var picked = $("[data-page-size]");
        if (picked && picked.value && raw) form._selectSize(picked.value);
      }
      success.hidden = true; body.hidden = false;
      document.body.classList.add("modal-open");
      modal.showModal();
      var first = form.elements.name; if (first) setTimeout(function () { first.focus(); }, 30);
    };
    var close = function () { modal.close(); };
    modal.addEventListener("close", function () {
      document.body.classList.remove("modal-open");
      if (lastTrigger) lastTrigger.focus();
    });
    modal.addEventListener("click", function (e) { if (e.target === modal) close(); });
    $$("[data-modal-close]", modal).forEach(function (b) { b.addEventListener("click", close); });
    form.addEventListener("lead:sent", function (e) {
      body.hidden = true; success.hidden = false;
      $("[data-modal-success-text]", modal).textContent = e.detail.message || "";
      form.reset(); clearErrors(form);
      $("[data-field=idempotency_key]", form).value = uuid();
      success.focus();
    });
    document.addEventListener("click", function (e) {
      var t = e.target.closest("[data-order]");
      if (!t) return;
      e.preventDefault();
      open(t);
    });
  }

  /* ---------- Галерея картины и увеличение ---------- */
  var gallery = $("[data-gallery]");
  if (gallery) {
    var zoom = $("[data-zoom]", gallery);
    var mainImg = zoom && $("img", zoom);
    $$("[data-thumb]", gallery).forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (!mainImg) return;
        mainImg.removeAttribute("srcset");
        mainImg.src = btn.getAttribute("data-src");
        mainImg.alt = btn.getAttribute("data-alt");
        zoom.href = btn.getAttribute("data-full");
        $$("[data-thumb]", gallery).forEach(function (b) { b.classList.toggle("is-active", b === btn); });
        var idx = $("[data-gallery-index]", gallery); if (idx) idx.textContent = btn.getAttribute("data-index");
      });
    });
    var lb = $("[data-lightbox]");
    if (zoom && lb && typeof lb.showModal === "function") {
      zoom.addEventListener("click", function (e) {
        e.preventDefault();
        var img = $("[data-lightbox-img]", lb);
        img.src = zoom.href; img.alt = mainImg ? mainImg.alt : "";
        lb.showModal();
      });
      $("[data-lightbox-close]", lb).addEventListener("click", function () { lb.close(); });
      lb.addEventListener("click", function (e) { if (e.target === lb || e.target.tagName === "IMG") lb.close(); });
      lb.addEventListener("close", function () { zoom.focus(); });
    }
  }

  /* ---------- «Показать еще»: те же данные, что и на следующей странице списка ---------- */
  $$("[data-load-more]").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      if (!window.fetch) return;
      e.preventDefault();
      var grid = $(btn.getAttribute("data-target"));
      btn.setAttribute("aria-busy", "true");
      fetch(btn.href, { headers: { "X-Requested-With": "fetch" }, credentials: "same-origin" })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          var tmp = document.createElement("ul");
          tmp.innerHTML = data.html;
          var firstNew = tmp.firstElementChild;
          while (tmp.firstElementChild) grid.appendChild(tmp.firstElementChild);
          if (data.next) { btn.href = data.next; } else { btn.remove(); }
          var link = firstNew && $("a", firstNew); if (link) link.focus({ preventScroll: true });
        })
        .catch(function () { location.href = btn.href; })
        .then(function () { btn.removeAttribute("aria-busy"); });
    });
  });
})();
