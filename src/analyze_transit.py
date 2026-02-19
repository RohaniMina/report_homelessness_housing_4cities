from __future__ import annotations

from pathlib import Path
import math
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


RAW_PATH = Path('data/raw/fta_monthly_complete.csv')
PROC_DIR = Path('data/processed')
FIG_DIR = Path('outputs/figures')
REPORT_PATH = Path('outputs/findings.md')

TARGET_METROS = {
    'NYC': 'New York--Jersey City--Newark, NY--NJ',
    'SF Bay': 'San Francisco--Oakland, CA',
    'Chicago': 'Chicago, IL--IN',
}

BASELINE_START = pd.Timestamp('2015-01-01')
BASELINE_END = pd.Timestamp('2019-12-01')
COVID_START = pd.Timestamp('2020-03-01')


def load_data() -> pd.DataFrame:
    usecols = ['Agency', 'UZA Name', 'Mode', 'Date', 'UPT', 'State', 'Reporter Type']
    df = pd.read_csv(RAW_PATH, usecols=usecols, low_memory=False)

    df = df.rename(columns={'UZA Name': 'uza_name', 'Agency': 'agency', 'Mode': 'mode', 'Date': 'date', 'UPT': 'upt'})
    df['date'] = pd.to_datetime(df['date'], format='%B %Y', errors='coerce')
    df['upt'] = pd.to_numeric(df['upt'], errors='coerce')

    df = df.dropna(subset=['date', 'upt', 'uza_name'])
    df = df[df['upt'] >= 0].copy()

    inv_map = {v: k for k, v in TARGET_METROS.items()}
    df = df[df['uza_name'].isin(inv_map)].copy()
    df['metro'] = df['uza_name'].map(inv_map)

    return df


def build_monthly_metro(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.groupby(['metro', 'date'], as_index=False)['upt']
        .sum()
        .sort_values(['metro', 'date'])
    )
    monthly['year'] = monthly['date'].dt.year
    monthly['month'] = monthly['date'].dt.month

    baseline = monthly[(monthly['date'] >= BASELINE_START) & (monthly['date'] <= BASELINE_END)]
    monthly_baseline = (
        baseline.groupby(['metro', 'month'], as_index=False)['upt']
        .mean()
        .rename(columns={'upt': 'baseline_monthly_mean'})
    )

    monthly = monthly.merge(monthly_baseline, on=['metro', 'month'], how='left')
    monthly['pct_of_baseline'] = monthly['upt'] / monthly['baseline_monthly_mean']

    jan_2019 = monthly[monthly['date'] == pd.Timestamp('2019-01-01')][['metro', 'upt']].rename(columns={'upt': 'jan2019_upt'})
    monthly = monthly.merge(jan_2019, on='metro', how='left')
    monthly['index_jan2019_100'] = monthly['upt'] / monthly['jan2019_upt'] * 100

    monthly['upt_12m_avg'] = (
        monthly.sort_values('date')
        .groupby('metro')['upt']
        .transform(lambda s: s.rolling(12, min_periods=3).mean())
    )

    return monthly


def recovery_table(monthly: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for metro, grp in monthly.groupby('metro'):
        grp = grp.sort_values('date').copy()
        covid_grp = grp[grp['date'] >= COVID_START]
        trough_idx = covid_grp['pct_of_baseline'].idxmin()
        trough = grp.loc[trough_idx]

        latest = grp.iloc[-1]
        pre_avg = grp[(grp['date'] >= BASELINE_START) & (grp['date'] <= BASELINE_END)]['upt'].mean()

        def first_recovery(threshold: float) -> pd.Timestamp | pd.NaT:
            hit = grp[(grp['date'] >= COVID_START) & (grp['pct_of_baseline'] >= threshold)]
            return hit['date'].iloc[0] if not hit.empty else pd.NaT

        rec_70 = first_recovery(0.70)
        rec_90 = first_recovery(0.90)

        rows.append(
            {
                'metro': metro,
                'pre_2015_2019_avg_upt': pre_avg,
                'trough_month': trough['date'],
                'trough_pct_of_baseline': trough['pct_of_baseline'],
                'latest_month': latest['date'],
                'latest_upt': latest['upt'],
                'latest_pct_of_baseline': latest['pct_of_baseline'],
                'month_recovered_to_70pct': rec_70,
                'month_recovered_to_90pct': rec_90,
            }
        )

    out = pd.DataFrame(rows).sort_values('latest_pct_of_baseline', ascending=False)
    return out


def mode_mix(df: pd.DataFrame) -> pd.DataFrame:
    mode_monthly = (
        df.groupby(['metro', 'mode', 'date'], as_index=False)['upt']
        .sum()
        .sort_values(['metro', 'mode', 'date'])
    )

    windows = {
        'pre_2015_2019': (pd.Timestamp('2015-01-01'), pd.Timestamp('2019-12-01')),
        'shock_2020_2021': (pd.Timestamp('2020-03-01'), pd.Timestamp('2021-12-01')),
    }

    latest_end = mode_monthly['date'].max()
    latest_start = latest_end - pd.DateOffset(months=11)
    windows['recent_12m'] = (latest_start, latest_end)

    rows = []
    for label, (start, end) in windows.items():
        w = mode_monthly[(mode_monthly['date'] >= start) & (mode_monthly['date'] <= end)]
        agg = w.groupby(['metro', 'mode'], as_index=False)['upt'].sum()
        totals = agg.groupby('metro', as_index=False)['upt'].sum().rename(columns={'upt': 'metro_total'})
        agg = agg.merge(totals, on='metro', how='left')
        agg['period'] = label
        agg['mode_share'] = agg['upt'] / agg['metro_total']
        rows.append(agg)

    out = pd.concat(rows, ignore_index=True)
    out = out.sort_values(['metro', 'period', 'mode_share'], ascending=[True, True, False])
    return out


def agency_concentration(df: pd.DataFrame) -> pd.DataFrame:
    latest_end = df['date'].max()
    latest_start = latest_end - pd.DateOffset(months=11)
    recent = df[(df['date'] >= latest_start) & (df['date'] <= latest_end)]

    agg = recent.groupby(['metro', 'agency'], as_index=False)['upt'].sum()
    agg = agg.sort_values(['metro', 'upt'], ascending=[True, False])
    agg['rank'] = agg.groupby('metro').cumcount() + 1

    top3 = agg[agg['rank'] <= 3].copy()
    totals = agg.groupby('metro', as_index=False)['upt'].sum().rename(columns={'upt': 'metro_total'})
    top3 = top3.merge(totals, on='metro', how='left')
    top3['share_of_metro'] = top3['upt'] / top3['metro_total']

    return top3


def plot_trends(monthly: pd.DataFrame) -> None:
    sns.set_theme(style='whitegrid')

    plt.figure(figsize=(12, 6))
    for metro, grp in monthly.groupby('metro'):
        plt.plot(grp['date'], grp['upt'] / 1e6, label=metro, linewidth=2)
    plt.axvline(COVID_START, color='black', linestyle='--', linewidth=1)
    plt.title('Monthly Public Transit Ridership (UPT) by Metro')
    plt.ylabel('UPT (millions)')
    plt.xlabel('Month')
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / '01_monthly_upt_metros.png', dpi=180)
    plt.close()

    plt.figure(figsize=(12, 6))
    for metro, grp in monthly.groupby('metro'):
        plt.plot(grp['date'], grp['pct_of_baseline'] * 100, label=metro, linewidth=2)
    plt.axhline(100, color='gray', linestyle='--', linewidth=1)
    plt.axvline(COVID_START, color='black', linestyle='--', linewidth=1)
    plt.title('Ridership as % of 2015-2019 Monthly Baseline')
    plt.ylabel('% of baseline')
    plt.xlabel('Month')
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / '02_pct_baseline_metros.png', dpi=180)
    plt.close()

    latest = monthly.groupby('metro', as_index=False).tail(1).sort_values('pct_of_baseline', ascending=False)
    plt.figure(figsize=(8, 5))
    sns.barplot(data=latest, x='metro', y=latest['pct_of_baseline'] * 100, hue='metro', dodge=False, legend=False)
    plt.axhline(100, color='gray', linestyle='--', linewidth=1)
    plt.title('Latest Month Recovery Level')
    plt.ylabel('% of baseline')
    plt.xlabel('Metro')
    plt.tight_layout()
    plt.savefig(FIG_DIR / '03_latest_recovery_bar.png', dpi=180)
    plt.close()

    pivot = monthly.copy()
    pivot['year'] = pivot['date'].dt.year
    pivot['month'] = pivot['date'].dt.month
    for metro, grp in pivot.groupby('metro'):
        heat = grp.pivot(index='year', columns='month', values='pct_of_baseline') * 100
        plt.figure(figsize=(11, 5))
        sns.heatmap(heat, cmap='RdYlGn', vmin=20, vmax=130, cbar_kws={'label': '% of baseline'})
        plt.title(f'{metro}: Monthly Ridership vs Baseline Heatmap')
        plt.xlabel('Month')
        plt.ylabel('Year')
        plt.tight_layout()
        file_name = metro.lower().replace(' ', '_').replace('-', '_')
        plt.savefig(FIG_DIR / f'04_heatmap_{file_name}.png', dpi=180)
        plt.close()


def build_report(recovery: pd.DataFrame, top_modes: pd.DataFrame, top3: pd.DataFrame) -> str:
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
        m = top_modes[top_modes['metro'] == metro]
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
    lines.append('- Figures: outputs/figures/*.png')

    return '\n'.join(lines)


def main() -> None:
    PROC_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = load_data()
    monthly = build_monthly_metro(df)
    recovery = recovery_table(monthly)
    mode = mode_mix(df)
    top_modes = mode.sort_values(['metro', 'period', 'mode_share'], ascending=[True, True, False])
    top3 = agency_concentration(df)

    monthly.to_csv(PROC_DIR / 'monthly_metro_upt.csv', index=False)
    recovery.to_csv(PROC_DIR / 'recovery_summary.csv', index=False)
    mode.to_csv(PROC_DIR / 'mode_mix_summary.csv', index=False)
    top3.to_csv(PROC_DIR / 'agency_top3_recent12m.csv', index=False)

    if os.getenv('MAKE_PLOTS', '0') == '1':
        plot_trends(monthly)

    report = build_report(recovery, top_modes, top3)
    REPORT_PATH.write_text(report)

    print('Done.')
    print('Rows in core dataframe:', len(df))
    print('Latest month:', monthly['date'].max().date())


if __name__ == '__main__':
    main()
