#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Normalize phone numbers to a canonical form and deduplicate by number.

Usage:
  python normalize_phones.py <input.json> <country_code> [--out out.json]

<input.json> may be a list of records, or {"leads": [...]}. Each record should
have a phone-like key among: phone, wa, whatsapp, mobile, tel. The script writes
canonical `phone` and a `phone_suffix` (last 9 digits) onto each record, drops
duplicates by canonical number (merging names into an `aliases` list), and
removes obvious placeholder numbers.

No real customer data is bundled — pass your own file. Synthetic sample:
  python normalize_phones.py ../assets/lead_pool.example.json 000
"""
import argparse, json, re, sys

PHONE_KEYS = ('phone', 'wa', 'whatsapp', 'mobile', 'tel')


def digits(s):
    return re.sub(r'\D', '', str(s or ''))


def normalize(raw, cc):
    d = digits(raw)
    cc = digits(cc)
    if not d:
        return ''
    # 00-prefixed international
    if d.startswith('00'):
        d = d[2:]
    # national trunk prefix -> country code
    if cc and d.startswith('0') and len(d) >= 9:
        d = cc + d[1:]
    # bare national number without '0' but shorter than cc+9 -> add cc
    if cc and not d.startswith(cc) and len(d) <= 9:
        d = cc + d
    return d


def is_placeholder(d, cc):
    if len(d) < 8:
        return True
    body = d[len(cc):] if cc and d.startswith(cc) else d
    # e.g. 700000000 / 123456789 style obvious fakes
    return len(set(body)) == 1 or body.startswith('000') or body == '123456789'


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('input', help='input JSON (list or {"leads":[...]})')
    ap.add_argument('country_code', help='country calling code, digits e.g. 000')
    ap.add_argument('--out', help='output JSON path (default: <input>.normalized.json)')
    args = ap.parse_args()

    data = json.load(open(args.input, encoding='utf-8'))
    records = data.get('leads', data) if isinstance(data, dict) else data
    if not isinstance(records, list):
        sys.exit('input must be a list or {"leads": [...]}')

    seen = {}
    dropped_placeholder = 0
    for rec in records:
        raw = next((rec.get(k) for k in PHONE_KEYS if rec.get(k)), '')
        canon = normalize(raw, args.country_code)
        if not canon or is_placeholder(canon, digits(args.country_code)):
            dropped_placeholder += 1
            continue
        rec = dict(rec)
        rec['phone'] = canon
        rec['phone_suffix'] = canon[-9:]
        name = rec.get('name') or rec.get('company') or ''
        key = canon
        if key in seen:
            aliases = seen[key].setdefault('aliases', [seen[key].get('name', '')])
            if name and name not in aliases:
                aliases.append(name)
            # keep the richer evidence record
            if len(str(rec.get('source', ''))) > len(str(seen[key].get('source', ''))):
                seen[key].update(rec)
                seen[key]['aliases'] = aliases
        else:
            seen[key] = rec
    out = list(seen.values())
    out_path = args.out or (args.input.rsplit('.', 1)[0] + '.normalized.json')
    json.dump(out, open(out_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    print(f'in records      : {len(records)}')
    print(f'placeholder/skip: {dropped_placeholder}')
    print(f'unique numbers  : {len(out)}')
    print(f'duplicates merged: {len(records) - dropped_placeholder - len(out)}')
    print(f'output          : {out_path}')


if __name__ == '__main__':
    main()
