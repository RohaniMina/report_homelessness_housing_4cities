# Metro Homelessness and Housing Patterns (2011-2026)

## TL;DR
- Long-run PIT homelessness rose in all four cities (2011->2024), highest in Chicago and NYC.
- Phase 2 lagged models suggest prior-year rent pressure is more predictive than same-year rent in this short panel, but coefficients are unstable and inference is weak due small-N/time-series limits.
- Structural break tests identify statistically strong inflection years around 2020-2021 in all cities, aligning with pandemic-era counting/policy shifts and post-2022 intake pressures.
- Policy annotations strengthen interpretation: NYC/Chicago breaks align with shelter-system shocks; SF and LA include major operational/funding pivots; Daniel Lurie period in SF currently has operational metrics but not PIT-year trend data yet.

## Nature of Data, Sources, and Methodology
- `Data`: HUD PIT CoC annual counts; Zillow ZORI metro rent index; NYC daily shelter census; city policy-event annotations (official sources prioritized).
- `Geography`: SF (CA-501), NYC (NY-600), Chicago (IL-510), Los Angeles (CA-600).
- `Window`: PIT 2011-2024; ZORI 2015-2026; NYC daily 2021-03-01 through 2026-02-18; policy events 2016-2025.
- `Phase 2 methods`: city fixed-effects lagged regression, event-indicator augmentation, sensitivity dropping method-warning rows, and Chow structural-break tests by city.
- `Limits`: short panel and potential endogeneity; PIT methodology differs in some years (notably 2021 sheltered-only/partial unsheltered in select CoCs).

## Key Insights + Visuals
1. Long-run growth in PIT homelessness is material across all cities.

![PIT trend](chart_pit_overall_2011_2024.png)
![Growth by city](chart_homeless_pct_change_city.png)

2. 2022->2024 composition differs; NYC/Chicago growth is mostly sheltered.

![Decomposition](chart_2022_2024_decomposition.png)

3. Unsheltered share trends diverge, with LA rising and SF/NYC/Chicago declining.

![Unsheltered share](chart_unsheltered_share_2011_2024.png)

4. Phase 2 model: lagged rent term is directionally positive in homelessness models; same-year rent term is not robust.

![Model coefficients](chart_phase2_model_coefficients.png)

5. Break tests show strongest inflection around 2020-2021 across city series.

![Break tests](chart_phase2_break_tests.png)

6. Policy timeline clarifies likely channels behind breaks and trend changes.

![Policy timeline](chart_policy_event_timeline.png)

7. San Francisco Daniel Lurie period: early operational metrics (2025) show material throughput actions while PIT trend data for his term is not yet available.

![SF Lurie metrics](chart_sf_lurie_operational_metrics.png)

## Phase 2 “What Explains What” Readout
- Baseline events model (`ln_homeless`): lagged rent coef=4.53 (p=0.054); same-year rent coef=-0.01 (p=0.998).
- Sensitivity excluding method-warning rows: lagged rent coef=5.14 (p=0.005).
- Event dummies (`asylum_shock`, `la_emergency`) are directionally plausible in some specs but statistically weak in this sample; treat as suggestive, not causal proof.
- Highest-confidence explanation: structural breaks around 2020-2021 plus policy-event timing indicate institutional/shelter-system regime changes were first-order drivers of recent jumps, especially NYC/Chicago.

## Detailed Findings
### City summary (2011->2024 PIT)
| city          |   start_homeless |   end_homeless |   pct_change_homeless |   pp_change_unsheltered_share |
|:--------------|-----------------:|---------------:|----------------------:|------------------------------:|
| Chicago       |             6635 |          18836 |               183.888 |                     -17.2784  |
| Los Angeles   |            34622 |          71201 |               105.652 |                      18.295   |
| New York City |            51123 |         140134 |               174.111 |                      -2.04195 |
| San Francisco |             5669 |           8323 |                46.816 |                      -7.15088 |

### 2022->2024 decomposition
| city          |   change_total_2022_2024 |   change_sheltered_2022_2024 |   change_unsheltered_2022_2024 |
|:--------------|-------------------------:|-----------------------------:|-------------------------------:|
| Chicago       |                    14961 |                        14590 |                            371 |
| Los Angeles   |                     6090 |                         2459 |                           3631 |
| New York City |                    78294 |                        77352 |                            942 |
| San Francisco |                      569 |                          612 |                            -43 |

### Phase 2 break-test summary
|   break_year |   F_stat |     p_value |   n | city          | series            |
|-------------:|---------:|------------:|----:|:--------------|:------------------|
|         2021 | 34.9261  | 3.0801e-05  |  14 | Chicago       | overall_homeless  |
|         2021 | 29.2024  | 6.67675e-05 |  14 | New York City | overall_homeless  |
|         2020 | 10.1569  | 0.00390659  |  14 | San Francisco | overall_homeless  |
|         2020 |  8.02217 | 0.00834513  |  14 | Los Angeles   | overall_homeless  |
|         2020 |  9.80953 | 0.00438676  |  14 | Los Angeles   | unsheltered_share |
|         2020 |  9.39476 | 0.00505624  |  14 | San Francisco | unsheltered_share |
|         2021 |  6.61931 | 0.0147553   |  14 | Chicago       | unsheltered_share |
|         2021 |  5.02922 | 0.0307974   |  14 | New York City | unsheltered_share |

### Policy events annotation table
| city          | date       | mayor           | event                                                                                       | policy_type                                     | source_type   | confidence   |
|:--------------|:-----------|:----------------|:--------------------------------------------------------------------------------------------|:------------------------------------------------|:--------------|:-------------|
| Chicago       | 2023-05-15 | Brandon Johnson | Johnson administration begins with homelessness funding platform (Bring Chicago Home)       | Administration change / funding proposal        | secondary     | medium       |
| Chicago       | 2024-03-19 | Brandon Johnson | Bring Chicago Home referendum fails                                                         | Funding referendum outcome                      | secondary     | medium       |
| Los Angeles   | 2016-11-08 | Eric Garcetti   | Measure HHH approved to finance supportive housing                                          | Capital funding                                 | official      | high         |
| Los Angeles   | 2022-12-12 | Karen Bass      | Declared state of emergency on homelessness (day one)                                       | Emergency operations                            | official      | high         |
| Los Angeles   | 2022-12-21 | Karen Bass      | Executive Directive 2 launched Inside Safe                                                  | Encampment-to-housing initiative                | official      | high         |
| Los Angeles   | 2023-04-01 | Karen Bass      | Measure ULA transfer tax takes effect                                                       | Funding for housing/homelessness programs       | official      | high         |
| New York City | 2017-11-14 | Bill de Blasio  | Housing New York 2.0 announced (300,000 homes goal)                                         | Housing supply strategy                         | official      | high         |
| New York City | 2022-10-07 | Eric Adams      | Emergency Executive Order 224 declared asylum-seeker emergency                              | Emergency shelter operations                    | official      | high         |
| New York City | 2024-12-05 | Eric Adams      | City of Yes for Housing Opportunity approved by City Council                                | Zoning reform / housing supply                  | official      | high         |
| San Francisco | 2018-11-06 | London Breed    | Proposition C approved (Our City, Our Home Fund)                                            | Funding                                         | official      | high         |
| San Francisco | 2025-01-08 | Daniel Lurie    | Daniel Lurie sworn in as 46th mayor                                                         | Administration change                           | official      | high         |
| San Francisco | 2025-02-12 | Daniel Lurie    | Fentanyl state of emergency ordinance signed; 24/7 stabilization center announced           | Emergency powers + treatment/shelter operations | official      | high         |
| San Francisco | 2025-12-08 | Daniel Lurie    | Mayor update reports 500+ treatment/recovery beds and 1,600+ shelter referrals in 11 months | Operational expansion                           | official      | high         |

### SF Daniel Lurie operational metrics (official release)
| metric                                 |   value | unit                                            | as_of      |
|:---------------------------------------|--------:|:------------------------------------------------|:-----------|
| Treatment and recovery beds opened     |     505 | beds                                            | 2025-12-08 |
| Shelter referrals completed            |    1600 | referrals                                       | 2025-12-08 |
| Encampment offers accepted             |    7560 | accepted offers (estimated from 54% of 14,000+) | 2025-12-08 |
| Tents and makeshift structures removed |     330 | count                                           | 2025-12-08 |

### Mayor-period PIT summary
| city          | mayor                  |   start_year |   end_year |   pct_change_homeless |   pp_change_unsheltered_share |
|:--------------|:-----------------------|-------------:|-----------:|----------------------:|------------------------------:|
| Chicago       | Rahm Emanuel           |         2011 |       2019 |            -20.2713   |                     -2.13475  |
| Chicago       | Lori Lightfoot         |         2020 |       2023 |             13.8961   |                    -12.2409   |
| Chicago       | Brandon Johnson        |         2024 |       2024 |              0        |                      0        |
| Los Angeles   | Antonio Villaraigosa   |         2011 |       2013 |              2.60528  |                     12.3517   |
| Los Angeles   | Eric Garcetti          |         2014 |       2022 |             89.3147   |                      4.77924  |
| Los Angeles   | Karen Bass             |         2023 |       2024 |             -0.166854 |                     -3.80714  |
| New York City | Michael Bloomberg      |         2011 |       2013 |             25.3056   |                     -0.215569 |
| New York City | Bill de Blasio         |         2014 |       2021 |              0.80814  |                     -1.46454  |
| New York City | Eric Adams             |         2022 |       2024 |            126.607    |                     -2.44929  |
| San Francisco | Ed Lee                 |         2011 |       2017 |             20.9737   |                      4.00957  |
| San Francisco | Mark Farrell (interim) |         2018 |       2018 |              0        |                      0        |
| San Francisco | London Breed           |         2019 |       2024 |              3.58432  |                    -12.1551   |

### Rent summary
| city          |   rent_start_year |   rent_end_year |   rent_pct_change |
|:--------------|------------------:|----------------:|------------------:|
| Chicago       |              2015 |            2026 |           51.9577 |
| Los Angeles   |              2015 |            2026 |           59.1567 |
| New York City |              2015 |            2026 |           45.8861 |
| San Francisco |              2015 |            2026 |           33.1439 |

### NYC current-year operational context
- Same-window YTD average shelter census: 2025=86247, 2026=86364, change=0.14% (first 49 days).

## Source Links
- [HUD PIT/AHAR](https://www.huduser.gov/portal/datasets/ahar.html)
- [HUD PIT 2024 page](https://www.huduser.gov/portal/datasets/ahar/2024-ahar-part-1-pit-estimates-of-homelessness-in-the-us.html)
- [NYC DHS Daily Shelter Census](https://data.cityofnewyork.us/d/k46n-sa2m)
- [Zillow ZORI data](https://www.zillow.com/research/data/)
- [SF Our City Our Home](https://www.sf.gov/information/our-city-our-home-oversight-committee)
- [SF Lurie inauguration](https://www.sf.gov/information--mayoral-inauguration-and-public-activities)
- [SF Lurie emergency ordinance](https://www.sf.gov/mayor-lurie-signs-fentanyl-state-of-emergency-ordinance-announces-plan-for-247-police-friendly-stabilization-center)
- [SF Lurie year-one update](https://www.sf.gov/news/mayor-daniel-lurie-delivers-significant-progress-addressing-city-challenges-and-leading-san)
- [NYC Housing New York 2.0](https://www.nyc.gov/office-of-the-mayor/news/722-17/de-blasio-administration-announces-housing-new-york-2-0-three-quarter-million-new-yorkers#/0)
- [NYC EO 224](https://www.nyc.gov/mayors-office/news/2022/10/emergency-executive-order-224)
- [NYC City of Yes passage](https://www.nyc.gov/mayors-office/news/2025/12/most-pro-housing-administration-in-city-history--mayor-adams--ci)
- [LA Measure HHH](https://housing2.lacity.org/residents/measure-hhh)
- [LA emergency declaration](https://mayor.lacity.gov/news/mayor-karen-bass-declares-state-emergency-homelessness)