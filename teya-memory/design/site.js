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

/* Бодрая Jingle Bells, мелодия народная. Запись ролика Coca-Cola сюда не входит. */
(function () {
  var KEY = "dedmoroz-ny-music";
  var LEVEL = 0.4;
  var Q = 0.42;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var ctx = null;
  var master = null;
  var bus = null;
  var noise = null;
  var generation = 0;
  var timer = 0;
  var playing = false;
  var score = null;
  var button = document.createElement("button");

  button.type = "button";
  button.className = "ny-music";
  button.innerHTML = "<span aria-hidden=\"true\">♫</span>";
  document.body.appendChild(button);

  function pref() {
    try { return localStorage.getItem(KEY); } catch (err) { return null; }
  }
  function save(value) {
    try { localStorage.setItem(KEY, value); } catch (err) {}
  }
  function paint() {
    button.classList.toggle("is-on", playing);
    button.setAttribute("aria-pressed", playing ? "true" : "false");
    button.setAttribute("aria-label", playing ? "Выключить тихую праздничную музыку" : "Включить тихую праздничную музыку");
    button.title = playing ? "Выключить музыку" : "Тихая праздничная музыка";
  }
  function ensure() {
    if (ctx) return;
    var AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    ctx = new AudioCtx();
    master = ctx.createGain();
    master.gain.value = 0.0001;
    var warm = ctx.createBiquadFilter();
    warm.type = "lowpass";
    warm.frequency.value = 7400;
    master.connect(warm);
    warm.connect(ctx.destination);
    var length = ctx.sampleRate;
    noise = ctx.createBuffer(1, length, ctx.sampleRate);
    var data = noise.getChannelData(0);
    for (var i = 0; i < length; i++) data[i] = Math.random() * 2 - 1;
  }
  function blip(time, freq, dur, amount, type) {
    var osc = ctx.createOscillator();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, time);
    var g = ctx.createGain();
    var rel = Math.min(Math.max(dur * 0.82, 0.07), 0.62);
    g.gain.setValueAtTime(0.0001, time);
    g.gain.exponentialRampToValueAtTime(amount, time + 0.008);
    g.gain.exponentialRampToValueAtTime(0.0001, time + rel);
    osc.connect(g);
    g.connect(bus);
    osc.start(time);
    osc.stop(time + rel + 0.02);
  }
  function sleigh(time, accent) {
    var amount = accent ? 0.07 : 0.035;
    var src = ctx.createBufferSource();
    src.buffer = noise;
    var bp = ctx.createBiquadFilter();
    bp.type = "bandpass";
    bp.frequency.setValueAtTime(accent ? 5400 : 3600, time);
    bp.Q.value = 0.8;
    var g = ctx.createGain();
    g.gain.setValueAtTime(0.0001, time);
    g.gain.exponentialRampToValueAtTime(amount, time + 0.003);
    g.gain.exponentialRampToValueAtTime(0.0001, time + 0.04);
    src.connect(bp);
    bp.connect(g);
    g.connect(bus);
    src.start(time);
    src.stop(time + 0.05);
  }
  function chordOf(name) {
    if (name === "F") return { bass: 174.61, notes: [349.23, 440, 523.25] };
    if (name === "G") return { bass: 196, notes: [392, 493.88, 587.33] };
    return { bass: 130.81, notes: [261.63, 329.63, 392] };
  }
  function buildScore() {
    var tune = [
      [329.63, 1], [329.63, 1], [329.63, 2],
      [329.63, 1], [329.63, 1], [329.63, 2],
      [329.63, 1], [392, 1], [523.25, 1], [587.33, 1],
      [329.63, 4],
      [349.23, 1], [349.23, 1], [349.23, 1], [349.23, 1],
      [349.23, 1], [329.63, 1], [329.63, 1], [329.63, 1],
      [329.63, 1], [293.66, 1], [293.66, 1], [329.63, 1],
      [293.66, 2], [392, 2],
      [329.63, 1], [329.63, 1], [329.63, 2],
      [329.63, 1], [329.63, 1], [329.63, 2],
      [329.63, 1], [392, 1], [523.25, 1], [587.33, 1],
      [329.63, 4],
      [349.23, 1], [349.23, 1], [349.23, 1], [349.23, 1],
      [349.23, 1], [329.63, 1], [329.63, 2],
      [392, 1], [392, 1], [349.23, 1], [293.66, 1],
      [261.63, 4]
    ];
    var bars = ["C", "C", "C", "C", "F", "C", "G", "G", "C", "C", "C", "C", "F", "C", "G", "C"];
    var events = [];
    var t = 0;
    var quarters = 0;
    tune.forEach(function (note) {
      events.push({ t: t, kind: "mel", f: note[0], dur: note[1] * Q });
      t += note[1] * Q;
      quarters += note[1];
    });
    var eighth = Q / 2;
    for (var time = 0; time < t - 0.02; time += eighth) {
      events.push({ t: time, kind: "bell", accent: Math.round(time / eighth) % 2 === 0 });
    }
    for (var q = 0; q < quarters; q++) {
      var bar = bars[Math.floor(q / 4)] || "C";
      if (q % 4 === 0) events.push({ t: q * Q, kind: "bass", chord: bar });
      if (q % 4 === 2) events.push({ t: q * Q, kind: "stab", chord: bar });
    }
    events.sort(function (a, b) { return a.t - b.t; });
    return { events: events, total: t };
  }
  function playEvent(ev, time) {
    if (ev.kind === "bell") {
      sleigh(time, ev.accent);
      return;
    }
    if (ev.kind === "mel") {
      blip(time, ev.f * 2, ev.dur, 0.12, "triangle");
      blip(time, ev.f * 4, ev.dur * 0.45, 0.035, "sine");
      return;
    }
    var chord = chordOf(ev.chord);
    if (ev.kind === "bass") {
      blip(time, chord.bass, Q * 0.85, 0.09, "sine");
      return;
    }
    chord.notes.forEach(function (freq) {
      blip(time, freq, Q * 0.4, 0.03, "triangle");
    });
  }
  function schedule(id, loopStart, index) {
    if (id !== generation || !playing) return;
    if (!score) score = buildScore();
    var now = ctx.currentTime;
    var horizon = now + 0.55;
    var guard = 0;
    while (guard < 6) {
      guard += 1;
      while (index < score.events.length && loopStart + score.events[index].t < horizon) {
        var at = loopStart + score.events[index].t;
        if (at > now) playEvent(score.events[index], at);
        index += 1;
      }
      if (index < score.events.length) break;
      loopStart += score.total;
      index = 0;
      if (loopStart > horizon) break;
    }
    timer = window.setTimeout(function () { schedule(id, loopStart, index); }, 160);
  }
  function start() {
    ensure();
    if (!ctx || playing) return;
    playing = true;
    generation += 1;
    var id = generation;
    bus = ctx.createGain();
    bus.gain.value = 1;
    bus.connect(master);
    master.gain.cancelScheduledValues(ctx.currentTime);
    master.gain.setValueAtTime(Math.max(master.gain.value, 0.0001), ctx.currentTime);
    master.gain.linearRampToValueAtTime(LEVEL, ctx.currentTime + 0.35);
    var resume = ctx.resume();
    if (resume && resume.catch) resume.catch(function () {});
    schedule(id, ctx.currentTime + 0.06, 0);
    save("on");
    paint();
  }
  function stop() {
    playing = false;
    generation += 1;
    window.clearTimeout(timer);
    if (ctx && master) {
      master.gain.cancelScheduledValues(ctx.currentTime);
      master.gain.setTargetAtTime(0.0001, ctx.currentTime, 0.12);
    }
    if (bus) {
      var old = bus;
      window.setTimeout(function () { try { old.disconnect(); } catch (err) {} }, 700);
      bus = null;
    }
    save("off");
    paint();
  }
  button.addEventListener("click", function (event) {
    event.stopPropagation();
    if (playing) stop();
    else start();
  });
  function gesture(event) {
    if (event.target && event.target.closest && event.target.closest(".ny-music")) return;
    if (pref() === "off") return;
    start();
  }
  if (!reduced && pref() !== "off") {
    document.addEventListener("pointerdown", gesture);
    document.addEventListener("keydown", gesture);
    window.addEventListener("load", function () {
      ensure();
      if (!ctx || pref() !== "on") return;
      ctx.resume().then(function () {
        if (ctx.state === "running") start();
      }).catch(function () {});
    });
  }
  paint();
})();
