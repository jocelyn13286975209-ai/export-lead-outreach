# Stage 5 — Filing, Classification & Tracking

## Contact naming convention

Default pattern: `{国家}{品类}{商家名}`, with an `A/B/C` suffix only when names collide within the same category.

- `{品类}` from a keyword map (order = priority; put specific categories before generic).
- `{商家名}` = strip corporate suffixes (`Ltd`, `Enterprises`, `Trading`, country/region words, `Group`, `Solutions`…), take the first 1–2 meaningful words, cap length so the WhatsApp display name stays short.
- Generate over the whole set, track used names, append `A`, `B`, `C`… from the second collision onward.
- Verify: all names unique, all numbers unique.

Use `scripts/generate_names.py` to generate the map. Make `{国家}` and the keyword map configurable per market/product.

## Intent classification

**A reply is not automatically high intent.** Judge by what the customer actually wrote.

| Level | Meaning | Signal |
|---|---|---|
| **A — High** | Genuine inquiry / wants a quote | Asks for pricing, packing list, destination port, specific specs |
| **B — Medium** | Comparison / networking / needs clarification | Asks about rates to compare, refers a client, reply off-topic due to role misunderstanding |
| **C — Low** | Perfunctory / auto-reply | `Thank you for contacting…`, `OK`, one-word answers |
| **D — No reply** | Sent, no answer | Last message is yours, no incoming reply |
| **E — Rejected** | Explicit refusal | Clear "no thanks" / not interested |

Track: intent level, follow-up priority, has-replied, reply count, suggested action, evidence note (verifiable), message-status icon, last conversation time, last message preview.

## Message status icons (WhatsApp)

| Icon | Meaning | Action |
|---|---|---|
| Blue double check | Read | Awaiting reply; follow up by cadence |
| Grey double check | Delivered, unread | Wait; don't over-message |
| Grey single check | Send failed / not delivered | Investigate and resend |

Surface failed deliveries in a dedicated "needs resend" view and handle first. To resend, re-open wa.me with the original text and confirm the message count increases.

## Follow-up cadence

- D (no reply): attempt a D2 activation a few days later with a **new angle** (don't repeat the website if already sent).
- B: answer their question, then quote when they provide details; re-touch in 24–48h if silent.
- A: quote promptly and move to negotiation.
- Always log the follow-up action and timestamp.

## Layered lead table

Produce a workbook with these sheets:
1. **All candidates** (sorted by evidence strength)
2. **Confirmed WhatsApp** (priority)
3. **Pending device check**
4. **Stats & definitions** (counts, dedup key, exclusion rules, verification definition)

Columns: seq, company, WhatsApp number, international format, email, category, city, type, verification status, evidence tier, source URL, suggested name.

Use `scripts/build_lead_table.py`. Keep the "verified" count honest by separating confirmed vs pending.

## Cloud-sheet sync (optional)

When the user has a cloud spreadsheet connector:
- Create a workbook in the user's chosen folder; write each sheet via the connector's table-put / cells-set APIs.
- Watch for API quirks: some `table-put` with a start cell inserts an extra header row (delete that row afterward); some CSV imports insert blank lines around emoji/special characters — prefer JSON cells API.
- Always read back a few cells to confirm the data landed correctly and columns align.
- Never include real tokens/credentials in the skill or examples. The user supplies their own connector auth at runtime.

## Privacy before sharing

Before committing or publishing:
- No real customer numbers, names, emails, or company names in any file.
- No real account tokens, folder tokens, API keys, device serials, or local file paths.
- Config and pool examples use only placeholders and obviously synthetic data.
- Keep real working data in a local, gitignored directory.
