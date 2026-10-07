"""Check a synthetic Forms handover inventory. Does not connect to Google.
One inventory per workflow. Missing or blocked evidence is never a pass.
"""
import argparse
import csv
import json
import sys
from pathlib import Path

REQUIRED = {'form', 'response_sheet', 'uploads', 'notifications', 'automation', 'entry_points'}
HEADERS = ['component', 'reference', 'current_owner', 'target_owner', 'status', 'evidence']
STATUSES = {'confirmed', 'pending', 'blocked', 'not_used'}

def check(path):
    rows = {}
    issues = []
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f, strict=True)
        if reader.fieldnames != HEADERS:
            raise ValueError('headers must be exactly: ' + ','.join(HEADERS))
        for number, row in enumerate(reader, 2):
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f'record {number}: wrong column count')
            row = {k:v.strip() for k,v in row.items()}
            component = row['component']
            if component not in REQUIRED:
                raise ValueError(f'record {number}: unknown component')
            if component in rows:
                raise ValueError(f'record {number}: duplicate component')
            if row['status'] not in STATUSES:
                raise ValueError(f'record {number}: invalid status')
            rows[component] = row
            if row['status'] in {'pending', 'blocked'}:
                issues.append({'component':component, 'issue':row['status']})
            elif row['status'] == 'confirmed':
                absent = [k for k in HEADERS[1:] if k != 'status' and not row[k]]
                if absent:
                    issues.append({'component':component,'issue':'missing confirmed fields: '+','.join(absent)})
            elif not row['evidence']:
                issues.append({'component':component,'issue':'not_used requires a reason/evidence reference'})
            if component == 'form' and row['status'] == 'not_used':
                issues.append({'component':component,'issue':'a Forms workflow must identify its form'})
    for component in sorted(REQUIRED - rows.keys()):
        issues.append({'component':component,'issue':'missing component'})
    return {'record_check':'open_items' if issues else 'complete_on_paper',
            'issues':sorted(issues,key=lambda x:(x['component'],x['issue'])),
            'platform_verified':False}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('inventory',type=Path)
    a=p.parse_args(argv)
    try:
        result=check(a.inventory)
    except (OSError, UnicodeError, ValueError, csv.Error) as e:
        print('Input rejected: '+str(e),file=sys.stderr)
        return 2
    print(json.dumps(result,indent=2))
    return 1 if result['issues'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
