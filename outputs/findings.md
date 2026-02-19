# Transit Ridership Deep Dive: NYC vs SF Bay vs Chicago

Data source: FTA National Transit Database, Complete Monthly Ridership (dataset 8bui-9xvu).

## Scope
- Metros: NYC, SF Bay, Chicago (UZA-level aggregates).
- Baseline window: January 2015 through December 2019.
- COVID break point: March 2020.

## Key Findings
- NYC: trough at 2020-04 (12.5% of baseline); latest 2025-12 at 89.9% of baseline; 70% recovery: 2022-09; 90% recovery: 2025-09.
- SF Bay: trough at 2020-04 (13.4% of baseline); latest 2025-12 at 66.7% of baseline; 70% recovery: 2020-03; 90% recovery: not reached.
- Chicago: trough at 2020-04 (18.5% of baseline); latest 2025-12 at 62.0% of baseline; 70% recovery: not reached; 90% recovery: not reached.

## Mode Mix Shifts (Top modes by period)
- NYC:
  - pre_2015_2019: HR 65.2%, MB 25.1%, CR 6.6%
  - shock_2020_2021: HR 60.8%, MB 31.2%, CR 5.0%
  - recent_12m: HR 64.4%, MB 26.2%, CR 6.4%
- SF Bay:
  - pre_2015_2019: MB 39.0%, HR 28.6%, TB 11.9%
  - shock_2020_2021: MB 55.6%, HR 16.6%, TB 15.1%
  - recent_12m: MB 42.9%, HR 19.4%, TB 15.6%
- Chicago:
  - pre_2015_2019: MB 47.5%, HR 39.0%, CR 12.2%
  - shock_2020_2021: MB 60.0%, HR 32.6%, CR 6.0%
  - recent_12m: MB 52.8%, HR 35.5%, CR 10.5%

## Agency Concentration (Recent 12 months, Top 3)
- NYC: MTA New York City Transit (81.2%); New Jersey Transit Corporation (6.0%); MTA Bus Company (3.6%)
- SF Bay: City and County of San Francisco (55.4%); San Francisco Bay Area Rapid Transit District (20.0%); Alameda-Contra Costa Transit District (13.2%)
- Chicago: Chicago Transit Authority (83.8%); Northeast Illinois Regional Commuter Railroad Corporation (10.0%); Pace, the Suburban Bus Division of the Regional Transportation Authority (5.4%)

## Output Files
- Processed data: data/processed/monthly_metro_upt.csv
- Recovery summary: data/processed/recovery_summary.csv
- Mode mix summary: data/processed/mode_mix_summary.csv
- Agency concentration: data/processed/agency_top3_recent12m.csv
- Figures: outputs/figures/*.png