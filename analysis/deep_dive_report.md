# Homelessness + Housing Deep Dive (SF, NYC, Chicago, Los Angeles)

## Scope
- Window requested: 15 years ending in 2026.
- Comparable homelessness series available: HUD PIT CoC counts through 2024 (annual January count).
- Cities: San Francisco (CA-501), New York City (NY-600), Chicago (IL-510), Los Angeles (CA-600).
- Current-year extension: NYC daily shelter census available through 2026-02-18; comparable daily/weekly series were not successfully retrievable in this run for SF/Chicago/LA.
- Housing pressure proxy: Zillow ZORI metro rent index (available 2015-2026).

## Headline findings
- Chicago: PIT homelessness changed from 6,635 (2011) to 18,836 (2024), a 183.9% change.
- Los Angeles: PIT homelessness changed from 34,622 (2011) to 71,201 (2024), a 105.7% change.
- New York City: PIT homelessness changed from 51,123 (2011) to 140,134 (2024), a 174.1% change.
- San Francisco: PIT homelessness changed from 5,669 (2011) to 8,323 (2024), a 46.8% change.
- Chicago: unsheltered share changed -17.3 percentage points over 2011-2024.
- Los Angeles: unsheltered share changed 18.3 percentage points over 2011-2024.
- New York City: unsheltered share changed -2.0 percentage points over 2011-2024.
- San Francisco: unsheltered share changed -7.2 percentage points over 2011-2024.
- Chicago rent pressure (ZORI) rose 52.0% from 2015 to 2026.
- Los Angeles rent pressure (ZORI) rose 59.2% from 2015 to 2026.
- New York City rent pressure (ZORI) rose 45.9% from 2015 to 2026.
- San Francisco rent pressure (ZORI) rose 33.1% from 2015 to 2026.
- NYC current context: average shelter census in the first 49 days of 2026 is 0.14% vs same 2025 window.

## Mayor-by-mayor pattern (using PIT years in office)
### San Francisco
- Ed Lee (2011-2017 PIT years): 5,669 -> 6,858 (21.0%), unsheltered-share change 4.0 percentage points.
- Mark Farrell (interim) (2018-2018 PIT years): 6,857 -> 6,857 (0.0%), unsheltered-share change 0.0 percentage points.
- London Breed (2019-2024 PIT years): 8,035 -> 8,323 (3.6%), unsheltered-share change -12.2 percentage points.

### New York City
- Michael Bloomberg (2011-2013 PIT years): 51,123 -> 64,060 (25.3%), unsheltered-share change -0.2 percentage points.
- Bill de Blasio (2014-2021 PIT years): 67,810 -> 68,358 (0.8%), unsheltered-share change -1.5 percentage points.
- Eric Adams (2022-2024 PIT years): 61,840 -> 140,134 (126.6%), unsheltered-share change -2.4 percentage points.

### Chicago
- Rahm Emanuel (2011-2019 PIT years): 6,635 -> 5,290 (-20.3%), unsheltered-share change -2.1 percentage points.
- Lori Lightfoot (2020-2023 PIT years): 5,390 -> 6,139 (13.9%), unsheltered-share change -12.2 percentage points.
- Brandon Johnson (2024-2024 PIT years): 18,836 -> 18,836 (0.0%), unsheltered-share change 0.0 percentage points.

### Los Angeles
- Antonio Villaraigosa (2011-2013 PIT years): 34,622 -> 35,524 (2.6%), unsheltered-share change 12.4 percentage points.
- Eric Garcetti (2014-2022 PIT years): 34,393 -> 65,111 (89.3%), unsheltered-share change 4.8 percentage points.
- Karen Bass (2023-2024 PIT years): 71,320 -> 71,201 (-0.2%), unsheltered-share change -3.8 percentage points.

## Focused 2022 to 2024 shift decomposition (total change = sheltered + unsheltered)
- San Francisco: total 569, sheltered 612, unsheltered -43.
- New York City: total 78,294, sheltered 77,352, unsheltered 942.
- Chicago: total 14,961, sheltered 14,590, unsheltered 371.
- Los Angeles: total 6,090, sheltered 2,459, unsheltered 3,631.

## Interpretation
- NYC and Chicago show very large 2024 PIT increases, overwhelmingly in sheltered counts, consistent with post-2022 intake/shelter dynamics.
- Los Angeles is elevated across the full period, with most growth occurring before 2023; PIT is roughly flat from 2023 to 2024.
- SF shows lower total growth than NYC/Chicago/LA and a post-2019 decline in unsheltered share.
- Rent growth is large in all four metros since 2015; trajectories differ by city, so supply/shelter policy and inflow dynamics likely mediate the rent-homelessness link.

## Mayor timeline through current year (2026)
- San Francisco: Ed Lee (2011-01-08 to 2017-12-12), Mark Farrell interim (2018-01-23 to 2018-07-11), London Breed (2018-07-11 to 2025-01-08), Daniel Lurie (2025-01-08 to present).
- New York City: Michael Bloomberg (through 2013-12-31 in this window), Bill de Blasio (2014-01-01 to 2021-12-31), Eric Adams (2022-01-01 to 2025-12-31), Zohran Mamdani (sworn in 2026-01-01, current).
- Chicago: Rahm Emanuel (2011-05-16 to 2019-05-20), Lori Lightfoot (2019-05-20 to 2023-05-15), Brandon Johnson (2023-05-15 to present).
- Los Angeles: Antonio Villaraigosa (through 2013-06-30 in this window), Eric Garcetti (2013-07-01 to 2022-12-11), Karen Bass (2022-12-12 to present).

## Important caveats
- PIT is a single-night annual count, not a full-year prevalence measure.
- 2021 includes sheltered-only or partial-unsheltered methodologies in some CoCs; direct comparison to full unsheltered years is imperfect.
- 2026 does not yet have a tri-city/four-city comparable HUD PIT series in this run; current-year extension relies on NYC operations data.