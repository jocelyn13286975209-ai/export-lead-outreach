#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate contact names: {国家}{品类}{商家名}, with A/B/C suffix on collisions.

Usage:
  python generate_names.py <leads.json> --country "{国家}" [--out names.json]

Reads each lead's category/name (and optional `product`), derives a short product
label via a configurable keyword map, extracts the brand core from the company
name, and produces a unique display name. Same product + same brand -> A/B/C.

The keyword map and drop-word set are intentionally generic; edit PRODUCT_RULES
and DROP_WORDS for your market. No real data is bundled.
"""
import argparse, json, re
from collections import Counter

# (regex, product label) — order = priority, specific before generic
PRODUCT_RULES = [
    (r'solar|inverter|光伏|太阳能', '光伏'),
    (r'perfume|fragrance|香水|香氛', '香水'),
    (r'mattress|床垫', '家居'),
    (r'toner|ink|printer|墨盒|耗材|打印机', '耗材'),
    (r'glass|aluminium|aluminum|门窗|玻璃|铝材', '铝材玻璃'),
    (r'agrochem|pest|fertilizer|种子|农化|肥料|农药', '农化'),
    (r'auto|spare|tyre|tire|汽车|汽配|轮胎', '汽配'),
    (r'cosmetic|makeup|beauty|化妆品|美妆', '化妆品'),
    (r'pharma|medical|chemist|医药|医疗|药品', '医药'),
    (r'food|beverage|食品|饮料|粮食', '食品'),
    (r'furniture|家具', '家具'),
    (r'electronics|digital|phone|gadget|cctv|手机|电子|家电', '电子'),
    (r'hardware|building|steel|tile|ceramic|建材|五金|钢材|瓷砖|卫浴', '建材'),
    (r'clothing|fashion|bags|shoe|服装|鞋|箱包', '服装'),
    (r'kitchen|cookware|厨具|厨房', '厨具'),
    (r'machinery|power tool|机械|设备|电动工具', '机械'),
    (r'chemical|paint|glue|化工|涂料|粘合剂', '化工'),
    (r'packaging|plastic|hdpe|paper|包装|塑料|纸', '包装'),
    (r'pump|irrigation|水泵|灌溉', '水泵'),
    (r'stationery|book|办公|文具|书籍', '文具'),
    (r'baby|kids|母婴|儿童', '母婴'),
    (r'household|home|decor|家居|日用品', '家居'),
]

DROP_WORDS = {
    'limited', 'ltd', 'company', 'co', 'enterprises', 'enterprise', 'trading',
    'trade', 'group', 'international', 'industries', 'industrial', 'solutions',
    'systems', 'services', 'service', 'supplies', 'supply', 'agencies', 'agency',
    'investments', 'investment', 'general', 'merchants', 'merchant', 'hub',
    'store', 'the', 'and',
    # Add your own target country / region words here, e.g. '<country>', '<region>'.
}


def product_of(lead):
    text = f"{lead.get('category','')} {lead.get('product','')} {lead.get('name','')}".lower()
    for pat, label in PRODUCT_RULES:
        if re.search(pat, text):
            return label
    return '杂货'


def brand_of(lead):
    name = re.sub(r'\(.*?\)', '', str(lead.get('name', '')))
    name = re.sub(r'[^A-Za-z0-9 ]', ' ', name)
    words = [w for w in name.split() if w]
    core = [w for w in words if w.lower() not in DROP_WORDS] or words[:2]
    brand = ''.join(w.capitalize() for w in core[:2])
    if len(brand) > 14:
        brand = ''.join(w.capitalize() for w in core[:1])[:14]
    return brand or 'Brand'


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('input', help='leads JSON (list or {"leads":[...]})')
    ap.add_argument('--country', default='{国家}', help='country prefix for names')
    ap.add_argument('--out', help='output JSON path')
    args = ap.parse_args()

    data = json.load(open(args.input, encoding='utf-8'))
    leads = data.get('leads', data) if isinstance(data, dict) else data
    leads = sorted(leads, key=lambda x: (product_of(x), str(x.get('name', ''))))

    used = {}
    out = []
    for x in leads:
        prod = product_of(x)
        brand = brand_of(x)
        base = f"{args.country}{prod}{brand}"
        n = used.get(base, 0) + 1
        used[base] = n
        name = base if n == 1 else f"{base}{chr(64 + n)}"
        row = dict(x)
        row['contact_name'] = name
        row['product'] = prod
        row['brand'] = brand
        out.append(row)

    json.dump(out, open(args.out or (args.input.rsplit('.', 1)[0] + '.named.json'), 'w',
                        encoding='utf-8'), ensure_ascii=False, indent=2)

    names = [r['contact_name'] for r in out]
    dups = [k for k, v in Counter(names).items() if v > 1]
    print(f'leads named     : {len(out)}')
    print(f'product spread  : {Counter(r["product"] for r in out).most_common(12)}')
    print(f'names unique    : {len(set(names)) == len(names)}')
    print(f'collisions left : {dups if dups else "none"}')
    print('sample:')
    for r in out[:5]:
        print('  ', r['contact_name'])


if __name__ == '__main__':
    main()
