from __future__ import annotations

from pathlib import Path

import pandas as pd

PROC_DIR = Path('data/processed')
REPORT_PATH = Path('outputs/findings.md')


def build_report(recovery: pd.DataFrame, mode: pd.DataFrame, top3: pd.DataFrame) -> str:
    mode = mode.sort_values(['metro', 'period', 'mode_share'], ascending=[True, True, False])

    lines: list[str] = []
    lines.append('# Transit Ridership Deep Dive: NYC vs SF Bay vs Chicago')
    lines.append('')
    lines.append('Data source: FTA National Transit Database, Complete Monthly Ridership (dataset 8bui-9xvu).')
    lines.append('')
    lines.append('## Scope')
    lines.append('- Metros: NYC, SF Bay, Chicago (UZA-level aggregates).')
    lines.append('- Baseline window: January 2015 through December 2019.')
    lines.append('- COVID break point: March 2020.')
    lines.append('')
    lines.append('## Key Findings')

    for _, r in recovery.sort_values('latest_pct_of_baseline', ascending=False).iterrows():
        metro = r['metro']
        trough_pct = r['trough_pct_of_baseline'] * 100
        latest_pct = r['latest_pct_of_baseline'] * 100
        trough_month = pd.to_datetime(r['trough_month']).strftime('%Y-%m')
        latest_month = pd.to_datetime(r['latest_month']).strftime('%Y-%m')
        rec70 = 'not reached' if pd.isna(r['month_recovered_to_70pct']) else pd.to_datetime(r['month_recovered_to_70pct']).strftime('%Y-%m')
        rec90 = 'not reached' if pd.isna(r['month_recovered_to_90pct']) else pd.to_datetime(r['month_recovered_to_90pct']).strftime('%Y-%m')
        lines.append(
            f'- {metro}: trough at {trough_month} ({trough_pct:.1f}% of baseline); latest {latest_month} at {latest_pct:.1f}% of baseline; 70% recovery: {rec70}; 90% recovery: {rec90}.'
        )

    lines.append('')
    lines.append('## Mode Mix Shifts (Top modes by period)')

    for metro in ['NYC', 'SF Bay', 'Chicago']:
        lines.append(f'- {metro}:')
        m = mode[mode['metro'] == metro]
        for period in ['pre_2015_2019', 'shock_2020_2021', 'recent_12m']:
            p = m[m['period'] == period].head(3)
            if p.empty:
                continue
            vals = ', '.join([f"{row['mode']} {row['mode_share']*100:.1f}%" for _, row in p.iterrows()])
            lines.append(f'  - {period}: {vals}')

    lines.append('')
    lines.append('## Agency Concentration (Recent 12 months, Top 3)')
    for metro in ['NYC', 'SF Bay', 'Chicago']:
        t = top3[top3['metro'] == metro]
        if t.empty:
            continue
        vals = '; '.join([f"{row['agency']} ({row['share_of_metro']*100:.1f}%)" for _, row in t.iterrows()])
        lines.append(f'- {metro}: {vals}')

    lines.append('')
    lines.append('## Output Files')
    lines.append('- Processed data: data/processed/monthly_metro_upt.csv')
    lines.append('- Recovery summary: data/processed/recovery_summary.csv')
    lines.append('- Mode mix summary: data/processed/mode_mix_summary.csv')
    lines.append('- Agency concentration: data/processed/agency_top3_recent12m.csv')

    return '\n'.join(lines)


recovery = pd.read_csv(PROC_DIR / 'recovery_summary.csv')
mode = pd.read_csv(PROC_DIR / 'mode_mix_summary.csv')
top3 = pd.read_csv(PROC_DIR / 'agency_top3_recent12m.csv')

REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
REPORT_PATH.write_text(build_report(recovery, mode, top3))
print('Wrote', REPORT_PATH)
