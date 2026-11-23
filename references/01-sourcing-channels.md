# Stage 1 — Sourcing Channels

Goal: build a candidate pool of **end buyers** (importers / wholesalers / factories) in a target market, with a verifiable contact method for each. Favor free, public channels. Work in waves and keep a running pool file (JSON) with a fixed schema (see `assets/lead_pool.example.json`).

## Who to target / who to exclude

**Target:** companies that import goods from your origin country and resell or use them — importers, wholesalers, distributors, retail chains, factories.

**Exclude (peers and noise):**
- Freight forwarders, customs brokers, shipping agents, clearing agents
- Sourcing / procurement agents and B2B buying platforms
- Exporters in the target country (they sell, not buy)
- Your own company, colleagues, payment/receiving contacts
- Local manufacturers that only produce for the domestic market with no import signal

Add exclusion keywords to every search: `-forwarder -freight -logistics -customs -clearing -cargo -shipping -agent`. Then manually verify ambiguous ones.

## Channel matrix (free / public)

| Channel | What it gives | How to use |
|---|---|---|
| **Google Maps / map tools** | Company name, phone, address, sometimes WhatsApp | Search `keyword + city` (e.g. `tiles importer {city}`). Best for local precision. A phone on Maps can be checked on WhatsApp directly. Map-scraping helper sites may fail — fall back to Google Maps UI search. |
| **Yellow pages** | Company listings with phone / email / website | Search by country → city → industry → product keyword. Country-local directories often have mobile numbers. |
| **Customs / trade data** | Real importer names + shipment records | Free tiers let you search by product keyword to find actual buyers and, sometimes, their origin (e.g. "from China"). Strongest evidence of import activity. |
| **Company directories** | Verified businesses, sometimes founded year | Filter by category + city. Founded year + full address = better authenticity signal. |
| **Search engines** | Anything indexed | Operators below. Information scarcity is relative — change keywords repeatedly. |
| **B2B / B2C platforms** | Buyer demand and price benchmarks | B2B: marketplace listings; B2C: local e-commerce to gauge demand and price sensitivity. |
| **Social / messaging** | Direct, informal contact | WhatsApp and Facebook dominate in many emerging markets. |
| **Industry associations / chambers** | Member directories with contacts | Often overlooked; good for wholesale/factory leads. |
| **Trade shows** | High-intent face-to-face leads | Expensive but high close rate; visit soon after the event. Budget option: attend a major home-country trade fair. |
| **Local trade companies / offices** | Warm introductions | Many African/EM trade firms keep offices in sourcing hubs; they hold buyer relationships. |
| **Local office + network** | Long-term scale | If budget allows, set up a local office and partner with a capable local contact. |

## Search syntax that works

Use Google/Yahoo (target-market audiences still rely on them). Combine a product keyword with an intent word and a location:

```
"{品类}" importer {城市}
"{品类}" buyer / wholesaler / distributor {国家}
"{品类}" "direct import" from China {国家}
"{品类}" importer {城市} -forwarder -freight -customs -logistics
site:<directory-domain> {品类} {城市}
"{品类}" "wa.me" {国家}
```

Tips:
- Run many small, varied queries rather than a few broad ones.
- English works in most markets; add the local language where relevant.
- A phone number on a company site / Facebook page / Maps listing is a usable lead even without email.

## Evidence strength for "imports from my country"

Record a per-lead evidence note using three tiers:
- **Strong** — customs/trade data or site text explicitly says "from China" / "direct importer", OR a wa.me / WhatsApp button is present.
- **Medium** — site lists the specific product category and mobile number, founded year, full address.
- **Weak** — directory-only listing, category inferred, no direct import proof. Use conditional wording in the message ("If you import from China…") rather than assuming.

## Workflow loop

1. Pick 2–3 channels suitable for the market and product.
2. Run a wave of searches; append each hit to the pool JSON with name, phone, WhatsApp, email, category, city, source URL, evidence note, type.
3. Skip anything on the exclusion list or already in the pool.
4. Repeat waves until the target count is reached.
5. Hand the pool to Stage 2 (verify + dedup).

## Reality check on "verified WhatsApp"

Public sources rarely give everything at once. Expect to distinguish:
- **Confirmed WhatsApp**: source contains a wa.me link / WhatsApp button / "call via WhatsApp".
- **Phone pending device check**: source lists only a mobile number — must be checked on a device later.

Do not claim the second group is verified. Build the table layered (see Stage 5).
