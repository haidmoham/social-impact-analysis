# Social Vulnerability & Modeled Health Outcomes

A reproducible, observational analysis of CDC SVI and six CDC PLACES measures at census-tract grain. This first overhaul turns the historical notebook into an audited offline pipeline and a reviewable analytical report.

**Read the [report](reports/generated/report.md)** or open [the self-contained review report](reports/generated/social-vulnerability-health-review.html) locally. Figures, samples, coverage, sensitivity calculations and input fingerprints are checked in alongside it.

The original 78,815-tract join and diabetes tract medians (9.5% below SVI 0.2; 15.6% above 0.8) reproduce. Coverage is **48 states and DC**: Kentucky and Pennsylvania are absent for the six selected 2023 outcomes. This is a contrast between modeled tract estimates, not individual relative risk, national population prevalence, or a causal effect.

## Reproduce the reviewed snapshot

Use Python 3.12 and the existing uv environment:

```powershell
uv sync --locked
uv run python scripts/analyze.py
```

Place the original public aggregate caches in `data/raw/svi_2022.csv` and `data/raw/places_2024.csv`. Raw and processed files remain gitignored. The misleading PLACES filename is preserved to identify the original cache: selected observations are from 2023, consistent with the currently documented 2025 release. All 472,890 selected records match CDC’s official current 2025 dataset, including confidence limits. The SVI cache is byte-identical to the official 2022 US tract download, confirming national rank scope. Original acquisition date and unused PLACES measures remain unauthenticated.

[source_manifest.json](source_manifest.json) pins SHA-256 hashes and source URLs. A rolling CDC download may differ; the runner refuses changed fingerprints rather than silently recomputing under the old label. The exact cache is not distributed here, so a fresh clone cannot reproduce numbers without matching files. Review and deliberately update the manifest for a new snapshot. No paid service, credential or network access is required by the analysis itself.

For another cache/output location:

```powershell
uv run python scripts/analyze.py --raw-dir C:\path\to\raw --output-dir C:\path\to\report
```

The runner validates FIPS, grain, years, estimate type, sentinels, ranges and interval ordering. It produces:

- Coverage by state and unmatched identifiers; pairwise n for every association.
- Pearson/Spearman correlations, state/county centering, and a coarse age-composition partial correlation.
- Unweighted vulnerability-band medians and interquartile ranges; state association strength beside tract medians and samples.
- CDC interval-width summaries and retained endpoints in `data/processed/selected_places_with_intervals.csv`.
- Three SVG charts, an HTML/Markdown report, CSV evidence and software/input provenance in `reports/generated/`.

## Interpretation and scope

PLACES is modeled adult prevalence using demographic and geographic predictors that overlap SVI inputs. The estimates are not direct tract disease counts or independent validation of SVI. Geographic dependence and unavailable joint draws limit aggregate uncertainty; no causal interpretation, individual prediction, independence-based p-values or invented confidence bands are provided.

The [historical notebook](notebooks/01_phase1_foundation.ipynb) retains saved outputs and an archival warning. Findings are reconciled in [the audit](reports/overhaul_audit.md). The [literature review](literature_review.md) is an unverified historical research aid, not a source of approved claims.

This bounded upgrade borrows validation and uncertainty display from Indigo Circuit and dated evidence/inference separation from Log Pose. It adds no warehouse, service, predictive model, map infrastructure or portfolio restructuring. Investigate residual unmatched tracts and exact boundary equivalence before publication or extension.

For an explicit network provenance comparison, run `uv run python scripts/authenticate_sources.py` after the offline analysis. It downloads official public records separately and preserves the original caches. Results are in `reports/generated/source_authentication.json`.
