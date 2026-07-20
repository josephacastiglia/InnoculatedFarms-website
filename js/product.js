/* ============================================================
   INNOCULATED FARMS — product page behavior
   Gallery slide swap, quantity selector (feeds data-item-quantity
   so it works in both demo-cart and Snipcart mode), sticky buy bar.
   ============================================================ */
(function () {
  "use strict";

  /* ---------- Gallery ---------- */
  const slides = document.querySelectorAll(".pdp-slide");
  const thumbs = document.querySelectorAll(".pdp-thumb");

  if (thumbs.length) {
    thumbs.forEach((thumb) => {
      thumb.addEventListener("click", () => {
        const i = thumb.dataset.thumb;
        slides.forEach((s) => {
          const active = s.dataset.slide === i;
          s.classList.toggle("is-active", active);
          if (active) {
            const img = s.querySelector("img[loading='lazy']");
            if (img) img.loading = "eager";
          }
        });
        thumbs.forEach((t) => t.classList.toggle("is-active", t === thumb));
      });
    });
  }

  /* ---------- Quantity ---------- */
  const qtyOut = document.querySelector("[data-qty-out]");
  const mainAdd = document.querySelector("[data-main-add]");
  const stickyAdd = document.querySelector("[data-sticky-add]");
  const lineTotal = document.querySelector("[data-line-total]");

  if (qtyOut && mainAdd) {
    const unitPrice = parseFloat(mainAdd.dataset.itemPrice);
    let qty = 1;

    const money = (n) => {
      const s = n.toLocaleString("en-US", { style: "currency", currency: "USD" });
      return s.endsWith(".00") ? s.slice(0, -3) : s;
    };

    function syncQty() {
      qtyOut.textContent = String(qty);
      mainAdd.dataset.itemQuantity = String(qty);
      if (stickyAdd) stickyAdd.dataset.itemQuantity = String(qty);
      if (lineTotal) lineTotal.textContent = money(unitPrice * qty);
    }

    document.querySelectorAll("[data-qty-step]").forEach((btn) => {
      btn.addEventListener("click", () => {
        qty = Math.min(20, Math.max(1, qty + parseInt(btn.dataset.qtyStep, 10)));
        syncQty();
      });
    });

    // After an add, reset to 1 so a second click doesn't silently double up
    [mainAdd, stickyAdd].forEach((btn) => {
      if (!btn) return;
      btn.addEventListener("click", () => {
        qty = 1;
        setTimeout(syncQty, 0);
      });
    });

    syncQty();
  }

  /* ---------- Frequently bought together ----------
     "Add Both" clicks this product's add button (at qty 1) plus the
     paired product's button down in the cross-sell grid — so it works
     identically in demo-cart and Snipcart mode. */
  (function fbt() {
    const btn = document.querySelector("[data-fbt-pair]");
    if (!btn || !mainAdd) return;
    btn.addEventListener("click", () => {
      const pairBtn = document.querySelector(
        '.shop-grid--pairs .snipcart-add-item[data-item-id="' + btn.dataset.fbtPair + '"]'
      );
      const prevQty = mainAdd.dataset.itemQuantity;
      mainAdd.dataset.itemQuantity = "1";
      mainAdd.click();
      mainAdd.dataset.itemQuantity = prevQty;
      if (pairBtn) setTimeout(() => pairBtn.click(), 60);
    });
  })();

  /* ---------- Sticky buy bar ----------
     Appears the moment the main Add button scrolls off the top,
     not when the whole (tall) panel does. */
  const stickyBar = document.querySelector("[data-sticky-buy]");

  if (stickyBar && mainAdd && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const above = entry.boundingClientRect.bottom < 90;
          const show = !entry.isIntersecting && above;
          stickyBar.classList.toggle("is-visible", show);
          stickyBar.setAttribute("aria-hidden", String(!show));
        });
      },
      { rootMargin: "-90px 0px 0px 0px" }
    );
    io.observe(mainAdd);
  }
})();
