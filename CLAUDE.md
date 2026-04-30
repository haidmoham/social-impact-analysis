# Project: Social Vulnerability and Health Outcomes

This project is a portfolio piece exploring the relationship between CDC's Social Vulnerability Index (SVI) and health outcomes from CDC PLACES, joined at the census tract level.

## Project Goals

1. Demonstrate solid analytical chops — statistics, regression, clustering
2. Tell a meaningful visual story about health equity in America
3. Build something hiring managers remember

## Phased Approach

- **Phase 1** (this weekend): Foundation analysis — correlations, scatter plots, choropleth map
- **Phase 2**: Geographic deep dive — interactive maps, twin tract analysis
- **Phase 3**: ML layer — clustering, predictive modeling, SHAP explainability
- **Phase 4**: Dashboard + portfolio integration

## Tech Stack

- Python 3.12 via uv
- pandas, numpy, scipy for analysis
- matplotlib, seaborn, plotly for visualization
- geopandas + shapely for geospatial work
- scikit-learn for ML

## Data Conventions

- Raw downloads → `data/raw/` (gitignored)
- Cleaned/joined data → `data/processed/`
- Figures and exports → `outputs/`
- Census tracts identified by FIPS code (11-digit string)
- Always preserve FIPS as string — never let pandas infer as int (loses leading zeros)

## Working Style Reminders

(See ~/CLAUDE_CONTEXT.md for full operating principles)

- Trust-but-verify approach to recommendations
- Explain reasoning, flag confidence levels
- Don't refer to LLMs as "thinking" — pattern matching, not cognition
- Surface tradeoffs, don't oversell

## Specific to This Project

- Prefer matplotlib for static portfolio plots, plotly for interactive
- Always document the "so what" of each finding in markdown cells
- Sanity-check all aggregations against known census stats before trusting results
- Avoid claiming causation — this is observational data
