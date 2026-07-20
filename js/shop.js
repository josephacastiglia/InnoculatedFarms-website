/* ============================================================
   INNOCULATED FARMS — commerce
   Snipcart-ready: when a real public API key is set in
   js/config.js, Snipcart is loaded and its cart takes over the
   same buttons (they already carry full Snipcart data-attrs).
   Until then, a local demo cart drawer handles the experience.
   ============================================================ */
(function () {
  "use strict";

  const cfg = window.IF_CONFIG || {};
  const keyIsLive =
    cfg.SNIPCART_API_KEY &&
    !/YOUR_SNIPCART/i.test(cfg.SNIPCART_API_KEY) &&
    cfg.SNIPCART_API_KEY.length > 20;

  /* ============================================
     LIVE MODE — load Snipcart
     ============================================ */
  if (keyIsLive) {
    document.documentElement.classList.add("snipcart-live");

    const container = document.createElement("div");
    container.hidden = true;
    container.id = "snipcart";
    container.dataset.apiKey = cfg.SNIPCART_API_KEY;
    container.dataset.configModalStyle = "side";
    container.dataset.currency = cfg.CURRENCY || "usd";
    document.body.appendChild(container);

    const css = document.createElement("link");
    css.rel = "stylesheet";
    css.href = "https://cdn.snipcart.com/themes/v3.7.1/default/snipcart.css";
    document.head.appendChild(css);

    const js = document.createElement("script");
    js.src = "https://cdn.snipcart.com/themes/v3.7.1/default/snipcart.js";
    js.async = true;
    document.head.appendChild(js);

    // Header cart button opens Snipcart; count stays in sync
    document.querySelectorAll("[data-cart-open]").forEach((btn) => {
      btn.classList.add("snipcart-checkout");
    });
    document.addEventListener("snipcart.ready", () => {
      window.Snipcart.store.subscribe(() => {
        const count = window.Snipcart.store.getState().cart.items.count;
        updateCountBadges(count);
      });
    });
    return; // Snipcart handles .snipcart-add-item clicks natively
  }

  /* ============================================
     DEMO MODE — local cart drawer
     ============================================ */
  const STORAGE_KEY = "if-cart-v1";
  let cart = [];
  try {
    cart = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch (e) {
    cart = [];
  }

  const money = (n) =>
    n.toLocaleString("en-US", { style: "currency", currency: "USD" });

  function save() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
    } catch (e) {
      /* private mode — cart lives for the session only */
    }
  }

  function count() {
    return cart.reduce((sum, item) => sum + item.qty, 0);
  }

  function updateCountBadges(n) {
    document.querySelectorAll(".cart-count").forEach((badge) => {
      badge.textContent = n;
      badge.classList.toggle("has-items", n > 0);
    });
  }

  /* ---------- Drawer markup (injected once) ---------- */
  const drawerHTML = `
    <div class="cart-backdrop" data-cart-close></div>
    <aside class="cart-drawer" role="dialog" aria-modal="true" aria-label="Shopping cart">
      <div class="cart-head">
        <h2>Your Harvest</h2>
        <button class="cart-close" data-cart-close aria-label="Close cart">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
      </div>
      <div class="cart-items" data-cart-items></div>
      <div class="cart-foot">
        <div class="pickup-nudge" data-pickup-nudge hidden>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 9l1-5h16l1 5M4 9v10a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V9M9 13h6"/></svg>
          <span>Choosing <strong>Farm Pickup</strong> at checkout earns <strong>2× loyalty points</strong> — and it's on us. Skip delivery, meet your mushrooms in Fairfield.</span>
        </div>
        <div class="ship-progress" data-ship-progress hidden>
          <p class="ship-progress-label" data-ship-label></p>
          <div class="ship-progress-bar"><div class="ship-progress-fill" data-ship-fill></div></div>
        </div>
        <div class="cart-savings" data-cart-savings hidden>
          <span>Volume savings (3+ of an item, 10% off)</span>
          <strong data-savings-amt></strong>
        </div>
        <div class="cart-subtotal">
          <span>Subtotal</span>
          <strong data-cart-subtotal>$0.00</strong>
        </div>
        <button class="btn btn--gold" data-cart-checkout>Proceed to Checkout</button>
        <p class="guarantee" style="margin-top: 12px; justify-content: center;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l7 4v6c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6z"/><path d="M9 12l2 2 4-4"/></svg>
          <span><strong>100% money-back guarantee</strong> on every order.</span>
        </p>
        <p class="cart-demo-note">Checkout activates the moment a Snipcart public
        API key is added to <a href="https://snipcart.com" target="_blank" rel="noopener">js/config.js</a> —
        a two-minute setup. Every product is already wired for it.</p>
      </div>
    </aside>`;

  const wrap = document.createElement("div");
  wrap.innerHTML = drawerHTML;
  while (wrap.firstElementChild) document.body.appendChild(wrap.firstElementChild);

  const itemsEl = document.querySelector("[data-cart-items]");
  const subtotalEl = document.querySelector("[data-cart-subtotal]");
  const shipWrap = document.querySelector("[data-ship-progress]");
  const shipLabel = document.querySelector("[data-ship-label]");
  const shipFill = document.querySelector("[data-ship-fill]");
  const savingsWrap = document.querySelector("[data-cart-savings]");
  const savingsAmt = document.querySelector("[data-savings-amt]");
  const pickupNudge = document.querySelector("[data-pickup-nudge]");

  const VOLUME_QTY = 3;
  const VOLUME_OFF = 0.10;

  function lineSavings(item) {
    return item.qty >= VOLUME_QTY ? item.price * item.qty * VOLUME_OFF : 0;
  }

  function renderExtras(subtotal, savings) {
    if (pickupNudge) pickupNudge.hidden = !cart.length;
    if (savingsWrap) {
      savingsWrap.hidden = savings <= 0;
      if (savings > 0) savingsAmt.textContent = "−" + money(savings);
    }
    const threshold = parseFloat(cfg.FREE_SHIP_THRESHOLD) || 0;
    if (shipWrap) {
      shipWrap.hidden = !(threshold > 0 && cart.length);
      if (threshold > 0 && cart.length) {
        const pct = Math.min(100, (subtotal / threshold) * 100);
        shipFill.style.width = pct.toFixed(1) + "%";
        shipLabel.innerHTML =
          subtotal >= threshold
            ? "<strong>You've unlocked free local delivery.</strong>"
            : "You're <strong>" + money(threshold - subtotal) + "</strong> away from free local delivery";
      }
    }
  }

  function render() {
    updateCountBadges(count());
    if (!cart.length) {
      itemsEl.innerHTML = `
        <div class="cart-empty">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true">
            <path d="M4 10c0-4 3.6-7 8-7s8 3 8 7H4zM6 10v2c0 1 .8 2 1.8 2h8.4c1 0 1.8-1 1.8-2v-2M10 14v6M14 14v6"/>
          </svg>
          Your basket is empty — the harvest awaits.
        </div>`;
      subtotalEl.textContent = money(0);
      renderExtras(0, 0);
      return;
    }
    itemsEl.innerHTML = cart
      .map(
        (item, i) => `
      <div class="cart-item">
        <div class="cart-item-name">${item.name}${item.optionValue ? `<span class="cart-item-option">${item.optionName}: ${item.optionValue}</span>` : ""}</div>
        <div class="cart-item-price">${money(item.price * item.qty)}</div>
        <div class="cart-qty" aria-label="Quantity for ${item.name}">
          <button data-qty="-1" data-index="${i}" aria-label="Decrease quantity">&minus;</button>
          <output>${item.qty}</output>
          <button data-qty="1" data-index="${i}" aria-label="Increase quantity">+</button>
        </div>
        <button class="cart-remove" data-remove="${i}">Remove</button>
      </div>`
      )
      .join("");
    const gross = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
    const savings = cart.reduce((sum, item) => sum + lineSavings(item), 0);
    const subtotal = gross - savings;
    subtotalEl.textContent = money(subtotal);
    renderExtras(subtotal, savings);
  }

  function openCart() {
    document.body.classList.add("cart-open");
  }
  function closeCart() {
    document.body.classList.remove("cart-open");
  }

  /* ---------- Events ---------- */
  document.addEventListener("click", (e) => {
    const add = e.target.closest(".snipcart-add-item");
    if (add) {
      e.preventDefault();
      const id = add.dataset.itemId;
      const qty = Math.max(1, parseInt(add.dataset.itemQuantity || "1", 10) || 1);
      const optionName = add.dataset.itemCustom1Name || "";
      const optionValue = add.dataset.itemCustom1Value || "";
      // Different option values (e.g. fulfillment method) are distinct lines —
      // matches how Snipcart itself treats custom options once live.
      const existing = cart.find((item) => item.id === id && item.optionValue === optionValue);
      if (existing) existing.qty += qty;
      else
        cart.push({
          id,
          name: add.dataset.itemName,
          price: parseFloat(add.dataset.itemPrice),
          qty: qty,
          optionName,
          optionValue,
        });
      save();
      render();
      const qtyNote = qty > 1 ? ` × ${qty}` : "";
      const optionNote = optionValue ? ` — ${optionValue}` : "";
      window.ifToast(`${add.dataset.itemName}${qtyNote} added to your basket${optionNote}.`);
      return;
    }

    if (e.target.closest("[data-cart-open]")) {
      e.preventDefault();
      render();
      openCart();
      return;
    }
    if (e.target.closest("[data-cart-close]")) {
      closeCart();
      return;
    }

    const qtyBtn = e.target.closest("[data-qty]");
    if (qtyBtn) {
      const i = parseInt(qtyBtn.dataset.index, 10);
      cart[i].qty += parseInt(qtyBtn.dataset.qty, 10);
      if (cart[i].qty <= 0) cart.splice(i, 1);
      save();
      render();
      return;
    }

    const removeBtn = e.target.closest("[data-remove]");
    if (removeBtn) {
      cart.splice(parseInt(removeBtn.dataset.remove, 10), 1);
      save();
      render();
      return;
    }

    if (e.target.closest("[data-cart-checkout]")) {
      window.ifToast(
        "Demo mode — add your Snipcart key in js/config.js to accept live orders."
      );
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && document.body.classList.contains("cart-open")) {
      closeCart();
    }
  });

  render();

  /* ============================================
     Category filters (shop page)
     ============================================ */
  const filterBtns = document.querySelectorAll(".filter-btn[data-filter]");
  if (filterBtns.length) {
    filterBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        filterBtns.forEach((b) => {
          b.classList.toggle("is-active", b === btn);
          b.setAttribute("aria-pressed", String(b === btn));
        });
        const cat = btn.dataset.filter;
        document.querySelectorAll(".shop-grid .product-card").forEach((card) => {
          const show = cat === "all" || card.dataset.category === cat;
          card.classList.toggle("is-hidden", !show);
        });
        document.querySelectorAll("[data-shop-section]").forEach((label) => {
          const show = cat === "all" || label.dataset.shopSection === cat;
          label.style.display = show ? "" : "none";
        });
      });
    });
  }
})();
