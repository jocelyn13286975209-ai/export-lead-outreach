# Stage 2 — Verification & Deduplication

## Two layers of "verified"

Never conflate "has a phone number" with "has WhatsApp".

| Tier | Meaning | How to identify | How to treat |
|---|---|---|---|
| **Confirmed WhatsApp** | Source proves the number is on WhatsApp | Source text/HTML contains `wa.me`, a WhatsApp button/icon, or "chat/call us on WhatsApp" | Safe to message; label `confirmed` |
| **Phone pending device check** | Only a mobile number is public | Yellow pages / site lists a mobile, no WhatsApp marker | Must open on a device to check registration; label `pending` |

Build outputs with both groups separated so the "verified" count is honest. Convert `pending → confirmed` only after a device check succeeds; log failures as invalid.

## Phone number normalization

Country formats vary (`07xxxxxxxx`, `+<cc>7xxxxxxxx`, `<cc> 7xx xxx xxx`). Normalize to one canonical form (country code + national number, digits only) before dedup.

Rules of thumb:
1. Strip all non-digits.
2. If it starts with `0` and is 10 digits, drop the leading `0` and prepend the country code.
3. If it already starts with the country code, keep it.
4. Keep the last 9 digits as a secondary comparison key to catch `+<cc>…` vs `<cc>…` vs `07…` variants.

Use `scripts/normalize_phones.py` to do this in bulk.

## Dedup: phone number is the ONLY key

**Critical rule:** deduplicate by phone number, never by name.

- Same name + different number → **two different customers** (common in markets where names repeat).
- Same number + different name → **one customer** (merge names into an "aliases" field).
- Compare both full canonical number and its last-9-digit suffix.

A name-based dedup will silently delete real customers. When merging an existing master list with a new pool, compare the new pool's numbers against the full existing number set by suffix, not by display name.

## Invalid-number handling

A number can be well-sourced yet unregistered. On a device, an unregistered number shows a "no WhatsApp account" dialog. When that happens:
1. Cancel the dialog (do not invite / do not push).
2. Append the number to an `invalid_numbers.txt` log with company + reason + date.
3. Skip to the next lead. Never let one invalid number stall a batch.

## Verification workflow summary

```
raw pool → normalize phones → dedup by number (suffix-aware)
        → split confirmed vs pending → device-check pending
        → move successful to confirmed, failed to invalid log
        → final verified pool
```

## Field-tested cautions

- The set of existing customers to dedup against must be extracted from the real master table by **number**, including the last-9 suffix set — not by display name.
- Directory data can contain placeholder/fake numbers (e.g. `+XXX 700 000 000`). Filter obvious placeholders.
- A number listed for two different companies is usually a data error; verify before merging.
- Map-sourced phone numbers are often mobile and WhatsApp-ready — prioritize them for device checks.
