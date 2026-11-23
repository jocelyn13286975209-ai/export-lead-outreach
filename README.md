# Export Lead Outreach

A reusable, field-tested workflow skill for **export / freight / cross-border sales teams**: find overseas import buyers from free public channels, verify their WhatsApp, deduplicate, file them, write a high-reply first message, send it via phone automation, and track intent — end to end.

Works with [WorkBuddy](https://www.workbuddy.cn/) as an agent skill, but the methodology and scripts are plain Markdown + Python and can be used on their own.

## The problem it solves

Finding genuine overseas buyers is hard: information is scattered, public sources are incomplete, and most cold messages get ignored. This skill turns a messy manual routine into a repeatable five-stage pipeline and encodes the small details that decide whether a campaign works (number-based dedup, honest verification tiers, natural messaging, reliable phone automation, reply handling).

## The 5 stages

| # | Stage | Key idea |
|---|---|---|
| 1 | **Source** | Yellow pages, customs data, directories, Google Maps, search operators, B2B/social. Target end buyers, exclude peers. |
| 2 | **Verify & dedup** | Distinguish confirmed WhatsApp from bare phone numbers; dedup by phone number only. |
| 3 | **Message design** | Lead with the customer, end with a low-friction question + free value; handle replies by reading their exact words. |
| 4 | **Phone automation** | `wa.me?text=` deep links for exact pre-fill; invalid-number skip; dynamic card/image location. |
| 5 | **File & track** | `{国家}{品类}{商家名}` naming, A/B/C intent levels, message-status icons, layered table + cloud sync. |

See `SKILL.md` for the decision tree and `references/01..05` for the full detail of each stage.

## Install

As a WorkBuddy skill, copy this folder into your skills directory:

```bash
# user-level (all projects)
cp -r export-lead-outreach ~/.workbuddy/skills/
# or project-level (shared with a repo)
cp -r export-lead-outreach <your-project>/.workbuddy/skills/
```

Then ask your assistant something like: *"Find 100 verified WhatsApp importers of {品类} in {国家} and draft the first message."* The skill loads automatically.

## Use the scripts standalone

```bash
pip install openpyxl

# 1. normalize + dedup by phone number
python scripts/normalize_phones.py assets/lead_pool.example.json 000 --out out.json

# 2. generate contact names
python scripts/generate_names.py out.json --country "{国家}" --out named.json

# 3. build the layered Excel / cloud payload
python scripts/build_lead_table.py named.json --out leads.xlsx --feishu payload.json
```

All scripts ship with **synthetic example data only** and print a summary. Edit `PRODUCT_RULES` / `DROP_WORDS` in `generate_names.py` for your market.

## Configuration

Copy `assets/config.example.json` → `config.json` and fill your own company name, name, target market, product keywords, timezone, and connector tokens. Scripts and the assistant use these placeholders; keep the filled file local.

## Privacy checklist before publishing

This repository is designed to be safe to push to GitHub. Before you commit:

- [ ] No real customer phone numbers, names, emails, or companies anywhere.
- [ ] No real API tokens, account/folder tokens, or credentials (`config.json` is gitignored).
- [ ] No real device serials or absolute local paths (see placeholders in config).
- [ ] `lead_pool.example.json` contains only synthetic records.
- [ ] Any working data lives in a local, gitignored directory.

## Disclaimer

Respect local laws and platform terms (including messaging anti-spam rules) when sourcing contacts and sending outreach. Confirm recipients and message text before any automated send. The authors are not responsible for misuse.

## License

MIT — see `LICENSE`.
