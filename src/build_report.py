from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = Path('.')
PROC = BASE / 'data' / 'processed'
OUT = BASE / 'outputs'
FIG = OUT / 'figures' / 'deep_dive'

FIG.mkdir(parents=True, exist_ok=True)

monthly = pd.read_csv(PROC / 'monthly_metro_upt.csv', parse_dates=['date'])
recovery = pd.read_csv(PROC / 'recovery_summary.csv', parse_dates=['trough_month', 'latest_month', 'month_recovered_to_70pct', 'month_recovered_to_90pct'])
mode_mix = pd.read_csv(PROC / 'mode_mix_summary.csv')
mode_recovery = pd.read_csv(PROC / 'mode_recovery_latest12m_vs_baseline.csv')
seasonality = pd.read_csv(PROC / 'seasonality_shift_pre_vs_recent.csv')

metros = ['NYC', 'SF Bay', 'Chicago']
colors = {'NYC': '#0B5FA5', 'SF Bay': '#0F8B8D', 'Chicago': '#9C3D10'}

# 1) Recovery trend vs baseline
fig1 = FIG / '01_recovery_trend_pct_baseline.png'
plt.figure(figsize=(12, 6))
for m in metros:
    g = monthly[monthly['metro'] == m]
    plt.plot(g['date'], g['pct_of_baseline'] * 100, label=m, color=colors[m], linewidth=2)
plt.axhline(100, color='gray', linestyle='--', linewidth=1)
plt.axvline(pd.Timestamp('2020-03-01'), color='black', linestyle=':', linewidth=1)
plt.title('Monthly Ridership Recovery (% of 2015-2019 baseline)')
plt.ylabel('% of baseline')
plt.xlabel('Month')
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig(fig1, dpi=180)
plt.close()

# 2) Trough vs latest comparison
fig2 = FIG / '02_trough_vs_latest.png'
comp = recovery[['metro', 'trough_pct_of_baseline', 'latest_pct_of_baseline']].copy()
comp = comp.set_index('metro').loc[metros].reset_index()

x = np.arange(len(metros))
width = 0.35
plt.figure(figsize=(10, 5))
plt.bar(x - width / 2, comp['trough_pct_of_baseline'] * 100, width=width, label='COVID trough', color='#D95F02')
plt.bar(x + width / 2, comp['latest_pct_of_baseline'] * 100, width=width, label='Latest (2025-12)', color='#1B9E77')
plt.xticks(x, metros)
plt.axhline(100, color='gray', linestyle='--', linewidth=1)
plt.ylabel('% of baseline')
plt.title('Collapse and Recovery by Metro')
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig(fig2, dpi=180)
plt.close()

# 3) Annual level vs 2019
fig3 = FIG / '03_annual_vs_2019.png'
a = monthly.copy()
a['year'] = a['date'].dt.year
annual = a.groupby(['metro', 'year'], as_index=False)['upt'].sum()
base2019 = annual[annual['year'] == 2019][['metro', 'upt']].rename(columns={'upt': 'upt_2019'})
annual = annual.merge(base2019, on='metro', how='left')
annual['pct_vs_2019'] = annual['upt'] / annual['upt_2019'] * 100
annual = annual[annual['year'] >= 2015]

plt.figure(figsize=(12, 6))
for m in metros:
    g = annual[annual['metro'] == m]
    plt.plot(g['year'], g['pct_vs_2019'], marker='o', color=colors[m], linewidth=2, label=m)
plt.axhline(100, color='gray', linestyle='--', linewidth=1)
plt.title('Annual Ridership Relative to 2019')
plt.ylabel('% of 2019 annual ridership')
plt.xlabel('Year')
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig(fig3, dpi=180)
plt.close()

# 4) Mode share shift pre vs recent
fig4 = FIG / '04_mode_share_shift.png'
periods = ['pre_2015_2019', 'recent_12m']
mode_top = mode_mix[mode_mix['period'].isin(periods)].copy()
mode_top['period_label'] = mode_top['period'].map({'pre_2015_2019': 'Pre (2015-2019)', 'recent_12m': 'Recent (last 12m)'})

rows = []
for m in metros:
    for p in periods:
        g = mode_top[(mode_top['metro'] == m) & (mode_top['period'] == p)].sort_values('mode_share', ascending=False).head(3)
        for _, r in g.iterrows():
            rows.append({'metro': m, 'period': r['period_label'], 'mode': r['mode'], 'share': r['mode_share'] * 100})
plot_df = pd.DataFrame(rows)

fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
for ax, m in zip(axes, metros):
    g = plot_df[plot_df['metro'] == m]
    pivot = g.pivot(index='mode', columns='period', values='share').fillna(0)
    pivot = pivot.sort_values('Recent (last 12m)', ascending=False)
    y = np.arange(len(pivot.index))
    ax.barh(y + 0.18, pivot['Pre (2015-2019)'], height=0.35, label='Pre', color='#A6CEE3')
    ax.barh(y - 0.18, pivot['Recent (last 12m)'], height=0.35, label='Recent', color='#1F78B4')
    ax.set_yticks(y)
    ax.set_yticklabels(pivot.index)
    ax.set_title(m)
    ax.invert_yaxis()
    ax.set_xlabel('Mode share (%)')
axes[0].legend(frameon=False, loc='lower right')
fig.suptitle('Top-Mode Share Shift: Pre-COVID vs Recent', y=1.02)
fig.tight_layout()
fig.savefig(fig4, dpi=180, bbox_inches='tight')
plt.close(fig)

# 5) Mode recovery heatmap
fig5 = FIG / '05_mode_recovery_heatmap.png'
heat = mode_recovery.pivot(index='mode', columns='metro', values='pct_of_baseline')
heat = heat.reindex(sorted(heat.index))

fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(heat.values, cmap='RdYlGn', vmin=20, vmax=140, aspect='auto')
ax.set_xticks(np.arange(len(heat.columns)))
ax.set_xticklabels(heat.columns)
ax.set_yticks(np.arange(len(heat.index)))
ax.set_yticklabels(heat.index)
ax.set_title('Mode Recovery (Recent 12m monthly avg vs 2015-2019 monthly avg)')
for i in range(len(heat.index)):
    for j in range(len(heat.columns)):
        v = heat.values[i, j]
        if np.isfinite(v):
            ax.text(j, i, f'{v:.0f}%', ha='center', va='center', fontsize=8, color='black')
fig.colorbar(im, ax=ax, label='% of baseline')
fig.tight_layout()
fig.savefig(fig5, dpi=180)
plt.close(fig)

# 6) Seasonality recovery profile
fig6 = FIG / '06_seasonality_profile.png'
fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)
for ax, m in zip(axes, metros):
    g = seasonality[seasonality['metro'] == m]
    ax.plot(g['month'], g['pct_of_pre'], marker='o', color=colors[m], linewidth=2)
    ax.axhline(100, color='gray', linestyle='--', linewidth=1)
    ax.set_title(m)
    ax.set_xlabel('Month')
    ax.set_xticks(range(1, 13))
axes[0].set_ylabel('Recent as % of pre-COVID same-month average')
fig.suptitle('Seasonality Shift (Recent 12m vs 2015-2019)', y=1.05)
fig.tight_layout()
fig.savefig(fig6, dpi=180, bbox_inches='tight')
plt.close(fig)

# Key stats text
latest = recovery.set_index('metro')['latest_pct_of_baseline'].to_dict()
trough = recovery.set_index('metro')['trough_pct_of_baseline'].to_dict()
latest_month = recovery['latest_month'].max().strftime('%Y-%m')

annual_latest_year = annual['year'].max()
annual_latest = annual[annual['year'] == annual_latest_year].set_index('metro')['pct_vs_2019'].to_dict()

# Markdown report
md_path = OUT / 'transit_deep_dive_report.md'
md = f"""# Transit Ridership Deep Dive (NYC, SF Bay, Chicago)

## TL;DR
- **NYC has recovered far more than SF Bay and Chicago**: {latest['NYC']*100:.1f}% vs {latest['SF Bay']*100:.1f}% and {latest['Chicago']*100:.1f}% of pre-COVID baseline in {latest_month}.
- **All three metros collapsed in April 2020**, with troughs around {trough['NYC']*100:.1f}% (NYC), {trough['SF Bay']*100:.1f}% (SF Bay), and {trough['Chicago']*100:.1f}% (Chicago) of baseline.
- **2025 annual levels still trail 2019** in all three metros: NYC {annual_latest['NYC']:.1f}%, SF Bay {annual_latest['SF Bay']:.1f}%, Chicago {annual_latest['Chicago']:.1f}%.
- **Bus/ferry-oriented modes generally recovered better than heavy rail**, especially outside NYC.

## Data, Source, and Methodology
- **Data nature**: Agency-reported, monthly unlinked passenger trips (UPT), mode-level operational ridership.
- **Primary source**: U.S. Department of Transportation / FTA National Transit Database, Complete Monthly Ridership dataset (`8bui-9xvu`).
- **Coverage used**: Metros mapped by UZA label to NYC (`New York--Jersey City--Newark`), SF Bay (`San Francisco--Oakland`), and Chicago (`Chicago, IL--IN`).
- **Time window**: January 2002 through December 2025 in source; analysis baseline uses **January 2015 to December 2019**.
- **Normalization**: For each metro and month-of-year, baseline is the 2015-2019 average for that same month; recovery is current/baseline.
- **Comparative lens**: Metro-level totals, annual trend vs 2019, mode-share shifts, and mode-specific recovery in recent 12 months.

## Key Insights, Interpretations, and Visualizations

### 1) Recovery paths diverged sharply after the shared shock
Interpretation: The initial COVID shock was similar in magnitude, but long-run recovery speed diverged. NYC nearly returned to baseline; SF Bay and Chicago remain structurally lower.

![Recovery Trend](figures/deep_dive/01_recovery_trend_pct_baseline.png)

### 2) The trough-to-latest gap is largest outside NYC
Interpretation: NYC rebuilt demand substantially from a deep trough, while SF Bay and Chicago recovered less despite similar shock timing.

![Trough vs Latest](figures/deep_dive/02_trough_vs_latest.png)

### 3) Annual totals confirm persistent post-COVID deficits
Interpretation: Even in 2025, no metro has fully returned to 2019 annual ridership. NYC is closest; SF Bay and Chicago appear to have lower new equilibria.

![Annual vs 2019](figures/deep_dive/03_annual_vs_2019.png)

### 4) Mode mix changed, then partially reverted
Interpretation: During the shock, bus share expanded while rail-heavy commuting fell. Recent mix shows partial normalization, but not full reversion in SF Bay/Chicago.

![Mode Share Shift](figures/deep_dive/04_mode_share_shift.png)

### 5) Mode-level recovery is uneven within each metro
Interpretation: High-recovery niches (e.g., ferry/other special modes) coexist with still-depressed commuter-heavy modes, indicating segmented demand recovery.

![Mode Recovery Heatmap](figures/deep_dive/05_mode_recovery_heatmap.png)

### 6) Seasonality patterns are weaker than pre-COVID
Interpretation: Month-to-month recovery remains below pre-COVID seasonal levels across most of the calendar, especially in SF Bay and Chicago.

![Seasonality Profile](figures/deep_dive/06_seasonality_profile.png)

## Detailed Findings
- **Latest month ({latest_month}) recovery vs baseline**:
  - NYC: **{latest['NYC']*100:.1f}%**
  - SF Bay: **{latest['SF Bay']*100:.1f}%**
  - Chicago: **{latest['Chicago']*100:.1f}%**
- **Trough month**: April 2020 for all three metros.
- **Trough depth (% of baseline)**:
  - NYC: **{trough['NYC']*100:.1f}%**
  - SF Bay: **{trough['SF Bay']*100:.1f}%**
  - Chicago: **{trough['Chicago']*100:.1f}%**
- **2025 annual ridership vs 2019**:
  - NYC: **{annual_latest['NYC']:.1f}%**
  - SF Bay: **{annual_latest['SF Bay']:.1f}%**
  - Chicago: **{annual_latest['Chicago']:.1f}%**

## Reproducibility
- Processed data tables are in `data/processed/`.
- This report was generated from those tables by `src/build_report.py`.
"""
md_path.write_text(md)

# HTML report (parallel content)
html_path = OUT / 'transit_deep_dive_report.html'

def img(name: str, alt: str) -> str:
    return f'<figure><img src="figures/deep_dive/{name}" alt="{alt}"/><figcaption>{alt}</figcaption></figure>'

html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Transit Ridership Deep Dive</title>
  <style>
    :root {{ --bg: #f7f8fa; --ink: #1f2937; --muted: #4b5563; --card: #ffffff; --accent: #0b5fa5; }}
    body {{ margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.5 -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
    .wrap {{ max-width: 1000px; margin: 0 auto; padding: 28px 20px 50px; }}
    h1, h2, h3 {{ line-height: 1.25; }}
    h1 {{ margin: 0 0 10px; }}
    .card {{ background: var(--card); border-radius: 12px; padding: 18px 20px; box-shadow: 0 1px 6px rgba(0,0,0,0.08); margin: 14px 0; }}
    ul {{ margin-top: 8px; }}
    figure {{ margin: 14px 0 24px; }}
    img {{ width: 100%; border-radius: 8px; border: 1px solid #e5e7eb; }}
    figcaption {{ color: var(--muted); font-size: 0.93rem; margin-top: 6px; }}
    .muted {{ color: var(--muted); }}
    .kpi {{ font-weight: 700; color: var(--accent); }}
    code {{ background: #eef2f7; padding: 0 5px; border-radius: 4px; }}
  </style>
</head>
<body>
  <div class=\"wrap\">
    <h1>Transit Ridership Deep Dive (NYC, SF Bay, Chicago)</h1>
    <p class=\"muted\">FTA NTD monthly ridership through {latest_month}</p>

    <section class=\"card\">
      <h2>TL;DR</h2>
      <ul>
        <li><span class=\"kpi\">NYC recovered far more:</span> {latest['NYC']*100:.1f}% of baseline vs SF Bay {latest['SF Bay']*100:.1f}% and Chicago {latest['Chicago']*100:.1f}%.</li>
        <li><span class=\"kpi\">Shared collapse in April 2020:</span> NYC {trough['NYC']*100:.1f}%, SF Bay {trough['SF Bay']*100:.1f}%, Chicago {trough['Chicago']*100:.1f}% of baseline.</li>
        <li><span class=\"kpi\">No metro fully back to 2019 annual total in 2025:</span> NYC {annual_latest['NYC']:.1f}%, SF Bay {annual_latest['SF Bay']:.1f}%, Chicago {annual_latest['Chicago']:.1f}%.</li>
      </ul>
    </section>

    <section class=\"card\">
      <h2>Data and Methodology</h2>
      <ul>
        <li>Agency-reported monthly UPT (unlinked passenger trips), mode-level operational ridership.</li>
        <li>Source: USDOT/FTA NTD Complete Monthly Ridership dataset (<code>8bui-9xvu</code>).</li>
        <li>Metro mapping by UZA label for NYC, SF Bay, and Chicago.</li>
        <li>Baseline: January 2015 to December 2019 (same-month normalization).</li>
        <li>Key metrics: % of baseline, annual % vs 2019, mode-share shift, and mode-level recovery.</li>
      </ul>
    </section>

    <section class=\"card\"><h2>Insights and Visual Findings</h2>
      <h3>1) Recovery paths diverged after a common shock</h3>
      <p>NYC climbed back near baseline; SF Bay and Chicago stayed materially below pre-COVID levels.</p>
      {img('01_recovery_trend_pct_baseline.png', 'Monthly Ridership Recovery (% of 2015-2019 baseline)')}

      <h3>2) Trough-to-latest rebound differs by metro</h3>
      <p>All metros collapsed in the same month, but the rebound magnitude is strongest in NYC.</p>
      {img('02_trough_vs_latest.png', 'Collapse and Recovery by Metro')}

      <h3>3) Annual totals still below 2019</h3>
      <p>2025 annual ridership remains below 2019 in all three metros, especially SF Bay and Chicago.</p>
      {img('03_annual_vs_2019.png', 'Annual Ridership Relative to 2019')}

      <h3>4) Mode mix shifted and only partly normalized</h3>
      <p>Bus/ferry shares expanded during the shock; rail-heavy structures recovered more slowly.</p>
      {img('04_mode_share_shift.png', 'Top-Mode Share Shift: Pre-COVID vs Recent')}

      <h3>5) Mode-level recovery is uneven</h3>
      <p>Recent performance varies strongly by mode within each metro, signaling segmented demand recovery.</p>
      {img('05_mode_recovery_heatmap.png', 'Mode Recovery Heatmap')}

      <h3>6) Seasonal strength remains muted</h3>
      <p>Recent month-by-month levels are below pre-COVID seasonal averages across most months outside NYC.</p>
      {img('06_seasonality_profile.png', 'Seasonality Shift: Recent vs Pre-COVID')}
    </section>

    <section class=\"card\">
      <h2>Detailed Findings</h2>
      <ul>
        <li>Latest recovery ({latest_month}): NYC <strong>{latest['NYC']*100:.1f}%</strong>, SF Bay <strong>{latest['SF Bay']*100:.1f}%</strong>, Chicago <strong>{latest['Chicago']*100:.1f}%</strong>.</li>
        <li>Trough month: April 2020 for all three metros.</li>
        <li>2025 annual vs 2019: NYC <strong>{annual_latest['NYC']:.1f}%</strong>, SF Bay <strong>{annual_latest['SF Bay']:.1f}%</strong>, Chicago <strong>{annual_latest['Chicago']:.1f}%</strong>.</li>
      </ul>
      <p class=\"muted\">Generated from processed tables in <code>data/processed/</code> via <code>src/build_report.py</code>.</p>
    </section>
  </div>
</body>
</html>
"""
html_path.write_text(html)

print('Wrote:', md_path)
print('Wrote:', html_path)
print('Figures:', len(list(FIG.glob('*.png'))))
