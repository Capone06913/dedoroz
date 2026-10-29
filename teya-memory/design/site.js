(function () {
  var scene = document.querySelector("[data-scene]");
  var track = document.querySelector("[data-hero-track]");
  var topbar = document.getElementById("topbar");
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var look = "show";
  var timer = 0;
  var heroVideo = document.querySelector(".scene-video");
  if (heroVideo && reduced) {
    heroVideo.removeAttribute("autoplay");
    heroVideo.pause();
  }

  function photos() {
    if (!scene) return [];
    return Array.prototype.filter.call(scene.querySelectorAll(".scene-photo"), function (img) {
      var set = img.getAttribute("data-set");
      return !set || set === look;
    });
  }
  function showAt(list, index) {
    scene.querySelectorAll(".scene-photo").forEach(function (img) { img.classList.remove("is-on"); });
    if (list[index]) list[index].classList.add("is-on");
  }
  function startCycle() {
    window.clearInterval(timer);
    if (!scene) return;
    var list = photos();
    var i = 0;
    showAt(list, 0);
    if (reduced || list.length < 2 || scene.classList.contains("page-hero")) return;
    timer = window.setInterval(function () {
      i = (i + 1) % list.length;
      showAt(list, i);
    }, 4200);
  }
  var showBtn = document.getElementById("mode-show");
  var classicBtn = document.getElementById("mode-classic");
  if (showBtn && classicBtn) {
    showBtn.addEventListener("click", function () {
      look = "show";
      showBtn.setAttribute("aria-checked", "true");
      classicBtn.setAttribute("aria-checked", "false");
      var line = document.getElementById("one-line");
      if (line) line.textContent = "Пайетки. Зал на секунду стихает.";
      startCycle();
    });
    classicBtn.addEventListener("click", function () {
      look = "classic";
      classicBtn.setAttribute("aria-checked", "true");
      showBtn.setAttribute("aria-checked", "false");
      var line = document.getElementById("one-line");
      if (line) line.textContent = "Классика. Образ собран по детали.";
      startCycle();
    });
  }
  startCycle();

  var reel = document.querySelector("[data-reel]");
  var reelTrack = document.querySelector("[data-reel-track]");
  function onScroll() {
    if (topbar) topbar.classList.toggle("is-solid", window.scrollY > 40);
    if (scene && track) {
      var rect = track.getBoundingClientRect();
      var total = track.offsetHeight - window.innerHeight;
      var passed = Math.min(Math.max(-rect.top, 0), total);
      scene.style.setProperty("--p", total ? (passed / total).toFixed(4) : "0");
    }
    if (!reduced && reel && reelTrack) {
      var r = reel.getBoundingClientRect();
      var span = reel.offsetHeight - window.innerHeight;
      var rp = span ? Math.min(Math.max(-r.top, 0), span) / span : 0;
      var max = Math.max(reelTrack.scrollWidth - reel.clientWidth, 0);
      reelTrack.style.transform = "translate3d(" + (-rp * max) + "px,0,0)";
    }
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);

  var navToggle = document.getElementById("nav-toggle");
  var menu = document.getElementById("menu");
  if (navToggle && menu) {
    navToggle.addEventListener("click", function () {
      var open = navToggle.getAttribute("aria-expanded") !== "true";
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
      menu.classList.toggle("is-open", open);
      navToggle.textContent = open ? "Закрыть" : "Меню";
    });
  }

  var carousel = document.getElementById("gallery-carousel");
  var galleryTrack = document.getElementById("gallery-track");
  var slidesNode = document.getElementById("gallery-slides");
  var lightbox = document.getElementById("gallery-lightbox");
  var lightboxImg = document.getElementById("gallery-lightbox-img");
  var lightboxCaption = document.getElementById("gallery-lightbox-caption");
  var lightboxClose = document.getElementById("gallery-lightbox-close");
  var lightboxPrev = document.getElementById("gallery-lightbox-prev");
  var lightboxNext = document.getElementById("gallery-lightbox-next");
  var lightboxBackdrop = document.getElementById("gallery-lightbox-backdrop");

  if (carousel && galleryTrack && slidesNode && lightbox && lightboxImg) {
    var slides = JSON.parse(slidesNode.textContent);
    var index = 0;
    var pos = 1;
    var open = false;
    var dragging = false;
    var moved = false;
    var dragX = 0;
    var dragOrigin = 0;
    var pressButton = null;
    var swipeX = 0;
    var autoTimer = 0;

    function makeSlide(slide, i, clone) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "carousel-slide";
      button.dataset.index = String(i);
      if (clone) {
        button.setAttribute("aria-hidden", "true");
        button.tabIndex = -1;
      } else {
        button.setAttribute("aria-label", "Открыть фото. " + slide.alt);
      }
      var img = document.createElement("img");
      img.src = slide.src;
      img.alt = clone ? "" : slide.alt;
      img.draggable = false;
      button.appendChild(img);
      return button;
    }

    if (slides.length) {
      galleryTrack.appendChild(makeSlide(slides[slides.length - 1], slides.length - 1, true));
      slides.forEach(function (slide, i) {
        galleryTrack.appendChild(makeSlide(slide, i, false));
      });
      galleryTrack.appendChild(makeSlide(slides[0], 0, true));
    }

    function metrics() {
      var view = carousel.clientWidth;
      var gap = 14;
      var w = Math.round(view * (view < 700 ? 0.76 : 0.48));
      return { w: w, gap: gap, view: view };
    }

    function xFor(at) {
      var m = metrics();
      return (m.view - m.w) / 2 - at * (m.w + m.gap);
    }

    function place(animate) {
      var m = metrics();
      var buttons = galleryTrack.children;
      for (var i = 0; i < buttons.length; i++) {
        buttons[i].style.flexBasis = m.w + "px";
        buttons[i].style.width = m.w + "px";
      }
      galleryTrack.style.transition = animate && !reduced ? "transform .7s cubic-bezier(.22,.61,.36,1)" : "none";
      galleryTrack.style.transform = "translate3d(" + xFor(pos) + "px,0,0)";
    }

    function realIndex() {
      return (pos - 1 + slides.length) % slides.length;
    }

    function render() {
      var slide = slides[index];
      if (!slide) return;
      lightboxImg.src = slide.src;
      lightboxImg.alt = slide.alt;
      if (lightboxCaption) lightboxCaption.textContent = slide.caption;
    }

    function arm(soon) {
      window.clearTimeout(autoTimer);
      if (reduced || open || slides.length < 2) return;
      autoTimer = window.setTimeout(function tick() {
        go(1);
        autoTimer = window.setTimeout(tick, 3200);
      }, soon ? 450 : 3200);
    }

    function go(dir) {
      pos += dir;
      index = realIndex();
      place(true);
    }

    function openAt(i) {
      index = (i + slides.length) % slides.length;
      open = true;
      window.clearTimeout(autoTimer);
      lightbox.removeAttribute("hidden");
      document.body.classList.add("gallery-lightbox-open");
      render();
      if (lightboxClose) lightboxClose.focus();
    }

    function close() {
      open = false;
      lightbox.setAttribute("hidden", "");
      document.body.classList.remove("gallery-lightbox-open");
      arm();
    }

    function step(dir) {
      index = (index + dir + slides.length) % slides.length;
      render();
    }

    galleryTrack.addEventListener("transitionend", function (event) {
      if (event.target !== galleryTrack || event.propertyName !== "transform") return;
      var before = pos;
      while (pos < 1) pos += slides.length;
      while (pos > slides.length) pos -= slides.length;
      if (pos === before) return;
      place(false);
    });

    carousel.addEventListener("pointerdown", function (event) {
      if (event.pointerType === "mouse" && event.button !== 0) return;
      dragging = true;
      moved = false;
      dragX = event.clientX;
      dragOrigin = xFor(pos);
      pressButton = event.target.closest(".carousel-slide");
      galleryTrack.style.transition = "none";
      carousel.classList.add("is-dragging");
      window.clearTimeout(autoTimer);
      carousel.setPointerCapture(event.pointerId);
    });
    carousel.addEventListener("pointermove", function (event) {
      if (!dragging) return;
      var dx = event.clientX - dragX;
      if (Math.abs(dx) > 8) moved = true;
      galleryTrack.style.transform = "translate3d(" + (dragOrigin + dx) + "px,0,0)";
    });
    function endDrag(event) {
      if (!dragging) return;
      dragging = false;
      carousel.classList.remove("is-dragging");
      var dx = event.clientX - dragX;
      if (dx <= -48) go(1);
      else if (dx >= 48) go(-1);
      else place(true);
      arm();
    }
    carousel.addEventListener("pointerup", endDrag);
    carousel.addEventListener("pointercancel", function () {
      dragging = false;
      carousel.classList.remove("is-dragging");
      place(true);
      arm();
    });
    carousel.addEventListener("click", function (event) {
      if (moved) {
        moved = false;
        event.preventDefault();
        return;
      }
      var button = event.target.closest(".carousel-slide") || pressButton;
      if (!button) return;
      openAt(Number(button.dataset.index));
    });

    if (lightboxClose) lightboxClose.addEventListener("click", close);
    if (lightboxBackdrop) lightboxBackdrop.addEventListener("click", close);
    if (lightboxPrev) lightboxPrev.addEventListener("click", function () { step(-1); });
    if (lightboxNext) lightboxNext.addEventListener("click", function () { step(1); });

    lightbox.addEventListener("pointerdown", function (event) {
      if (event.target.closest("button")) return;
      swipeX = event.clientX;
    });
    lightbox.addEventListener("pointerup", function (event) {
      if (event.target.closest("button")) return;
      var dx = event.clientX - swipeX;
      if (dx > 48) step(-1);
      else if (dx < -48) step(1);
    });
    document.addEventListener("keydown", function (event) {
      if (!open) return;
      if (event.key === "Escape") close();
      if (event.key === "ArrowLeft") step(-1);
      if (event.key === "ArrowRight") step(1);
    });
    window.addEventListener("resize", function () { place(false); });

    place(false);
    arm(true);
  }


  var lead = document.getElementById("lead");
  if (lead) {
    lead.addEventListener("submit", function (event) {
      event.preventDefault();
      var data = new FormData(event.target);
      var lines = [
        "Имя: " + data.get("name"),
        "Телефон: " + data.get("phone"),
        "Дата: " + data.get("date")
      ];
      if (data.get("venue")) lines.push("Зал: " + data.get("venue"));
      if (data.get("format")) lines.push("Формат: " + data.get("format"));
      if (data.get("msg")) lines.push("Сообщение: " + data.get("msg"));
      var note = document.getElementById("form-note");
      if (note) note.textContent = "Открываю письмо на ded.moroz.nnovgorod@yandex.ru";
      window.location.href = "mailto:ded.moroz.nnovgorod@yandex.ru?subject=" +
        encodeURIComponent("Заявка на Деда Мороза и Снегурочку") +
        "&body=" + encodeURIComponent(lines.join("\n"));
    });
  }

  var arrival = document.getElementById("arrival");
  if (arrival) {
    document.body.classList.add("arrival-open");
    var hero = document.querySelector(".scene-video");
    var closed = false;
    function openSite() {
      if (closed) return;
      closed = true;
      if (hero) {
        try { hero.currentTime = 0; } catch (err) {}
        var play = hero.play();
        if (play && play.catch) play.catch(function () {});
      }
      arrival.classList.add("is-gone");
      document.body.classList.remove("arrival-open");
      window.setTimeout(function () {
        if (arrival.parentNode) arrival.parentNode.removeChild(arrival);
      }, 700);
    }
    if (hero) {
      hero.pause();
      if (hero.readyState >= 3) openSite();
      else hero.addEventListener("canplay", openSite, { once: true });
    }
    window.addEventListener("load", function () {
      if (!hero || hero.readyState >= 3) openSite();
    });
    window.setTimeout(openSite, 12000);
  }

  var faq = document.querySelector(".faq");
  if (faq) {
    faq.addEventListener("toggle", function (event) {
      var item = event.target;
      if (!item || item.tagName !== "DETAILS" || !item.open) return;
      Array.prototype.forEach.call(faq.querySelectorAll("details"), function (other) {
        if (other !== item) other.open = false;
      });
    }, true);
  }
})();
