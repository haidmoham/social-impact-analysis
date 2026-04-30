# Social Vulnerability and Health Outcomes in America

> Exploring how socioeconomic vulnerability predicts health outcomes at the census tract level using CDC public datasets.

## The Question

Does where you live, in terms of community vulnerability, predict whether you'll develop diabetes, suffer from poor mental health, or struggle with chronic disease?

This analysis uses two complementary CDC datasets to investigate that question:

- **Social Vulnerability Index (SVI)** — 16 demographic indicators measuring community-level socioeconomic vulnerability
- **PLACES** — Estimated prevalence of 36 health outcomes at the census tract level

By joining these two datasets across ~73,000 US census tracts, we can quantify the relationship between social conditions and health outcomes — and surface where the disparities are most severe.

## Project Phases

This is a phased analysis. Each phase builds on the previous one:

### Phase 1 — Foundation (this notebook)
Establish the core relationship: how strongly does SVI predict health outcomes?
- Data acquisition and joining
- Correlation analysis across SVI components and 5–6 health outcomes
- Headline scatter plots and a national choropleth map
- State-level disparity rankings

### Phase 2 — Geographic Deep Dive
Move from "what" to "where."
- Interactive Folium/Plotly maps
- Regional comparisons
- "Twin tracts" analysis: similar vulnerability, divergent outcomes — what explains the gap?

### Phase 3 — Modeling and ML
Add predictive power and explainability.
- K-means clustering to identify "vulnerability archetypes"
- Regression model predicting health outcomes from SVI components
- SHAP values for feature importance and interpretability

### Phase 4 — Polish and Publication
Convert findings into a portfolio-ready story.
- Interactive dashboard linked from mhaider.dev
- Standalone HTML export of notebook
- Written summary for non-technical audiences

## Data Sources

| Dataset | Source | Update Cadence | Granularity |
|---------|--------|----------------|-------------|
| Social Vulnerability Index | [CDC/ATSDR](https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html) | Biennial | Census tract |
| PLACES Health Outcomes | [CDC PLACES](https://www.cdc.gov/places/index.html) | Annual | Census tract |
| Census Tract Boundaries | [US Census TIGER/Line](https://www.census.gov/geographies/mapping-files.html) | Annual | Geography only |

All datasets are public domain or open data. No API keys required.

## Setup

```powershell
# Clone the repo
git clone <repo-url>
cd social-impact-analysis

# Sync the environment (uv reads pyproject.toml + uv.lock)
uv sync

# Open in VS Code
code .
```

Then open `notebooks/01_phase1_foundation.ipynb` and run all cells.

## Project Structure

```
social-impact-analysis/
├── notebooks/
│   └── 01_phase1_foundation.ipynb    # Phase 1 analysis
├── data/
│   ├── raw/                           # Downloaded source data (gitignored)
│   └── processed/                     # Cleaned, joined datasets
├── outputs/
│   └── figures/                       # Exported plots
├── pyproject.toml                     # Project + dependencies
├── uv.lock                            # Pinned versions for reproducibility
└── README.md
```

## Author

Mohammad Haider · [mhaider.dev](https://mhaider.dev) · [LinkedIn](https://linkedin.com/in/haidmoham)
