# Innoculated Farms — Gold & Black Edition

A three-page luxury site for Innoculated Farms (Fairfield, NJ): cinematic home,
Snipcart-ready shop, and the Sub to Soil garden program. Zero build step, zero
frameworks — deploy the folder anywhere.

## Pages

| File | Purpose |
|---|---|
| `index.html` | Cinematic home — hero, standards, story, five varieties, apothecary, Chef's Harvest Box, Sub to Soil teaser, contact |
| `shop.html` | Full catalog with category filters and cart — all 5 fresh varieties, powder, 3 tinctures, 2 curated boxes |
| `sub-to-soil.html` | Garden program — the cycle, 4-step service, benefits, free-consultation form, FAQ |
| `products/*.html` | 11 individual product pages — 3-photo gallery, quantity + add-to-basket, detail accordions, real customer quotes, cross-sells, frequently-bought-together, sticky buy bar, Product JSON-LD |
| `subscribe.html` | Subscription plans (Monthly Lion's Mane, Functional Stack, Immune Stack, weekly Family Box) with pickup/delivery/shipping selector and skip/pause/swap messaging |
| `referral.html` | Refer-a-friend page — 3-step structure with waitlist form; program specifics intentionally left for later |
| `rewards.html` | The Mycelium Club loyalty program — points for purchases, reviews, shares, referrals, birthdays; waitlist form |

## Reviews & the review gate

- The home page carries a side-scrolling **Google reviews rail**. Its content lives in
  `window.IF_REVIEWS` in `js/config.js` — currently seeded with the three verified
  customer testimonials from the old site. **Paste your verbatim Google reviews there**
  (text + first name exactly as they appear on Google, `source: "google"` to show the
  badge). The rail scrolls/swipes automatically once cards overflow.
- "Rate us" buttons (reviews section + every footer) open the **rating modal**:
  5 stars opens your Google write-a-review dialog (`GOOGLE_REVIEW_URL` in config.js);
  1–4 stars routes to a private name/email/feedback form that posts to your Formspree
  endpoint with the chosen rating attached.
- ⚠️ Heads-up: routing only 5-star raters to Google ("review gating") is against
  Google's review policies and can get reviews filtered if detected. Ship it or
  soften it — your call; swapping the gate to "everyone goes to Google" is a
  two-line change in `js/main.js`.

## Conversion features

- **Frequently bought together** — every product page pairs itself with its top
  companion and one "Add Both" button.
- **Volume discount** — 3+ of the same item takes 10% off that line, computed in the
  demo cart and shown as a savings row. (When Snipcart goes live, mirror it there:
  Dashboard → Discounts → quantity-based.)
- **Free-shipping progress bar** — cart drawer shows "you're $X away from free local
  delivery"; threshold is `FREE_SHIP_THRESHOLD` in config.js.
- **Subscription savings** — every plan shows its % saved vs. one-time.
- **Limited-time offer bar** — set `OFFER_TEXT` in config.js to show a dismissible
  site-wide bar; leave `""` to keep it off (use sparingly).
- **100% money-back guarantee** — surfaced on every product buy panel, the shop hero,
  the subscribe page, the cart drawer, and all footers. It's a trust signal only; the
  actual refund policy is up to you to honor.

## Wholesale & farm-pickup incentives

- **Wholesale** is its own page (`wholesale.html`) with its own nav tab — hero,
  audience cards for restaurants / meal-prep / corporate, a 3-step onboarding story,
  a terms-at-a-glance grid, and an inquiry form (posts to Formspree via
  `data-if-form`). It is deliberately **not** mentioned anywhere on the home page;
  the shop page's trade CTA links here.
- **Farm-pickup nudges** steer customers toward the cheapest fulfillment for the farm:
  a "2× Points" badge on the subscribe page's pickup chip, a pickup nudge in the cart
  drawer, and a "Farm pickup · 2× points" earning card on the rewards page. The 2×
  multiplier is a stated promise — wire it into your loyalty provider at launch.

## Fresh-mushroom photography

The five variety photos live in `assets/photos/fresh-*.jpg` and appear on the home
variety cards, the shop fresh-mushroom cards, and the five fresh product-page
galleries. They're black-background studio shots, so they sit flush in the gold
plate frames. To replace one, drop a new file at the same path (or update the
`photos` list in `build_products.py` for the product pages and re-run).

## Product pages

The 11 pages in `products/` are **generated** — edit the catalog in
`build_products.py` (copy, prices, photos, pairings) and re-run:

```
python build_products.py
```

Each gallery has 3 slides: the real photo first (where one exists in
`assets/photos/`), then two engraved placeholder plates ("Detail" and a
category-specific second angle). To swap a placeholder for a real photo, add
the filename to that product's `"photos"` list in `build_products.py` and
rebuild. The quantity selector feeds Snipcart's `data-item-quantity`, so it
works in demo mode and live mode alike. Product names on the shop and home
cards link into these pages.

`css/main.css` holds the entire design system (tokens at the top).
`js/main.js` is shared behavior; `js/shop.js` is the cart; `js/config.js` is the
only file you edit to go live.

## Go-live checklist (three edits, ~10 minutes)

1. **Checkout** — create a free [Snipcart](https://snipcart.com) account, copy the
   *public* API key, paste it into `js/config.js`. Every Add button already carries
   full Snipcart data attributes; the demo cart hands over automatically.
   (I can't create the account for you — it needs your business/payment details.)
2. **Forms** — create a free [Formspree](https://formspree.io) form and paste its
   endpoint into `js/config.js`. Both the contact form and the consultation form
   post to it. Until then they show a success state without sending.
3. **Email** — replace `hello@innoculatedfarms.com` in `index.html` with the real
   inbox (2 occurrences: contact section link).

## Dropping in real photography

Every gold-framed "Photography Plate" accepts a real image with one line —
place it as the first child inside the `.plate` figure:

```html
<figure class="plate">
  <img class="plate-photo" src="assets/photos/lions-mane.jpg"
       alt="Fresh Lion's Mane cluster" loading="lazy">
  ...
</figure>
```

The engraved line-art hides itself automatically when a photo is present
(`.plate:has(.plate-photo)`), and the gold double-frame stays. Recommended:
4:5 crop for product plates, 16:10 for the wide feature plates, WebP ≤ 200 KB.

## Prices

Real prices from the current site were kept (powder $45.99, tinctures $30).
Fresh-mushroom and box prices are sensible placeholders — edit them in **two
places** per product: the visible `.product-price` text and the button's
`data-item-price` attribute (Snipcart charges from the attribute).

## Run locally

```
python serve.py
```

Serves on `http://localhost:8642` with no-cache headers, so edits always show up
on refresh. (Plain `python -m http.server` works too but the browser will
aggressively cache `css/main.css` and the `js/*.js` files between edits —
use `serve.py` during active development.) Everything also works by
double-clicking `index.html` — the demo cart uses localStorage.

## Cursor micro-interactions

Three mouse-only effects, echoing the site's own gold-dust motif:

- **Cursor trail** — a lagging gold ring with three drifting dust motes,
  swelling over anything clickable
- **Magnetic buttons** — `.btn` and `.add-btn` elements lean a few px toward
  the cursor and spring back
- **Card spotlight** — a faint gold glow tracks the cursor across
  `.product-card`, `.variety-card`, `.step`, and `.benefit`

All three require `(hover: hover) and (pointer: fine)` and are skipped under
`prefers-reduced-motion` — touch devices get none of it. The trail's animation
loop sleeps when the pointer is idle. Implementation lives at the bottom of
`js/main.js` and in the "CURSOR MICRO-INTERACTIONS" block near the end of
`css/main.css`.

## Design notes

- Palette: black `#0B0A07` / gold `#C9A43A` / ivory `#F5EFE2` — all text pairs
  meet WCAG AA on dark.
- Type: Playfair Display (display) + Karla (body), Google Fonts.
- Motion: IntersectionObserver reveals, hero parallax, gold sheen — transform/
  opacity only, fully disabled under `prefers-reduced-motion`.
- Touch targets ≥ 44px, focus-visible styles, skip link, semantic landmarks,
  LocalBusiness JSON-LD on the home page.

> Note: a second, earlier site build lives in the sibling `innoculated-farms/`
> folder (caramel/cream palette, five pages). The two are independent — keep
> whichever direction wins.
