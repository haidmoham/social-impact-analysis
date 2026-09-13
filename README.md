# Social Vulnerability and Health Outcomes in America

An exploratory notebook joining CDC Social Vulnerability Index (SVI) and CDC PLACES estimates at census-tract level.

## Implemented analysis

[`notebooks/01_phase1_foundation.ipynb`](notebooks/01_phase1_foundation.ipynb) downloads and caches the source data, joins tract FIPS identifiers, and records:

- overall SVI and four theme rankings against six selected health measures;
- a correlation heatmap and diabetes scatterplot with a rolling median;
- sorted within-state SVI/diabetes correlations.

The saved join output contains **78,815 tracts**. Some historical notebook prose and figure captions still say roughly 73,000; those captions are inconsistent with the saved output. Pairwise missingness can make individual correlation sample sizes smaller than the joined table.

Geographic maps, residual models, clustering, and feature-importance experiments are not implemented in the current notebook. State-level interpretation remains deferred. TIGER/Line boundaries are not an input to the implemented calculations.

## Reproduce

Use Python 3.12 and uv:

```bash
git clone https://github.com/haidmoham/social-impact-analysis.git
cd social-impact-analysis
uv sync
uv run jupyter lab notebooks/01_phase1_foundation.ipynb
```

Run the notebook from the repository root or `notebooks/`. It creates ignored `data/raw/`, `data/processed/`, and `outputs/figures/` directories. Reproduction requires the external CDC downloads; the saved outputs are historical results, not a newly validated dataset snapshot.

## Limits

These are observational, area-level associations, not causal effects or individual predictions. Source estimates, missingness, joins, and geographic aggregation affect interpretation. The notebook’s discussion and [`literature_review.md`](literature_review.md) contain proposed explanations that the correlations alone cannot establish. Reconcile source versions, sample counts, and captions before extending or publishing the analysis.
