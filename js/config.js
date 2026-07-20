/* ============================================================
   INNOCULATED FARMS — Site configuration
   ============================================================
   1) CHECKOUT — create a free account at https://snipcart.com,
      copy your PUBLIC API key (Dashboard → API Keys), and paste
      it below. The cart instantly becomes a live checkout.
      Until then the site runs a polished demo cart.

   2) FORMS — create a free form at https://formspree.io, and
      paste its endpoint below (looks like
      https://formspree.io/f/abcdwxyz). Until then, form
      submissions show a success state without sending.

   3) REVIEWS — GOOGLE_REVIEW_URL opens your Google
      write-a-review dialog. IF_REVIEWS feeds the reviews rail
      on the home page: REPLACE the seeded quotes below with
      your verbatim Google reviews (copy the text and first
      name exactly as they appear on Google).

   4) OFFERS — set OFFER_TEXT to show a site-wide limited-time
      offer bar (e.g. "Harvest Week — 15% off fresh boxes with
      code HARVEST"). Leave it "" to hide the bar. Use sparingly.

   5) FREE SHIPPING — FREE_SHIP_THRESHOLD powers the cart's
      "you're $X away from free delivery" progress bar. Set to
      0 to disable.
   ============================================================ */

window.IF_CONFIG = {
  SNIPCART_API_KEY: "YOUR_SNIPCART_PUBLIC_API_KEY",
  FORM_ENDPOINT: "YOUR_FORMSPREE_ENDPOINT",
  CURRENCY: "usd",

  GOOGLE_REVIEW_URL:
    "https://www.google.com/search?q=Innoculated+farms#lrd=0x89c307f4cc2b9e19:0x444f17282a4f7974,3",

  OFFER_TEXT: "",
  OFFER_LINK: "shop.html",

  FREE_SHIP_THRESHOLD: 75,
};

/* Reviews rail (home page). Swap these seeded site testimonials for your
   verbatim Google reviews — text and first name exactly as written there. */
window.IF_REVIEWS = [
  {
    stars: 5,
    text: "I've tried Lion's Mane at some higher end restaurants and fell in love with them. I wasn't able to find them until I found Innoculated. I'm so happy to have access to cook them to my liking at home!",
    name: "Verified customer",
  },
  {
    stars: 5,
    text: "Adding Lions Mane Powder to my morning routine has been a game changer. There is definitely been an improvement in my mental clarity. I've had it in my coffee, tea, and protein shakes!",
    name: "Verified customer",
  },
  {
    stars: 5,
    text: "I couldn't believe my eyes when I got my mushroom box! It was like opening a treasure chest. I could clearly see AND taste the difference in quality from the store bought mushrooms I'm used to getting. So many delicious possibilities!",
    name: "Verified customer",
  },
];
