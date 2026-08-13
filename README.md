# Social Vulnerability and Health Outcomes in America

Analysis of how community-level social vulnerability relates to health outcomes across U.S. census tracts.

## Data

- **CDC/ATSDR Social Vulnerability Index (SVI)** — demographic and socioeconomic vulnerability indicators.
- **CDC PLACES** — estimated prevalence of health outcomes at the census-tract level.
- **U.S. Census TIGER/Line** — tract boundaries for geographic output.

The analysis joins the datasets across roughly 73,000 census tracts.

## Analysis

- correlation between SVI components and selected health outcomes;
- state and regional comparisons;
- geographic visualization;
- tract-level modeling and residual analysis;
- clustering and feature-importance experiments where useful.

## Setup

```bash
git clone <repo-url>
cd social-impact-analysis
uv sync
code .
```

Open `notebooks/01_phase1_foundation.ipynb` and run the notebook.

## Structure

```text
notebooks/
data/
  raw/
  processed/
outputs/
  figures/
pyproject.toml
uv.lock
```

Source datasets are public CDC and U.S. Census data.

## Reproduce and interpret

Start with `notebooks/01_phase1_foundation.ipynb`; it is the technical entry point for data preparation and the initial analysis. Interpret tract-level relationships as observational associations, not causal effects. Dataset estimates, joins, missingness, and geographic aggregation can all affect the results.
