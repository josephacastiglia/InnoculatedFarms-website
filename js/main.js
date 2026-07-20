/* ============================================================
   INNOCULATED FARMS — shared behaviors
   Reveals, header state, mobile nav, parallax, forms, toast.
   Zero dependencies. Respects prefers-reduced-motion.
   ============================================================ */
(function () {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Header scroll state ---------- */
  const header = document.querySelector(".header");
  if (header) {
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- Mobile nav ---------- */
  const navToggle = document.querySelector(".nav-toggle");
  if (navToggle) {
    navToggle.addEventListener("click", () => {
      const open = document.body.classList.toggle("nav-open");
      navToggle.setAttribute("aria-expanded", String(open));
    });
    document.querySelectorAll(".nav a").forEach((a) =>
      a.addEventListener("click", () => {
        document.body.classList.remove("nav-open");
        navToggle.setAttribute("aria-expanded", "false");
      })
    );
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) {
        document.body.classList.remove("nav-open");
        navToggle.setAttribute("aria-expanded", "false");
        navToggle.focus();
      }
    });
  }

  /* ---------- Offer bar (config-driven, sparing by design) ---------- */
  (function offerBar() {
    const cfg = window.IF_CONFIG || {};
    if (!cfg.OFFER_TEXT) return;
    let dismissed = false;
    try { dismissed = sessionStorage.getItem("if-offer-dismissed") === "1"; } catch (e) {}
    if (dismissed) return;
    const bar = document.createElement("div");
    bar.className = "offer-bar";
    bar.setAttribute("role", "status");
    const link = cfg.OFFER_LINK || "shop.html";
    bar.innerHTML =
      '<span></span>' +
      '<button class="offer-bar-close" type="button" aria-label="Dismiss offer">&times;</button>';
    const span = bar.querySelector("span");
    span.textContent = cfg.OFFER_TEXT;
    const a = document.createElement("a");
    a.href = link;
    a.textContent = "Shop now";
    bar.insertBefore(a, bar.querySelector(".offer-bar-close"));
    document.body.prepend(bar);
    document.body.classList.add("has-offer");
    bar.querySelector(".offer-bar-close").addEventListener("click", () => {
      bar.remove();
      document.body.classList.remove("has-offer");
      try { sessionStorage.setItem("if-offer-dismissed", "1"); } catch (e) {}
    });
  })();

  /* ---------- Reviews rail (renders from IF_REVIEWS in config.js) ---------- */
  (function reviewsRail() {
    const track = document.querySelector("[data-rev-track]");
    if (!track) return;
    const reviews = window.IF_REVIEWS || [];
    const STAR = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 5.9 6.6 1-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5-4.8-4.6 6.6-1z"/></svg>';
    track.innerHTML = reviews
      .map((r) => {
        const stars = STAR.repeat(Math.max(1, Math.min(5, r.stars || 5)));
        const src = r.source === "google" ? '<span class="rev-src">Google review</span>' : "";
        const div = document.createElement("div");
        div.textContent = r.text;
        const safeText = div.innerHTML;
        div.textContent = r.name || "";
        const safeName = div.innerHTML;
        return (
          '<article class="rev-card">' +
          '<div class="rev-stars" aria-label="' + (r.stars || 5) + ' out of 5 stars">' + stars + "</div>" +
          '<p class="rev-text">“' + safeText + '”</p>' +
          '<div class="rev-meta"><span class="rev-name">' + safeName + "</span>" + src + "</div>" +
          "</article>"
        );
      })
      .join("");

    const step = () => (track.querySelector(".rev-card") ? track.querySelector(".rev-card").offsetWidth + 20 : 380);
    const prev = document.querySelector("[data-rev-prev]");
    const next = document.querySelector("[data-rev-next]");
    if (prev) prev.addEventListener("click", () => track.scrollBy({ left: -step(), behavior: "smooth" }));
    if (next) next.addEventListener("click", () => track.scrollBy({ left: step(), behavior: "smooth" }));
  })();

  /* ---------- Rate-us modal (review gate) ----------
     5 stars → opens the Google write-a-review page.
     1–4 stars → private feedback form, handled like every other
     site form (Formspree-ready via data-if-form). */
  (function rateUs() {
    const cfg = window.IF_CONFIG || {};
    const STAR = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 5.9 6.6 1-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5-4.8-4.6 6.6-1z"/></svg>';

    const overlay = document.createElement("div");
    overlay.className = "rate-overlay";
    overlay.innerHTML = `
      <div class="rate-dialog" role="dialog" aria-modal="true" aria-labelledby="rate-title">
        <button class="rate-close" type="button" data-rate-close aria-label="Close">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
        <span class="wordmark" aria-hidden="true">
          <span class="wordmark-main"><span class="gilt">INNOCULATED</span></span>
          <span class="wordmark-sub">Farms · Est. 2020</span>
        </span>

        <div data-rate-step="stars">
          <p class="rate-title" id="rate-title">How would you rate us?</p>
          <p class="rate-sub">Tap a star — it takes ten seconds.</p>
          <div class="rate-stars" data-rate-stars>
            ${[1, 2, 3, 4, 5].map((n) => `<button type="button" data-star="${n}" aria-label="${n} star${n > 1 ? "s" : ""}">${STAR}</button>`).join("")}
          </div>
        </div>

        <div data-rate-step="feedback" hidden>
          <p class="rate-title">Help us make it right.</p>
          <p class="rate-sub">Tell us what fell short — this comes straight to the farm, privately.</p>
          <form class="rate-form" data-if-form data-success=".rate-form-success" novalidate>
            <input type="hidden" name="form-type" value="private-feedback">
            <input type="hidden" name="rating" value="" data-rate-rating>
            <div class="form-field">
              <label for="rate-name">Name</label>
              <input id="rate-name" name="name" type="text" autocomplete="name" required>
            </div>
            <div class="form-field">
              <label for="rate-email">Email</label>
              <input id="rate-email" name="email" type="email" autocomplete="email" required>
            </div>
            <div class="form-field">
              <label for="rate-feedback">Your feedback</label>
              <textarea id="rate-feedback" name="feedback" rows="4" required></textarea>
            </div>
            <button class="btn btn--gold" type="submit">Send Private Feedback</button>
          </form>
          <div class="form-success rate-form-success" role="status">
            <p class="rate-title">Thank you.</p>
            <p class="rate-sub">A member of the farm will read this personally — and we'll make it right.</p>
          </div>
        </div>

        <div data-rate-step="thanks" hidden>
          <p class="rate-title">You're the best. 5 stars right back.</p>
          <p class="rate-sub">We just opened our Google review page in a new tab — your few words there mean the world to a small farm.</p>
        </div>

        <p class="rate-note">Reviews help neighbors find real, farm-grown mushrooms.</p>
      </div>`;
    document.body.appendChild(overlay);

    const steps = {
      stars: overlay.querySelector('[data-rate-step="stars"]'),
      feedback: overlay.querySelector('[data-rate-step="feedback"]'),
      thanks: overlay.querySelector('[data-rate-step="thanks"]'),
    };
    const starBtns = Array.from(overlay.querySelectorAll("[data-star]"));

    function showStep(name) {
      Object.keys(steps).forEach((k) => { steps[k].hidden = k !== name; });
    }
    function openModal() {
      showStep("stars");
      starBtns.forEach((b) => b.classList.remove("is-lit"));
      document.body.classList.add("rate-open");
    }
    function closeModal() {
      document.body.classList.remove("rate-open");
    }

    document.addEventListener("click", (e) => {
      if (e.target.closest("[data-rate-us]")) { e.preventDefault(); openModal(); }
      if (e.target.closest("[data-rate-close]")) closeModal();
      if (e.target === overlay) closeModal();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && document.body.classList.contains("rate-open")) closeModal();
    });

    // hover/focus preview fill
    starBtns.forEach((btn, i) => {
      const lit = (n) => starBtns.forEach((b, j) => b.classList.toggle("is-lit", j < n));
      btn.addEventListener("mouseenter", () => lit(i + 1));
      btn.addEventListener("focus", () => lit(i + 1));
      btn.addEventListener("click", () => {
        const rating = i + 1;
        if (rating === 5) {
          showStep("thanks");
          window.open(cfg.GOOGLE_REVIEW_URL || "https://www.google.com/maps", "_blank", "noopener");
        } else {
          const hidden = overlay.querySelector("[data-rate-rating]");
          if (hidden) hidden.value = String(rating);
          showStep("feedback");
        }
      });
    });
    overlay.querySelector("[data-rate-stars]").addEventListener("mouseleave", () => {
      starBtns.forEach((b) => b.classList.remove("is-lit"));
    });
  })();

  /* ---------- Scroll reveals ---------- */
  const revealEls = document.querySelectorAll(".reveal");
  if (revealEls.length && "IntersectionObserver" in window && !reduceMotion) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  }

  /* ---------- Hero parallax (mycelium drift) ---------- */
  const mycelium = document.querySelector(".hero-mycelium");
  if (mycelium && !reduceMotion) {
    let ticking = false;
    window.addEventListener(
      "scroll",
      () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
          const y = Math.min(window.scrollY, window.innerHeight);
          mycelium.style.transform = `translateY(${y * 0.18}px)`;
          ticking = false;
        });
      },
      { passive: true }
    );
  }

  /* ---------- Toast ---------- */
  let toastTimer = null;
  window.ifToast = function (message) {
    let toast = document.querySelector(".toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.className = "toast";
      toast.setAttribute("role", "status");
      toast.setAttribute("aria-live", "polite");
      toast.innerHTML =
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg><span></span>';
      document.body.appendChild(toast);
    }
    toast.querySelector("span").textContent = message;
    toast.classList.add("is-visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("is-visible"), 4000);
  };

  /* ---------- Forms (Formspree-ready with local success fallback) ---------- */
  document.querySelectorAll("form[data-if-form]").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      // Simple required validation with inline errors
      let firstInvalid = null;
      form.querySelectorAll("[required]").forEach((input) => {
        const field = input.closest(".form-field");
        const valid = input.checkValidity();
        if (field) field.classList.toggle("has-error", !valid);
        if (!valid && !firstInvalid) firstInvalid = input;
      });
      if (firstInvalid) {
        firstInvalid.focus();
        return;
      }

      const btn = form.querySelector('button[type="submit"]');
      const btnText = btn ? btn.textContent : "";
      if (btn) {
        btn.disabled = true;
        btn.textContent = "Sending…";
      }

      const endpoint = (window.IF_CONFIG && window.IF_CONFIG.FORM_ENDPOINT) || "";
      const isLive = /^https?:\/\//.test(endpoint);

      try {
        if (isLive) {
          const res = await fetch(endpoint, {
            method: "POST",
            headers: { Accept: "application/json" },
            body: new FormData(form),
          });
          if (!res.ok) throw new Error("Form service returned " + res.status);
        } else {
          // Demo mode: no endpoint configured yet
          await new Promise((r) => setTimeout(r, 700));
        }
        const success = document.querySelector(form.dataset.success || ".form-success");
        if (success) {
          form.hidden = true;
          success.classList.add("is-visible");
          success.setAttribute("tabindex", "-1");
          success.focus({ preventScroll: false });
        }
      } catch (err) {
        window.ifToast("Something went wrong — please email us directly.");
        if (btn) {
          btn.disabled = false;
          btn.textContent = btnText;
        }
      }
    });

    // Clear error state as the user types
    form.querySelectorAll("input, select, textarea").forEach((input) => {
      input.addEventListener("input", () => {
        const field = input.closest(".form-field");
        if (field) field.classList.remove("has-error");
      });
    });
  });

  /* ---------- Story video plate ----------
     Lazy-loads the grow-room film only when its plate scrolls near the
     viewport, autoplays muted while in view (paused when scrolled away
     to save CPU/battery), and always leaves a manual play/pause toggle.
     Under prefers-reduced-motion it loads but never autoplays — the
     visitor has to choose to press play. */
  document.querySelectorAll("[data-video-plate]").forEach((plate) => {
    const video = plate.querySelector(".plate-video-el");
    const source = video && video.querySelector("source[data-src]");
    const toggle = plate.querySelector("[data-video-toggle]");
    if (!video || !source) return;

    let loaded = false;
    let userPaused = false;

    function load() {
      if (loaded) return;
      loaded = true;
      source.src = source.dataset.src;
      video.load();
    }

    function play() {
      load();
      video.play().catch(() => {});
    }

    function pause() {
      video.pause();
    }

    video.addEventListener("canplay", () => plate.classList.add("is-ready"));
    video.addEventListener("play", () => {
      plate.classList.add("is-playing");
      toggle.setAttribute("aria-pressed", "true");
    });
    video.addEventListener("pause", () => {
      plate.classList.remove("is-playing");
      toggle.setAttribute("aria-pressed", "false");
    });

    if (toggle) {
      toggle.addEventListener("click", () => {
        if (video.paused) {
          userPaused = false;
          play();
        } else {
          userPaused = true;
          pause();
        }
      });
    }

    if ("IntersectionObserver" in window) {
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              load();
              if (!reduceMotion && !userPaused) play();
            } else if (!video.paused) {
              pause();
            }
          });
        },
        { threshold: 0.4 }
      );
      io.observe(plate);
    } else {
      load();
    }
  });

  /* ---------- Cursor micro-interactions ----------
     Mouse-only (fine pointer + hover), skipped under reduced motion.
     One rAF loop drives a lagging ring and three trailing gold-dust motes,
     echoing the ambient .dust already used in the hero; the ring swells
     over interactive elements. Loop sleeps at rest — zero idle CPU. */

  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  (function cursorTrail() {
    if (reduceMotion || !finePointer) return;

    const layer = document.createElement("div");
    layer.className = "cursor-layer";
    layer.setAttribute("aria-hidden", "true");

    const ring = document.createElement("div");
    ring.className = "cursor-ring";
    layer.appendChild(ring);

    const motes = [
      { size: 5, lerp: 0.3, o: 0.55 },
      { size: 4, lerp: 0.16, o: 0.4 },
      { size: 3, lerp: 0.09, o: 0.25 },
    ].map((spec) => {
      const el = document.createElement("div");
      el.className = "cursor-dust";
      el.style.width = spec.size + "px";
      el.style.height = spec.size + "px";
      el.style.margin = -spec.size / 2 + "px 0 0 " + -spec.size / 2 + "px";
      el.style.setProperty("--o", spec.o);
      layer.appendChild(el);
      return { el, x: window.innerWidth / 2, y: window.innerHeight / 2, lerp: spec.lerp };
    });

    document.body.appendChild(layer);

    let tx = window.innerWidth / 2, ty = window.innerHeight / 2;
    let rx = tx, ry = ty;
    let scale = 1, targetScale = 1;
    let running = false;

    function loop() {
      let settled =
        Math.abs(tx - rx) < 0.15 && Math.abs(ty - ry) < 0.15 &&
        Math.abs(targetScale - scale) < 0.002;

      rx += (tx - rx) * 0.22;
      ry += (ty - ry) * 0.22;
      scale += (targetScale - scale) * 0.14;
      ring.style.transform = `translate3d(${rx.toFixed(1)}px,${ry.toFixed(1)}px,0) scale(${scale.toFixed(3)})`;

      motes.forEach((m) => {
        settled = settled && Math.abs(tx - m.x) < 0.15 && Math.abs(ty - m.y) < 0.15;
        m.x += (tx - m.x) * m.lerp;
        m.y += (ty - m.y) * m.lerp;
        m.el.style.transform = `translate3d(${m.x.toFixed(1)}px,${m.y.toFixed(1)}px,0)`;
      });

      if (settled) { running = false; return; }
      requestAnimationFrame(loop);
    }

    function wake() {
      if (!running) {
        running = true;
        requestAnimationFrame(loop);
      }
    }

    document.addEventListener("pointermove", (e) => {
      if (e.pointerType && e.pointerType !== "mouse") return;
      tx = e.clientX;
      ty = e.clientY;
      layer.classList.add("is-visible");
      wake();
    }, { passive: true });

    document.documentElement.addEventListener("mouseleave", () => {
      layer.classList.remove("is-visible");
    });

    document.addEventListener("pointerover", (e) => {
      targetScale = e.target.closest("a, button, input, select, textarea, label, .variety-card") ? 1.7 : 1;
      wake();
    }, { passive: true });
  })();

  /* ---------- Magnetic buttons ---------- */

  (function magneticButtons() {
    if (reduceMotion || !finePointer) return;
    document.querySelectorAll(".btn, .add-btn").forEach((btn) => {
      btn.classList.add("is-magnetic");
      btn.addEventListener("pointermove", (e) => {
        if (e.pointerType && e.pointerType !== "mouse") return;
        const r = btn.getBoundingClientRect();
        const mx = (e.clientX - r.left - r.width / 2) / (r.width / 2);
        const my = (e.clientY - r.top - r.height / 2) / (r.height / 2);
        btn.style.transform = `translate3d(${(mx * 5).toFixed(1)}px,${(my * 4).toFixed(1)}px,0)`;
      });
      btn.addEventListener("pointerleave", () => {
        btn.style.transform = "";
      });
    });
  })();

  /* ---------- Cursor spotlight on dark surfaces ---------- */

  (function spotlight() {
    if (reduceMotion || !finePointer) return;
    document.querySelectorAll(".product-card, .variety-card, .step, .benefit").forEach((card) => {
      card.classList.add("spotlight");
      card.addEventListener("pointermove", (e) => {
        if (e.pointerType && e.pointerType !== "mouse") return;
        const r = card.getBoundingClientRect();
        card.style.setProperty("--mx", ((e.clientX - r.left) / r.width * 100).toFixed(1) + "%");
        card.style.setProperty("--my", ((e.clientY - r.top) / r.height * 100).toFixed(1) + "%");
      });
    });
  })();

  /* ---------- Footer year ---------- */
  document.querySelectorAll("[data-year]").forEach((el) => {
    el.textContent = new Date().getFullYear();
  });
})();
