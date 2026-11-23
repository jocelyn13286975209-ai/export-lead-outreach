---
name: export-lead-outreach
description: End-to-end workflow for finding overseas import buyers from public free channels, verifying their WhatsApp, deduplicating by phone number, naming and filing them, writing a high-reply first-touch message, and sending it via phone automation while tracking follow-up. Use this skill when a user asks to find overseas customers/importers/wholesalers for an export or freight/logistics business, build a verified WhatsApp lead list, write or optimize cold-outreach messages, send WhatsApp messages in batches, or classify and follow up leads. Covers sourcing, verification, messaging, phone automation, and CRM-tracking stages.
agent_created: true
---

# Export Lead Outreach

## Overview

A field-tested, end-to-end pipeline that turns open web sources into a **verified WhatsApp lead list** and drives the **first outreach** to a reply. It codifies the full loop: sourcing → verification → dedup → naming/filing → message design → phone-automated sending → follow-up classification.

The workflow is business-agnostic: replace the placeholders (`{国家}`, `{城市}`, `{品类}`, `{你的名字}`, `{你的公司}`, `{你的官网}`) with your own. It was distilled from real export/freight prospecting and includes the hard-won pitfalls of WhatsApp phone automation.

## When to use

- "Find me importers/wholesalers/factories in {country} that buy from China"
- "Build a verified WhatsApp customer list of N companies"
- "Optimize my first-touch message — nobody is replying"
- "Send WhatsApp messages to these leads in batches and save contacts"
- "Classify my leads by intent and set follow-up priority"
- "Sync my lead list to a spreadsheet / cloud sheet"

## Workflow Decision Tree

Match the request to a stage, then load the matching reference in `references/`:

| User intent | Stage | Reference to load |
|---|---|---|
| Find candidate customers from free channels | 1 Sourcing | `references/01-sourcing-channels.md` |
| Check a phone is real WhatsApp / dedup by number | 2 Verify & dedup | `references/02-verification-dedup.md` |
| Write / optimize a first-touch message or reply | 3 Message design | `references/03-outreach-scripts.md` |
| Send messages / save contacts / handle invalid numbers on phone | 4 Phone automation | `references/04-whatsapp-automation.md` |
| Name & file leads, classify intent, sync to sheet | 5 Filing & tracking | `references/05-tracking-notes.md` |

For a full "find → send → track" request, run all five stages in order.

## Core Principles (apply at every stage)

1. **Verified beats numerous.** A phone number appearing on a website is not the same as a number registered on WhatsApp. Always label the evidence tier; never present unverified numbers as "verified customers".
2. **Phone number is the only dedup key.** Two records with the same name but different numbers are two different customers. Never dedup by name.
3. **Target end buyers, not peers.** Exclude freight forwarders, customs brokers, sourcing agents, your own company, and exporters. Keep end importers / wholesalers / factories.
4. **First touch is about being the right person, not selling.** Lead with the customer and how you found them; keep it short; end with a low-friction question plus a free-value offer.
5. **Confirm before irreversible actions.** Sending messages and deleting/editing contacts are irreversible — confirm recipients and exact text with the user before executing.
6. **No privacy leakage in shared artifacts.** Config files, examples, and any public repo copy must contain only placeholders and synthetic data — never real customer numbers, names, account tokens, or device serials.

## Stage Summary

### Stage 1 — Source candidates
Use the channel matrix and search syntax in `references/01-sourcing-channels.md`. Combine yellow pages, customs data, company directories, Google Maps, search-engine operators, B2B platforms, and social channels. Record for each lead: name, phone/WhatsApp, email, category, city, source URL, and an evidence note. Set a target count and keep sourcing in waves until reached.

### Stage 2 — Verify & dedup
Apply the evidence tiers (confirmed WhatsApp vs. phone-pending-device-check) and normalize+deduplicate phone numbers with `scripts/normalize_phones.py`. Detailed rules in `references/02-verification-dedup.md`.

### Stage 3 — Design the message
Pick a template by lead type in `references/03-outreach-scripts.md` and fill the placeholders. Apply the anti-patterns and the reply-handling rules (read the customer's exact words, correct role misunderstandings gently, end with a two-option question). Confirm the final text with the user before sending.

### Stage 4 — Send via phone automation
Follow `references/04-whatsapp-automation.md`. The reliable method is `wa.me/<digits>?text=<urlencoded>` deep links (pre-fills text exactly), never raw `input text`. Handle invalid numbers by cancelling the dialog, logging, and skipping. Confirm before sending.

### Stage 5 — File & track
Generate names and the layered lead table with `scripts/generate_names.py` and `scripts/build_lead_table.py`. Apply intent classification and message-status rules in `references/05-tracking-notes.md`. Sync to the user's spreadsheet/cloud sheet if requested.

## Configuration

All business-specific values live in `assets/config.example.json` (copy to `config.json` and fill). Scripts read from config where relevant. **Never commit a filled `config.json` or any real lead data.**

## Scripts

- `scripts/normalize_phones.py <input.json> <country_code> [--out out.json]` — normalize phone formats and dedup by number.
- `scripts/generate_names.py <leads.json> --country "{国家}" [--out names.json]` — generate `国家+品类+商家名` contact names with A/B/C suffixes for collisions.
- `scripts/build_lead_table.py <leads.json> [--out x.xlsx] [--feishu payload.json]` — build a layered Excel workbook (all / confirmed / pending / stats) and an optional cloud-sheet payload.

All scripts operate on synthetic/example input by default and print a summary. See each script's `--help`.

## License & privacy

MIT licensed. The repository contains only generic methodology, placeholder config, and synthetic example data. See `README.md` for usage and the privacy checklist before publishing.
