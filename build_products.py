"""Generates the 11 static product pages in products/ from the catalog below.

Re-run after editing copy, prices, or photos:  python build_products.py
Each page gets: 3-slide gallery (real photo first when one exists, engraved
placeholder plates otherwise), buy panel with quantity + Snipcart-ready Add,
detail accordions, a real customer quote where one exists, cross-sells, and
Product JSON-LD. Drop real photos into assets/photos/ and set "photos" below.
"""
import json
import os

SITE = {
    "css_v": "growth4",
    "brand": "Innoculated Farms",
}


def fmt_money(n):
    s = f"${n:,.2f}"
    return s[:-3] if s.endswith(".00") else s

# ---------------------------------------------------------------- catalog ---

ART = {
    "lions_mane": '<path d="M14 30c0-10 8-18 18-18s18 8 18 18"/><path d="M14 30v7M18.5 30.5v9M23 31.5v11M27.5 32v13M32 32.5v14M36.5 32v13M41 31.5v11M45.5 30.5v9M50 30v7"/>',
    "blue_oyster": '<path d="M12 44C14 29 27 19 46 17c-6 8-8.5 14.5-8 23"/><path d="M12 44c11 2.5 23 1 32-4.5"/><path d="M12 44l14-15M12 44l19-10M12 44l23-5"/>',
    "shiitake": '<path d="M8 32C10 17 20 9 32 9s22 8 24 23c-8 3-16 4.5-24 4.5S16 35 8 32z"/><path d="M26 36.5c.5 7-.5 12.5-2 17.5h16c-1.5-5-2.5-10.5-2-17.5"/><path d="M18 30l1.5-4M32 32v-4.5M46 30l-1.5-4"/>',
    "maitake": '<path d="M10 35c2-9 8-13 15-13-2.5 6-1.5 10.5 1.5 15-6.5 2-12.5.5-16.5-2z"/><path d="M54 35c-2-9-8-13-15-13 2.5 6 1.5 10.5-1.5 15 6.5 2 12.5.5 16.5-2z"/><path d="M23 21c3-6 6.5-9 9-9s6 3 9 9c-4 4.5-5.5 8-5.5 12h-7c0-4-1.5-7.5-5.5-12z"/><path d="M28 37c.5 6-.5 12-2 17h12c-1.5-5-2.5-11-2-17"/>',
    "chestnut": '<path d="M12 25a8 8 0 0 1 16 0c-3 1.5-5 2-8 2s-5-.5-8-2z"/><path d="M37 21a9 9 0 0 1 18 0c-3.5 1.5-6 2-9 2s-5.5-.5-9-2z"/><path d="M22 36a10 10 0 0 1 20 0c-4 2-6.5 2.5-10 2.5S26 38 22 36z"/><path d="M19 27c.5 5-.5 9-2 13M46 23c.5 6 0 10-1 15M30 38.5c.5 6-.5 11-2 15.5h8c-1.5-4.5-2.5-9.5-2-15.5"/>',
    "jar": '<rect x="18" y="22" width="28" height="30" rx="3"/><path d="M16 14h32v8H16z"/><path d="M25 44c2-4 5-6 7-6s5 2 7 6"/><path d="M18 30h28"/>',
    "tincture": '<rect x="22" y="24" width="20" height="28" rx="3"/><path d="M27 24v-7h10v7"/><rect x="25" y="10" width="14" height="7" rx="2"/><path d="M32 33c2.7 3.6 4 5.6 4 7.4a4 4 0 1 1-8 0c0-1.8 1.3-3.8 4-7.4z"/>',
    "cordyceps": '<path d="M22 54c-2.5-9-2.5-18 0-26 1-3.5 5-3.5 6 0 2.5 8 2.5 17 0 26"/><path d="M36 54c-2.5-11-2.5-22 .5-32 1-3.5 5-3.5 6 0 2.5 10 2 21-.5 32"/><path d="M25 28v-5M39 22v-5"/>',
    "chaga": '<path d="M17 49l-5-13 7-13 13-7 14 4 6 12-4 13-11 6z"/><path d="M19 23l11 7 13-3M30 30l-2 21M30 30l-11-4"/>',
    "crate": '<path d="M8 22L32 12l24 10-24 10z"/><path d="M8 22v20l24 10V32M56 22v20L32 52"/><path d="M20 17l24 10"/>',
    "gift_set": '<rect x="22" y="24" width="20" height="28" rx="3"/><path d="M27 24v-7h10v7"/><rect x="25" y="10" width="14" height="7" rx="2"/><path d="M12 52h40"/>',
    # placeholder arts
    "spore_print": '<circle cx="32" cy="32" r="6"/><path d="M32 10v8M32 46v8M10 32h8M46 32h8M17 17l5.5 5.5M41.5 41.5L47 47M47 17l-5.5 5.5M22.5 41.5L17 47"/><circle cx="32" cy="32" r="16" stroke-dasharray="2 5"/>',
    "kitchen": '<ellipse cx="27" cy="40" rx="17" ry="7"/><path d="M44 38l12-5"/><path d="M21 26c0-3 4-4 4-8M31 26c0-3 4-4 4-8"/>',
    "ritual": '<path d="M18 32h24v9a12 12 0 0 1-24 0z"/><path d="M42 34h5a5 5 0 0 1-5 8"/><path d="M24 24c0-3 4-4 4-8M32 24c0-3 4-4 4-8"/>',
    "unboxing": '<path d="M12 28l20-8 20 8-20 8z"/><path d="M12 28v16l20 8V36M52 28v16L32 52"/><path d="M12 28l-6-7M52 28l6-7"/>',
}

PLACEHOLDER_B = {"fresh": ("kitchen", "In the Kitchen"),
                 "wellness": ("ritual", "The Ritual"),
                 "boxes": ("unboxing", "The Unboxing")}

FRESH_ACC_SHIP = ("Freshness &amp; delivery",
    "<p>Cut to order the morning of dispatch — never from cold storage. Fairfield pickup and Tri-State delivery. "
    "Keep refrigerated in a paper bag and enjoy within the week for peak flavor and texture.</p>")
WELL_ACC_SHIP = ("Shipping &amp; care",
    "<p>Bottled in small batches on the farm and shipped across the Tri-State. Store in a cool, dark place. "
    "These statements have not been evaluated by the FDA; this product is not intended to diagnose, treat, cure, or prevent any disease.</p>")
BOX_ACC_SHIP = ("How dispatch works",
    "<p>Boxes are packed the morning they leave the farm. Choose Fairfield pickup or Tri-State delivery at checkout — "
    "we confirm your dispatch day by email.</p>")

PRODUCTS = [
    {
        "id": "lions-mane-fresh", "name": "Lion's Mane", "cart_name": "Fresh Lion's Mane",
        "latin": "Hericium erinaceus", "cat": "fresh", "price": "14.00", "price_disp": "$14", "unit": "per ½ lb",
        "art": "lions_mane", "photos": ["fresh-lions-mane.jpg"],
        "desc": "Snow-white cascades with a crab-sweet delicacy and a tender, meaty bite.",
        "long": "Lion's Mane is the mushroom that converts skeptics. Seared thick in butter it takes on a golden crust and a texture close to crab or scallop — which is why chefs slice it into “crab” cakes and vegan “steaks.” Ours is grown on hardwood, cut the morning it ships, and never sees cold storage.",
        "benefits": ["Cut to order — never cold storage", "Grown on hardwood, no pesticides ever", "Tender, meaty texture chefs seek out"],
        "acc": [
            ("Tasting notes", "<p>Delicate, faintly sweet, with a crab-like flavor and a dense, tender bite. The exterior crisps beautifully while the center stays succulent.</p>"),
            ("In the kitchen", "<p>Slice thick and sear in butter until deep gold on both sides — salt at the end. Use in place of crab, chicken, or steak; it shreds well for tacos and “crab” cakes.</p>"),
            FRESH_ACC_SHIP,
        ],
        "quote": ("I've tried Lion's Mane at some higher end restaurants and fell in love with them. I wasn't able to find them until I found Innoculated. I'm so happy to have access to cook them to my liking at home!", "Fresh mushroom customer"),
        "pairs": ["lions-mane-powder", "blue-oyster-fresh", "chefs-harvest-box"],
    },
    {
        "id": "blue-oyster-fresh", "name": "Blue Oyster", "cart_name": "Fresh Blue Oyster",
        "latin": "Pleurotus columbinus", "cat": "fresh", "price": "10.00", "price_disp": "$10", "unit": "per ½ lb",
        "art": "blue_oyster", "photos": ["fresh-blue-oyster.jpg"],
        "desc": "Slate-blue velvet fans with tender caps and crisping edges.",
        "long": "The most forgiving mushroom a home cook will ever meet. Blue Oysters soak up whatever you cook them in — butter and garlic for a weeknight side, soy and sesame for something bolder — and the edges crisp while the caps stay tender. Shred them raw for a pulled-meat texture.",
        "benefits": ["The easiest gourmet mushroom to cook", "Cut to order — never cold storage", "No pesticides, no chemicals, ever"],
        "acc": [
            ("Tasting notes", "<p>Mild, savory, and endlessly agreeable — soft caps, crisping edges, and a comforting umami depth that deepens with browning.</p>"),
            ("In the kitchen", "<p>Tear rather than slice, get the pan hot, and don't crowd it. Finish with garlic and a knob of butter, or shred for tacos and stir-fries.</p>"),
            FRESH_ACC_SHIP,
        ],
        "quote": None,
        "pairs": ["shiitake-fresh", "chestnut-fresh", "chefs-harvest-box"],
    },
    {
        "id": "shiitake-fresh", "name": "Shiitake", "cart_name": "Fresh Shiitake",
        "latin": "Lentinula edodes", "cat": "fresh", "price": "12.00", "price_disp": "$12", "unit": "per ½ lb",
        "art": "shiitake", "photos": ["fresh-shiitake.jpg"],
        "desc": "Dense umber caps carrying smoke, earth, and deep umami.",
        "long": "Grown on oak and selected by hand at peak, our shiitake carry the smoke-and-earth depth that made them a staple of great kitchens for a thousand years. The caps are dense and meaty; the flavor is pure umami and gets deeper the harder you sear.",
        "benefits": ["Grown on oak, selected by hand", "Deep umami that anchors any dish", "Cut to order — never cold storage"],
        "acc": [
            ("Tasting notes", "<p>Rich, earthy, faintly smoky. A meaty chew that holds structure in soups, braises, and high-heat stir-fries alike.</p>"),
            ("In the kitchen", "<p>Sear caps hard in a dry pan before adding fat for maximum depth. Save the stems for stock — they carry huge flavor.</p>"),
            FRESH_ACC_SHIP,
        ],
        "quote": None,
        "pairs": ["maitake-fresh", "blue-oyster-fresh", "chefs-harvest-box"],
    },
    {
        "id": "maitake-fresh", "name": "Maitake", "cart_name": "Fresh Maitake",
        "latin": "Grifola frondosa", "cat": "fresh", "price": "16.00", "price_disp": "$16", "unit": "per ½ lb",
        "art": "maitake", "photos": ["fresh-maitake.jpg"],
        "desc": "Hen-of-the-woods — intricate, feathered clusters prized for centuries.",
        "long": "Legend says foragers danced when they found maitake in the wild — the name means “dancing mushroom.” Roasted hot, the feathered clusters shatter into crisp, deeply savory edges around a tender heart. This is the variety chefs fight over.",
        "benefits": ["The chef's favorite — roasts to a crackle", "Feathered clusters, hand-harvested whole", "Cut to order — never cold storage"],
        "acc": [
            ("Tasting notes", "<p>Deep, woodsy, and peppery at the edges. High heat turns the fronds shatteringly crisp while the base stays succulent.</p>"),
            ("In the kitchen", "<p>Tear into large fronds, toss with oil, and roast at high heat until the edges crackle. Finishes pastas, pizzas, and grain bowls like nothing else.</p>"),
            FRESH_ACC_SHIP,
        ],
        "quote": None,
        "pairs": ["shiitake-fresh", "chestnut-fresh", "chefs-harvest-box"],
    },
    {
        "id": "chestnut-fresh", "name": "Chestnut", "cart_name": "Fresh Chestnut",
        "latin": "Pholiota adiposa", "cat": "fresh", "price": "12.00", "price_disp": "$12", "unit": "per ½ lb",
        "art": "chestnut", "photos": ["fresh-chestnut.jpg"],
        "desc": "Copper-capped clusters with nutty undertones and a firm, meaty texture.",
        "long": "Chestnuts are the quiet workhorse of the gourmet kitchen — copper caps, nutty undertones, and a firm bite that holds its own in stews, risottos, and long braises where softer mushrooms disappear. A chef's favorite for good reason.",
        "benefits": ["Firm texture that survives any braise", "Nutty, savory depth", "Cut to order — never cold storage"],
        "acc": [
            ("Tasting notes", "<p>Nutty and savory with a clean, firm chew. Holds shape and texture through wet heat better than nearly any variety.</p>"),
            ("In the kitchen", "<p>Halve the clusters and brown well; then let them simmer — risotto, coq au vin, and mushroom ragù are their natural home.</p>"),
            FRESH_ACC_SHIP,
        ],
        "quote": None,
        "pairs": ["blue-oyster-fresh", "maitake-fresh", "chefs-harvest-box"],
    },
    {
        "id": "lions-mane-powder", "name": "Lion's Mane Powder", "cart_name": "Lion's Mane Powder",
        "latin": "Hericium erinaceus", "cat": "wellness", "price": "45.99", "price_disp": "$45.99", "unit": "90 g jar",
        "art": "jar", "photos": ["lions-mane-cover.jpg", "lions-mane-lifestyle.jpg", "lions-mane-macro.jpg"],
        "desc": "Whole fruiting bodies, slow-dried and fine-milled. For coffee, broths, and clarity.",
        "long": "Whole fruiting-body Lion's Mane — never mycelium-on-grain filler — grown here, slow-dried, and milled fine enough to vanish into coffee. Sixty servings of the mushroom traditionally used to support memory, focus, and nervous-system health.",
        "benefits": ["Whole fruiting body — no grain filler", "Grown, dried &amp; milled on our farm", "Disappears into coffee, tea &amp; broth"],
        "acc": [
            ("What's inside", "<p>100% Hericium erinaceus fruiting body, slow-dried and fine-milled. Nothing else — no mycelium biomass, no starch carriers, no flavorings.</p>"),
            ("The ritual", "<p>Stir a teaspoon into coffee, tea, smoothies, or broth — it dissolves cleanly and adds a faint, pleasant earthiness. Most people take it in the morning; consistency matters more than timing.</p>"),
            WELL_ACC_SHIP,
        ],
        "quote": ("Adding Lions Mane Powder to my morning routine has been a game changer. There is definitely been an improvement in my mental clarity. I've had it in my coffee, tea, and protein shakes!", "Wellness customer"),
        "pairs": ["cordyceps-tincture", "chaga-tincture", "wellness-collection"],
    },
    {
        "id": "reishi-tincture", "name": "Reishi Tincture", "cart_name": "Reishi Tincture",
        "latin": "Ganoderma lucidum", "cat": "wellness", "price": "30.00", "price_disp": "$30", "unit": "2 fl oz",
        "art": "tincture", "photos": ["reishi-tincture.png", "reishi-studio.jpg", "reishi-macro.jpg"],
        "desc": "The “mushroom of immortality,” dual-extracted for calm and deep rest.",
        "long": "Reishi has been called the mushroom of immortality for two thousand years. Ours is dual-extracted — alcohol and hot water — to pull both the calming triterpenes and the polysaccharides from fruiting bodies we grew ourselves. An evening ritual for settling the mind.",
        "benefits": ["Dual-extracted for full potency", "From fruiting bodies we grew ourselves", "Traditionally used for calm &amp; rest"],
        "acc": [
            ("What's inside", "<p>Dual-extract of Ganoderma lucidum fruiting body in alcohol and water. Both extraction methods matter: alcohol pulls the bitter triterpenes, hot water the polysaccharides.</p>"),
            ("The ritual", "<p>A dropper in the evening — straight, or in tea or warm water. Reishi is bitter by nature; that bitterness is the mark of a real extract.</p>"),
            WELL_ACC_SHIP,
        ],
        "quote": None,
        "pairs": ["chaga-tincture", "cordyceps-tincture", "wellness-collection"],
    },
    {
        "id": "cordyceps-tincture", "name": "Cordyceps Tincture", "cart_name": "Cordyceps Tincture",
        "latin": "Cordyceps militaris", "cat": "wellness", "price": "30.00", "price_disp": "$30", "unit": "2 fl oz",
        "art": "cordyceps", "photos": ["cordyceps-tincture.png", "cordyceps-studio.jpg", "cordyceps-macro.jpg"],
        "desc": "Bright orange clubs, extracted for stamina, breath, and drive.",
        "long": "The bright-orange clubs of Cordyceps militaris have long been the athlete's mushroom — traditionally used to support stamina, oxygen uptake, and steady natural energy. Dual-extracted from fruiting bodies grown on the farm, not imported biomass.",
        "benefits": ["Dual-extracted for full potency", "Grown here — never imported biomass", "Traditionally used for energy &amp; endurance"],
        "acc": [
            ("What's inside", "<p>Dual-extract of Cordyceps militaris fruiting body in alcohol and water — the real orange clubs, cultivated in our grow rooms.</p>"),
            ("The ritual", "<p>A dropper before training, the trail, or a long morning — many take it in place of a second coffee. Steady, not jittery.</p>"),
            WELL_ACC_SHIP,
        ],
        "quote": None,
        "pairs": ["reishi-tincture", "lions-mane-powder", "wellness-collection"],
    },
    {
        "id": "chaga-tincture", "name": "Chaga Tincture", "cart_name": "Chaga Tincture",
        "latin": "Inonotus obliquus", "cat": "wellness", "price": "30.00", "price_disp": "$30", "unit": "2 fl oz",
        "art": "chaga", "photos": ["chaga-tincture.png", "chaga-studio.jpg", "chaga-macro.jpg"],
        "desc": "Birch-born and antioxidant-rich. Earthy, grounding, resilient.",
        "long": "Chaga grows slowly on birch and concentrates one of the highest antioxidant loads in the natural world. Our dual-extract pulls its earthy, grounding depth into a daily dropper — traditionally taken for immunity and resilience through the seasons.",
        "benefits": ["Dual-extracted for full potency", "One of nature's richest antioxidant sources", "Traditionally used for immune support"],
        "acc": [
            ("What's inside", "<p>Dual-extract of Inonotus obliquus in alcohol and water. Earthy and faintly vanilla-like from its natural vanillin content.</p>"),
            ("The ritual", "<p>A dropper morning or night — it plays well in coffee, where its earthiness reads almost like dark cocoa.</p>"),
            WELL_ACC_SHIP,
        ],
        "quote": None,
        "pairs": ["reishi-tincture", "lions-mane-powder", "wellness-collection"],
    },
    {
        "id": "chefs-harvest-box", "name": "The Chef's Harvest Box", "cart_name": "The Chef's Harvest Box",
        "latin": "The week's finest, curated", "cat": "boxes", "price": "65.00", "price_disp": "$65", "unit": "per box · weekly",
        "art": "crate", "photos": ["chefs-harvest-box.jpg"], "wide": True,
        "desc": "Two pounds across all five varieties, chosen by our growers the morning of dispatch.",
        "long": "Two pounds of the week's best, chosen by the people who grew it — the morning it leaves the farm. Every box carries all five varieties at whatever moment each is at its peak, with tasting notes and a preparation card so nothing goes to waste.",
        "benefits": ["2 lbs across all five varieties", "Curated morning-of by our growers", "Tasting notes &amp; preparation card included"],
        "acc": [
            ("What's inside", "<p>Roughly two pounds spanning Lion's Mane, Blue Oyster, Shiitake, Maitake, and Chestnut — weighted toward whatever is most spectacular that week — plus tasting notes and a preparation card.</p>"),
            ("Who it's for", "<p>The curious cook who wants the whole range without choosing, the household that cooks most nights, and the gift that outclasses a bottle of wine.</p>"),
            BOX_ACC_SHIP,
        ],
        "quote": ("I couldn't believe my eyes when I got my mushroom box! It was like opening a treasure chest. I could clearly see AND taste the difference in quality from the store bought mushrooms I'm used to getting. So many delicious possibilities!", "Mushroom box customer"),
        "pairs": ["lions-mane-fresh", "maitake-fresh", "wellness-collection"],
    },
    {
        "id": "wellness-collection", "name": "The Wellness Collection", "cart_name": "The Wellness Collection",
        "latin": "All three tinctures, gifted", "cat": "boxes", "price": "80.00", "price_disp": "$80", "unit": "set of three",
        "art": "gift_set", "photos": [],
        "desc": "Reishi, Cordyceps, and Chaga together in a gift-ready set.",
        "long": "The complete daily ritual from one farm: Cordyceps for the morning, Chaga for the day, Reishi for the evening — all dual-extracted from fruiting bodies grown here, boxed and ready to gift. Ten dollars kinder than buying the three alone.",
        "benefits": ["All three tinctures — save $10 vs. separate", "A complete morning-to-evening ritual", "Gift-ready presentation"],
        "acc": [
            ("What's inside", "<p>One 2 fl oz dual-extract each of Reishi, Cordyceps, and Chaga, presented as a gift-ready set with a card explaining each mushroom's tradition.</p>"),
            ("The ritual", "<p>Cordyceps with the morning coffee, Chaga through the day, Reishi as the evening winds down — one farm, one routine, covered.</p>"),
            WELL_ACC_SHIP,
        ],
        "quote": None,
        "pairs": ["reishi-tincture", "cordyceps-tincture", "chaga-tincture"],
    },
]

BY_ID = {p["id"]: p for p in PRODUCTS}
CAT_LABEL = {"fresh": "Fresh from the Grow Room", "wellness": "The Apothecary", "boxes": "Curated Boxes"}


def svg(art_key, cls=""):
    return (f'<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true"{cls}>{ART[art_key]}</svg>')


def gallery(p):
    """3 slides + 3 thumbs. Real photos fill slots first (up to 3);
    engraved placeholder plates fill whatever remains."""
    ph_b_key, ph_b_label = PLACEHOLDER_B[p["cat"]]
    slides, thumbs = [], []
    slide_defs = []
    for photo in p["photos"][:3]:
        slide_defs.append(("photo", photo, f'{p["name"]} — {SITE["brand"]}'))
    if not slide_defs:
        slide_defs.append(("art", p["art"], "Photography Plate"))
    fillers = [("art", "spore_print", "Photography Plate · Detail"),
               ("art", ph_b_key, f"Photography Plate · {ph_b_label}")]
    while len(slide_defs) < 3 and fillers:
        slide_defs.append(fillers.pop(0))

    for i, (kind, ref, label) in enumerate(slide_defs):
        active = " is-active" if i == 0 else ""
        if kind == "photo":
            load_attr = 'fetchpriority="high"' if i == 0 else 'loading="lazy"'
            inner = (f'<img class="plate-photo" src="../assets/photos/{ref}" alt="{label}" {load_attr}>')
            slides.append(f'<div class="pdp-slide{active}" data-slide="{i}">{inner}</div>')
            thumbs.append(f'<button class="pdp-thumb{active}" data-thumb="{i}" aria-label="View photo {i+1}">'
                          f'<img src="../assets/photos/{ref}" alt="" loading="lazy"></button>')
        else:
            slides.append(f'<div class="pdp-slide{active}" data-slide="{i}">'
                          f'<div class="plate-art">{svg(ref)}</div>'
                          f'<figcaption class="plate-cap">{label}</figcaption></div>')
            thumbs.append(f'<button class="pdp-thumb{active}" data-thumb="{i}" aria-label="View {label}">'
                          f'<span class="pdp-thumb-art">{svg(ref)}</span></button>')
    return "\n              ".join(slides), "\n            ".join(thumbs)


def pair_card(pid, i):
    p = BY_ID[pid]
    if p["photos"]:
        plate_inner = (f'<img class="plate-photo" src="../assets/photos/{p["photos"][0]}" alt="{p["name"]}" loading="lazy">')
    else:
        plate_inner = (f'<div class="plate-art">{svg(p["art"])}</div>'
                       f'<figcaption class="plate-cap">Photography Plate</figcaption>')
    return f'''<article class="product-card reveal" style="--i:{i}">
            <a class="pair-link" href="{p["id"]}.html" aria-label="{p["name"]} — view product"></a>
            <figure class="plate">{plate_inner}</figure>
            <div class="product-body">
              <h3 class="product-name">{p["name"]}</h3>
              <p class="product-latin">{p["latin"]}</p>
              <div class="product-foot">
                <p class="product-price">{p["price_disp"]}<span class="product-unit">{p["unit"]}</span></p>
                <button class="add-btn snipcart-add-item"
                  data-item-id="{p["id"]}"
                  data-item-name="{p["cart_name"]}"
                  data-item-price="{p["price"]}"
                  data-item-url="/products/{p["id"]}.html"
                  data-item-description="{p["desc"]}">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
                  Add
                </button>
              </div>
            </div>
          </article>'''


CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>')


def page(p):
    slides, thumbs = gallery(p)
    benefits = "\n                ".join(f"<li>{CHECK}<span>{b}</span></li>" for b in p["benefits"])
    accordions = "\n              ".join(
        f'''<details class="pdp-acc"{" open" if i == 0 else ""}>
                <summary>{title}<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></summary>
                <div class="pdp-acc-body">{body}</div>
              </details>''' for i, (title, body) in enumerate(p["acc"]))

    quote_html = ""
    if p["quote"]:
        text, who = p["quote"]
        quote_html = f'''
    <!-- ================= CUSTOMER QUOTE ================= -->
    <section class="section pdp-quote-band">
      <div class="container">
        <blockquote class="pdp-quote reveal">
          <p>“{text}”</p>
          <footer>— {who}</footer>
        </blockquote>
      </div>
    </section>'''

    pairs = "\n          ".join(pair_card(pid, i) for i, pid in enumerate(p["pairs"]))
    photo_meta = f"/assets/photos/{p['photos'][0]}" if p["photos"] else ""
    og_image = f'\n  <meta property="og:image" content="{photo_meta}">' if photo_meta else ""

    ld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": p["cart_name"],
        "description": p["desc"],
        "sku": p["id"],
        "brand": {"@type": "Brand", "name": SITE["brand"]},
        "offers": {
            "@type": "Offer",
            "url": f"/products/{p['id']}.html",
            "priceCurrency": "USD",
            "price": p["price"],
            "availability": "https://schema.org/InStock",
        },
    }
    if photo_meta:
        ld["image"] = photo_meta
    ld_json = json.dumps(ld, indent=2)

    title = f"{p['name']} — {p['price_disp']} · {SITE['brand']}"
    v = SITE["css_v"]

    fbt = BY_ID[p["pairs"][0]]
    fbt_id = fbt["id"]
    fbt_name = fbt["name"]
    fbt_total = fmt_money(float(p["price"]) + float(fbt["price"]))
    wide_cls = " plate--wide" if p.get("wide") else ""

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{p["desc"]} {p["price_disp"]} {p["unit"]} — grown in Fairfield, NJ by {SITE["brand"]}.">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{p["desc"]}">
  <meta property="og:type" content="product">{og_image}
  <meta name="theme-color" content="#0B0A07">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Karla:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/main.css?v={v}">
  <script type="application/ld+json">
{ld_json}
  </script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to main content</a>

  <!-- ================= HEADER ================= -->
  <header class="header">
    <div class="container--wide header-inner">
      <a class="wordmark" href="../index.html" aria-label="Innoculated Farms — home">
        <span class="wordmark-main"><span class="gilt">INNOCULATED</span></span>
        <span class="wordmark-sub">Farms · Est. 2020</span>
      </a>

      <nav class="nav" aria-label="Primary">
        <a href="../index.html">Home</a>
        <a href="../shop.html" aria-current="page">The Harvest</a>
        <a href="../subscribe.html">Subscribe</a>
        <a href="../wholesale.html">Wholesale</a>
        <a href="../sub-to-soil.html">Sub to Soil</a>
        <a href="../index.html#story">Our Story</a>
        <a href="../index.html#contact">Contact</a>
      </nav>

      <div class="header-actions">
        <button class="cart-btn" data-cart-open aria-label="Open cart">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M4 9h16l-1.8 10.5A2 2 0 0 1 16.2 21H7.8a2 2 0 0 1-2-1.5L4 9z"/>
            <path d="M8 9c0-3.3 1.6-6 4-6s4 2.7 4 6"/>
          </svg>
          <span class="cart-count" aria-hidden="true">0</span>
        </button>
        <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
          <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h18"/></svg>
          <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
      </div>
    </div>
  </header>

  <main id="main">
    <!-- ================= PRODUCT ================= -->
    <section class="pdp">
      <div class="container--wide">
        <nav class="breadcrumb reveal" aria-label="Breadcrumb">
          <a href="../shop.html">The Harvest</a>
          <span aria-hidden="true">/</span>
          <a href="../shop.html">{CAT_LABEL[p["cat"]]}</a>
          <span aria-hidden="true">/</span>
          <span aria-current="page">{p["name"]}</span>
        </nav>

        <div class="pdp-grid">
          <!-- Gallery -->
          <div class="pdp-gallery reveal">
            <figure class="plate pdp-stage{wide_cls}">
              {slides}
            </figure>
            <div class="pdp-thumbs" role="tablist" aria-label="Product photos">
            {thumbs}
            </div>
          </div>

          <!-- Buy panel -->
          <div class="pdp-panel reveal" data-buy-panel>
            <p class="eyebrow">{CAT_LABEL[p["cat"]]}</p>
            <h1 class="pdp-title">{p["name"]}</h1>
            <p class="product-latin pdp-latin">{p["latin"]}</p>

            <p class="pdp-price"><span class="pdp-price-num">{p["price_disp"]}</span><span class="product-unit">{p["unit"]}</span></p>

            <p class="pdp-long">{p["long"]}</p>

            <ul class="benefit-list">
                {benefits}
            </ul>

            <div class="pdp-buy-row">
              <div class="qty" data-qty-widget aria-label="Quantity">
                <button type="button" data-qty-step="-1" aria-label="Decrease quantity">&minus;</button>
                <output data-qty-out aria-live="polite">1</output>
                <button type="button" data-qty-step="1" aria-label="Increase quantity">+</button>
              </div>
              <button class="btn btn--gold pdp-add snipcart-add-item" data-main-add
                data-item-id="{p["id"]}"
                data-item-name="{p["cart_name"]}"
                data-item-price="{p["price"]}"
                data-item-quantity="1"
                data-item-url="/products/{p["id"]}.html"
                data-item-description="{p["desc"]}">
                Add to Basket — <span data-line-total>{p["price_disp"]}</span>
              </button>
            </div>
            <p class="qty-hint">Buy <strong>3+</strong> of this item, save <strong>10%</strong> — applied automatically in your basket.</p>

            <p class="pdp-trust">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
              Harvested to order · Fairfield pickup &amp; Tri-State delivery
            </p>
            <p class="guarantee">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l7 4v6c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6z"/><path d="M9 12l2 2 4-4"/></svg>
              <span><strong>100% money-back guarantee.</strong> If it isn't the best you've had, we replace it or refund you — no questions asked.</span>
            </p>

            <div class="fbt" data-fbt>
              <p class="fbt-label">Frequently bought together</p>
              <div class="fbt-items"><span>{p["name"]}</span><span class="fbt-plus">+</span><span>{fbt_name}</span></div>
              <p class="fbt-total">{fbt_total}</p>
              <button class="add-btn" type="button" data-fbt-pair="{fbt_id}">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
                Add Both
              </button>
            </div>

            <div class="pdp-accordions">
              {accordions}
            </div>
          </div>
        </div>
      </div>
    </section>
{quote_html}
    <!-- ================= PAIRS WELL WITH ================= -->
    <section class="section pdp-pairs">
      <div class="container--wide">
        <div class="section-head reveal">
          <p class="eyebrow">From the Same Soil</p>
          <h2 class="h-display">Pairs well <em>with</em>.</h2>
        </div>
        <div class="shop-grid shop-grid--pairs">
          {pairs}
        </div>
      </div>
    </section>
  </main>

  <!-- Sticky buy bar -->
  <div class="sticky-buy" data-sticky-buy aria-hidden="true">
    <div class="container--wide sticky-buy-inner">
      <p class="sticky-buy-name">{p["name"]} <span class="product-unit">{p["price_disp"]} · {p["unit"]}</span></p>
      <button class="btn btn--gold snipcart-add-item" data-sticky-add
        data-item-id="{p["id"]}"
        data-item-name="{p["cart_name"]}"
        data-item-price="{p["price"]}"
        data-item-quantity="1"
        data-item-url="/products/{p["id"]}.html"
        data-item-description="{p["desc"]}">
        Add to Basket
      </button>
    </div>
  </div>

  <!-- ================= FOOTER ================= -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <a class="wordmark" href="../index.html" aria-label="Innoculated Farms — home">
            <span class="wordmark-main"><span class="gilt">INNOCULATED</span></span>
            <span class="wordmark-sub">Farms · Est. 2020</span>
          </a>
          <p class="footer-tag">Small-batch gourmet &amp; functional mushrooms, grown with patience in Fairfield, New Jersey.</p>
          <p class="guarantee footer-guarantee"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l7 4v6c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6z"/><path d="M9 12l2 2 4-4"/></svg><span><strong>100% money-back guarantee.</strong> If your harvest isn't perfect, we make it right — replaced or refunded, no questions.</span></p>
        </div>
        <div>
          <h4>Explore</h4>
          <ul class="footer-links">
            <li><a href="../shop.html">The Harvest</a></li>
            <li><a href="../subscribe.html">Subscribe</a></li>
            <li><a href="../wholesale.html">Wholesale</a></li>
            <li><a href="../rewards.html">Rewards</a></li>
            <li><a href="../referral.html">Refer a Friend</a></li>
            <li><a href="../sub-to-soil.html">Sub to Soil</a></li>
            <li><a href="../index.html#contact">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4>The Collection</h4>
          <ul class="footer-links">
            <li><a href="../shop.html">Fresh Mushrooms</a></li>
            <li><a href="../shop.html">Wellness &amp; Tinctures</a></li>
            <li><a href="chefs-harvest-box.html">The Chef's Harvest Box</a></li>
            <li><a href="#" data-rate-us>Rate your harvest</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; <span data-year>2026</span> Innoculated Farms · Fairfield, New Jersey · All rights reserved.</p>
        <div class="socials">
          <a href="https://www.facebook.com/innoculated/" aria-label="Facebook" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8h3V4h-3c-2.8 0-5 2.2-5 5v3H6v4h3v8h4v-8h3l1-4h-4V9c0-.6.4-1 1-1z"/></svg>
          </a>
          <a href="https://www.instagram.com/innoculatedfarms" aria-label="Instagram" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor" stroke="none"/></svg>
          </a>
          <a href="https://www.youtube.com/@Innoculated" aria-label="YouTube" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 8.2a3 3 0 0 0-2.1-2.1C18 5.5 12 5.5 12 5.5s-6 0-7.9.6A3 3 0 0 0 2 8.2 31 31 0 0 0 1.5 12 31 31 0 0 0 2 15.8a3 3 0 0 0 2.1 2.1c1.9.6 7.9.6 7.9.6s6 0 7.9-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 22.5 12 31 31 0 0 0 22 8.2zM10 15V9l5.2 3z"/></svg>
          </a>
        </div>
      </div>
    </div>
  </footer>

  <script src="../js/config.js?v={v}"></script>
  <script src="../js/main.js?v={v}"></script>
  <script src="../js/shop.js?v={v}"></script>
  <script src="../js/product.js?v={v}"></script>
</body>
</html>
'''


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products")
    os.makedirs(out_dir, exist_ok=True)
    for p in PRODUCTS:
        path = os.path.join(out_dir, f"{p['id']}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(page(p))
        print(f"wrote products/{p['id']}.html")
    print(f"\n{len(PRODUCTS)} product pages generated.")


if __name__ == "__main__":
    main()
