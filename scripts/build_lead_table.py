#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a layered Excel lead table (all / confirmed / pending / stats).

Usage:
  python build_lead_table.py <leads.json> [--out leads.xlsx] [--feishu payload.json]

Expects each lead to have a `phone` (canonical digits) and optionally a
`wa_verified` boolean. If `wa_verified` is absent, it is inferred from source /
credential text containing wa.me / whatsapp / "whats app". Requires openpyxl.

No real data bundled. Synthetic sample:
  python build_lead_table.py ../assets/lead_pool.example.json
"""
import argparse, json, re
from collections import Counter

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
except ImportError:
    raise SystemExit('openpyxl is required: pip install openpyxl')


def wa_verified(lead):
    if 'wa_verified' in lead:
        return bool(lead['wa_verified'])
    text = ' '.join(str(lead.get(k, '')) for k in ('source', 'credential', 'wa_link')).lower()
    return any(k in text for k in ('wa.me', 'whatsapp', 'whats app'))


HEADERS = ['序号', '客户名称', 'WhatsApp号码', '国际格式', '邮箱', '品类', '城市',
           '客户性质', '验证状态', '证据等级', '来源', '命名建议']


def rows_of(items):
    out = []
    for i, x in enumerate(items, 1):
        d = re.sub(r'\D', '', str(x.get('phone', '')))
        status = '✅公开渠道确认WhatsApp' if wa_verified(x) else '⚠️手机号-待设备验证'
        out.append([
            i, x.get('name', ''), d, '+' + d if d else '',
            x.get('email', ''), x.get('category', ''), x.get('city', ''),
            x.get('type', ''), status, x.get('credential', ''),
            x.get('source', ''), x.get('contact_name', ''),
        ])
    return out


def style_header(ws, ncol):
    hf = Font(bold=True, color='FFFFFF')
    fill = PatternFill('solid', fgColor='1F4E78')
    for c in range(1, ncol + 1):
        cell = ws.cell(1, c)
        cell.font = hf
        cell.fill = fill
        cell.alignment = Alignment(vertical='center')
    ws.freeze_panes = 'A2'


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('input')
    ap.add_argument('--out', default='leads.xlsx')
    ap.add_argument('--feishu', help='write cloud-sheet payload JSON here')
    args = ap.parse_args()

    data = json.load(open(args.input, encoding='utf-8'))
    leads = data.get('leads', data) if isinstance(data, dict) else data
    confirmed = [x for x in leads if wa_verified(x)]
    pending = [x for x in leads if not wa_verified(x)]
    all_sorted = confirmed + pending

    wb = Workbook()
    specs = [('全部候选', all_sorted), ('已确认WhatsApp', confirmed), ('待设备验证', pending)]
    for idx, (title, items) in enumerate(specs):
        ws = wb.active if idx == 0 else wb.create_sheet()
        ws.title = title
        ws.append(HEADERS)
        for r in rows_of(items):
            ws.append(r)
        style_header(ws, len(HEADERS))

    ws = wb.create_sheet('统计与口径')
    ws.append(['指标', '数值'])
    for k, v in [
        ('有效候选总数', len(all_sorted)),
        ('已确认WhatsApp', len(confirmed)),
        ('待设备验证', len(pending)),
        ('去重键', '电话号码'),
        ('验证口径', '已确认=来源含wa.me或WhatsApp按钮；待验证=仅手机号需设备核验'),
    ]:
        ws.append([k, v])
    style_header(ws, 2)
    wb.save(args.out)

    if args.feishu:
        payload = []
        for title, items in specs:
            payload.append({'name': title, 'columns': HEADERS,
                            'data': [[str(c) for c in r] for r in rows_of(items)]})
        payload.append({'name': '统计与口径', 'columns': ['指标', '数值'],
                        'data': [['已确认WhatsApp', str(len(confirmed))],
                                 ['待设备验证', str(len(pending))]]})
        json.dump({'sheets': payload}, open(args.feishu, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2)

    print(f'total     : {len(all_sorted)}')
    print(f'confirmed : {len(confirmed)}')
    print(f'pending   : {len(pending)}')
    print(f'excel     : {args.out}')
    if args.feishu:
        print(f'feishu    : {args.feishu}')


if __name__ == '__main__':
    main()
