# Agent instructions

This repository is a portfolio analysis of CDC Social Vulnerability Index data and CDC PLACES health outcomes at the census-tract level.

## Operating contract

- Read `README.md`, `literature_review.md`, and the current notebook before changing analysis or claims.
- Use a trust-but-verify approach. Explain material reasoning, surface tradeoffs, and distinguish verified facts from judgment.
- The human owns method selection, assumptions, interpretation, and final analytical conclusions when those are the learning target.
- Agents may surface well-supported alternatives, flag violated preconditions, implement a chosen method, check calculations, verify citations, and refine a user-authored draft.
- Do not manufacture analytical conclusions or present agent output as evidence.
- For important claims, prefer direct data, reproducible computation, or primary/peer-reviewed sources over model confidence.

## Data conventions

- Raw downloads go in `data/raw/` and remain gitignored.
- Cleaned or joined data goes in `data/processed/`.
- Figures and exports go in `outputs/`.
- Preserve census-tract FIPS as an 11-digit string. Never allow integer inference to remove leading zeros.
- Sanity-check aggregations against known census or CDC totals before trusting them.

## Analysis and writing

- This is observational data. Do not imply causation from association.
- Map major interpretation claims to relevant literature and distinguish established findings from speculation.
- Surface counterintuitive results instead of hiding them.
- Prefer established methods when they answer the question. Do not add complexity for portfolio polish alone.
- Keep public claims methodologically defensible and calibrated to an engineering/data portfolio audience.
- When revising prose, preserve the user's analytical judgment and flag overstatement rather than replacing it with stronger claims.

## Tooling

- Python 3.12 via `uv`.
- Prefer the existing pandas/scipy/geospatial/scikit-learn stack.
- Prefer matplotlib for static portfolio figures and Plotly when interaction adds real value.
- Keep project-local dependencies and conventions in this repository. Cross-project AI-use principles live in Poneglyph.
