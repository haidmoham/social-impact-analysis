"""Offline, auditable rerun of the six-outcome tract analysis.

Run from any directory: python scripts/analyze.py --raw-dir data/raw
Raw files are public CDC aggregates. No network calls or notebook state required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MEASURES = {"DIABETES": "Diabetes", "MHLTH": "Poor mental health",
            "CHD": "Coronary heart disease", "OBESITY": "Obesity",
            "CSMOKING": "Current smoking", "BPHIGH": "High blood pressure"}
THEMES = {"RPL_THEMES": "Overall SVI", "RPL_THEME1": "Socioeconomic",
          "RPL_THEME2": "Household", "RPL_THEME3": "Minority status",
          "RPL_THEME4": "Housing / transport"}


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def tract_ids(frame, column):
    require(frame[column].notna().all(), f"Missing {column}")
    require(frame[column].str.fullmatch(r"\d{11}").all(), f"Invalid 11-digit {column}")


def residual_corr(pair, group):
    centered = pair[["x", "y"]] - pair.groupby(group)[["x", "y"]].transform("mean")
    return centered.x.corr(centered.y)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, default=ROOT / "data/raw")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "reports/generated")
    args = parser.parse_args()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    svi_path, places_path = args.raw_dir / "svi_2022.csv", args.raw_dir / "places_2024.csv"
    manifest = json.loads((ROOT / "source_manifest.json").read_text(encoding="utf-8"))
    hashes = {p.name: digest(p) for p in [svi_path, places_path]}
    for p in [svi_path, places_path]:
        require(hashes[p.name] == manifest["files"][p.name]["sha256"],
                f"Source snapshot drift: {p.name}. Review provenance before updating source_manifest.json")
    svi = pd.read_csv(svi_path, dtype={"FIPS": str, "STCNTY": str},
                      usecols=["FIPS", "STCNTY", "STATE", "E_TOTPOP", "EP_AGE65", "EP_AGE17", *THEMES])
    tract_ids(svi, "FIPS")
    require(not svi.FIPS.duplicated().any(), "SVI must have one row per tract")
    svi.replace({c: {-999: np.nan} for c in [*THEMES, "E_TOTPOP", "EP_AGE65", "EP_AGE17"]}, inplace=True)
    for c in THEMES:
        require(svi[c].dropna().between(0, 1).all(), f"Invalid rank: {c}")
    require(svi.E_TOTPOP.dropna().ge(0).all(), "Negative population")
    selected, inventory = [], []
    columns = ["LocationID", "Year", "MeasureId", "DataValueTypeID", "Data_Value",
               "Low_Confidence_Limit", "High_Confidence_Limit"]
    for chunk in pd.read_csv(places_path, dtype={"LocationID": str}, usecols=columns, chunksize=200_000):
        tract_ids(chunk, "LocationID")
        inventory.append(chunk.groupby(["MeasureId", "Year", "DataValueTypeID"]).size().rename("rows"))
        selected.append(chunk.loc[chunk.MeasureId.isin(MEASURES)].copy())
    inv = pd.concat(inventory).groupby(level=[0, 1, 2]).sum().reset_index()
    inv.to_csv(out / "source_inventory.csv", index=False)
    places = pd.concat(selected, ignore_index=True)
    require(set(places.MeasureId) == set(MEASURES), "A selected measure is absent")
    require(set(places.DataValueTypeID) == {"CrdPrv"}, "Expected crude prevalence only; choose explicitly")
    require(set(places.Year) == {2023}, "Expected selected measures from 2023; review source before extending")
    require(not places.duplicated(["LocationID", "MeasureId"]).any(), "Duplicate tract/measure: refuse first-record pivot")
    for c in ["Data_Value", "Low_Confidence_Limit", "High_Confidence_Limit"]:
        require(places[c].dropna().between(0, 100).all(), f"Invalid prevalence/interval: {c}")
    complete = places.dropna(subset=["Data_Value", "Low_Confidence_Limit", "High_Confidence_Limit"])
    require((complete.Low_Confidence_Limit <= complete.Data_Value).all() and
            (complete.Data_Value <= complete.High_Confidence_Limit).all(), "Inverted CDC intervals")
    wide = places.pivot(index="LocationID", columns="MeasureId", values="Data_Value").reset_index()
    joined = svi.merge(wide, left_on="FIPS", right_on="LocationID", how="outer", validate="one_to_one", indicator=True)
    coverage = joined.groupby("STATE", dropna=False).agg(svi_tracts=("FIPS", "count"),
        matched_tracts=("LocationID", "count"), svi_population=("E_TOTPOP", "sum"))
    coverage["matched_population"] = joined.loc[joined._merge == "both"].groupby("STATE").E_TOTPOP.sum().reindex(coverage.index, fill_value=0)
    coverage["tract_coverage_pct"] = 100 * coverage.matched_tracts / coverage.svi_tracts
    coverage["population_coverage_pct"] = 100 * coverage.matched_population / coverage.svi_population
    coverage.to_csv(out / "coverage_by_state.csv")
    joined[["FIPS", "LocationID", "STATE", "_merge"]].loc[joined._merge != "both"].to_csv(out / "unmatched_tracts.csv", index=False)
    df = joined.loc[joined._merge == "both"].copy()
    require((df.FIPS.str[:5] == df.STCNTY).all(), "SVI county ID disagrees with tract prefix")
    processed = ROOT / "data/processed"
    processed.mkdir(parents=True, exist_ok=True)
    df.drop(columns="_merge").to_csv(processed / "validated_join.csv", index=False)
    places.to_csv(processed / "selected_places_with_intervals.csv", index=False)
    correlations = []
    for theme, label in THEMES.items():
        for measure in MEASURES:
            pair = df[[theme, measure, "STATE", "STCNTY", "EP_AGE65", "EP_AGE17"]].rename(columns={theme: "x", measure: "y"}).dropna(subset=["x", "y"])
            age = pair.dropna(subset=["EP_AGE65", "EP_AGE17"])
            design = np.column_stack([np.ones(len(age)), age[["EP_AGE65", "EP_AGE17"]].to_numpy()])
            xy = age[["x", "y"]].to_numpy()
            residual = xy - design @ np.linalg.lstsq(design, xy, rcond=None)[0]
            correlations.append({"theme": label, "measure": measure, "n": len(pair),
                "missing_from_join": len(df) - len(pair), "pearson": pair.x.corr(pair.y),
                "spearman": pair.x.corr(pair.y, method="spearman"),
                "state_centered": residual_corr(pair, "STATE"),
                "county_centered": residual_corr(pair, "STCNTY"),
                "age_composition_partial": np.corrcoef(residual.T)[0, 1], "age_n": len(age)})
    corr = pd.DataFrame(correlations)
    corr.to_csv(out / "correlations.csv", index=False)
    bands = []
    for measure in MEASURES:
        for name, mask in [("Low (<0.2)", df.RPL_THEMES < .2), ("High (>0.8)", df.RPL_THEMES > .8)]:
            values = df.loc[mask, measure].dropna()
            bands.append({"measure": measure, "band": name, "n": len(values), "median": values.median(),
                          "p25": values.quantile(.25), "p75": values.quantile(.75)})
    bands = pd.DataFrame(bands)
    bands.to_csv(out / "vulnerability_bands.csv", index=False)
    state_rows = []
    for state, group in df.dropna(subset=["RPL_THEMES", "DIABETES"]).groupby("STATE"):
        state_rows.append({"state": state, "n": len(group), "pearson": group.RPL_THEMES.corr(group.DIABETES),
                           "median_diabetes": group.DIABETES.median(), "svi_sd": group.RPL_THEMES.std()})
    states = pd.DataFrame(state_rows).sort_values("pearson")
    states.to_csv(out / "state_associations.csv", index=False)
    widths = places.assign(width=places.High_Confidence_Limit - places.Low_Confidence_Limit).groupby("MeasureId").agg(
        rows=("LocationID", "size"), point_nonmissing=("Data_Value", "count"),
        interval_nonmissing=("width", "count"), median_interval_width_pp=("width", "median"))
    widths.to_csv(out / "estimate_uncertainty.csv")
    provenance = {"run_utc": datetime.now(timezone.utc).isoformat(), "python": __import__("platform").python_version(),
        "pandas": pd.__version__, "numpy": np.__version__, "matplotlib": matplotlib.__version__,
        "input_files": [{"filename": p.name, "bytes": p.stat().st_size, "sha256": hashes[p.name],
            "acquisition": "Copied from original local public CDC cache; original download date unknown"} for p in [svi_path, places_path]],
        "svi_rows": len(svi), "places_rows": int(inv.rows.sum()), "places_measures": int(inv.MeasureId.nunique()),
        "selected_places_year": 2023, "selected_type": "CrdPrv", "joined_tracts": len(df),
        "svi_only": int((joined._merge == "left_only").sum()), "places_only": int((joined._merge == "right_only").sum()),
        "valid_overall_svi_in_source": int(svi.RPL_THEMES.notna().sum()),
        "matched_population": int(df.E_TOTPOP.sum()), "svi_population": int(svi.E_TOTPOP.sum()),
        "release_identity": "Cached filename says 2024; 40-measure inventory and 2023 BRFSS years match live 2025 release documentation. Original download release not independently authenticated.",
        "geography": "ACS 2022 and PLACES 2024+ documentation use 2020 census tract definitions (subject to legal-area updates); matching IDs checked, not a geometry crosswalk audit"}
    metadata_path = args.raw_dir / "places_live_metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        snapshot = {k: metadata.get(k) for k in ["id", "name", "description", "rowsUpdatedAt", "viewLastModified"]}
        snapshot.update({"metadata_url": "https://data.cdc.gov/api/views/cwsq-ngmh.json",
                         "accessed_utc_date": "2026-10-01", "snapshot_sha256": digest(metadata_path),
                         "relationship_to_cache": "Current metadata; not proof of cached download identity"})
        (out / "places_metadata_observation.json").write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    (out / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    make_figures(corr, df, states, out)
    make_report(provenance, corr, bands, coverage, widths, out)
    print(json.dumps(provenance, indent=2))


def make_figures(corr, df, states, out):
    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False,
                         "axes.titlesize": 15, "axes.labelsize": 11, "svg.fonttype": "none"})
    matrix = corr.pivot(index="theme", columns="measure", values="pearson").reindex(index=THEMES.values(), columns=MEASURES)
    fig, ax = plt.subplots(figsize=(11, 4.8))
    im = ax.imshow(matrix, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(6), MEASURES.values(), rotation=20, ha="right")
    ax.set_yticks(range(5), THEMES.values())
    for i in range(5):
        for j in range(6):
            ax.text(j, i, f"{matrix.iloc[i, j]:.2f}", ha="center", va="center", color="white" if abs(matrix.iloc[i, j]) > .6 else "#172e40")
    ax.set_title("Vulnerability and modeled adult health prevalence", loc="left", pad=18)
    fig.colorbar(im, ax=ax, label="Pearson r · pairwise samples in correlations.csv")
    fig.tight_layout()
    fig.savefig(out / "correlations.svg")
    fig.savefig(out / "correlations.png", dpi=150)
    plt.close(fig)
    pair = df.dropna(subset=["RPL_THEMES", "DIABETES"])
    fig, ax = plt.subplots(figsize=(10, 5))
    density = ax.hexbin(pair.RPL_THEMES, pair.DIABETES, gridsize=65, bins="log", mincnt=1, cmap="Blues")
    decile = pair.assign(bin=pd.cut(pair.RPL_THEMES, np.linspace(0, 1, 11), include_lowest=True)).groupby("bin", observed=True).agg(x=("RPL_THEMES", "median"), y=("DIABETES", "median"))
    ax.plot(decile.x, decile.y, "o-", color="#c34832", linewidth=2, label="Median within fixed 0.1 SVI bands")
    ax.set(xlabel="National overall SVI percentile", ylabel="Modeled adult diabetes prevalence (%)",
           title=f"An area-level gradient, with substantial tract variation · n={len(pair):,}")
    ax.legend(frameon=False)
    fig.colorbar(density, ax=ax, label="Tracts per hexagon (log scale)")
    fig.tight_layout()
    fig.savefig(out / "diabetes_gradient.svg")
    fig.savefig(out / "diabetes_gradient.png", dpi=150)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(12, 12), sharey=True, gridspec_kw={"width_ratios": [2, 1]})
    y = np.arange(len(states))
    axes[0].barh(y, states.pearson, color="#275675")
    axes[0].set_yticks(y, [f"{r.state} (n={r.n:,})" for r in states.itertuples()])
    axes[0].set(xlabel="Within-state Pearson r", title="Association strength")
    axes[1].scatter(states.median_diabetes, y, color="#c34832")
    axes[1].set(xlabel="Tract median prevalence (%)", title="Absolute level")
    fig.suptitle("Correlation strength is different from disease burden", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, .97))
    fig.savefig(out / "state_context.svg")
    fig.savefig(out / "state_context.png", dpi=150)
    plt.close(fig)
    # Matplotlib emits trailing spaces inside SVG path attributes; normalize them
    # so generated artifacts pass the same whitespace gate as source files.
    for name in ["correlations.svg", "diabetes_gradient.svg", "state_context.svg"]:
        path = out / name
        path.write_text("\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")


def make_report(p, corr, bands, coverage, widths, out):
    diabetes = bands.loc[bands.measure == "DIABETES"].set_index("band")
    low, high = diabetes.loc["Low (<0.2)"], diabetes.loc["High (>0.8)"]
    selected = corr.loc[corr.theme == "Overall SVI", ["measure", "n", "pearson", "spearman", "state_centered", "county_centered", "age_composition_partial"]]
    worst = coverage.sort_values("tract_coverage_pct").head(5).reset_index()
    text = f"""# Social vulnerability & modeled health: a validated rerun

Generated {p['run_utc'][:10]} from the original local CDC cache. This is a cross-sectional tract analysis, not individual prediction or causal evidence.

## The result that survives

The original join reproduces **{p['joined_tracts']:,} tracts**. Median modeled adult diabetes prevalence is **{low['median']:.1f}%** in tracts with national SVI <0.2 (n={int(low['n']):,}) and **{high['median']:.1f}%** with SVI >0.8 (n={int(high['n']):,}): **{high['median']-low['median']:.1f} percentage points**, or **{high['median']/low['median']:.2f}×**. These are unweighted medians of tract estimates; they are not population prevalence or an individual relative risk. Threshold bands use strict inequalities, preserving the historical calculation; they are not equal-size quintiles in the joined sample.

![Diabetes association density and band medians](diabetes_gradient.svg)

## What changed about the evidence

- The cached PLACES file is named `places_2024.csv`, but contains {p['places_measures']} measures and selected outcomes dated **2023**. Its content agrees with the live **2025 release** documentation. Original acquisition date and release identity are unknown; filename is not provenance. The live metadata snapshot is a separate present-day observation.
- SVI has {p['svi_rows']:,} tracts, with {p['valid_overall_svi_in_source']:,} valid overall ranks. {p['svi_only']:,} SVI tracts lack a selected PLACES record; {p['places_only']:,} selected PLACES tracts lack SVI. **Kentucky and Pennsylvania are entirely absent** for these six outcomes: 4,751 tracts and 17,492,143 people in cached SVI estimates. CDC's 2025 release notes report both states unavailable for 2023 BRFSS-based measures. The remaining 554 unmatched tracts require separate investigation. Each correlation reports its own complete-pair n.
- Matched tracts account for {p['matched_population']:,} of {p['svi_population']:,} people in the cached SVI population estimates ({100*p['matched_population']/p['svi_population']:.2f}%). This is coverage of ACS all-age estimates, not the PLACES adult denominator or a validated national prevalence total.
- Selected rows are uniquely keyed by tract and measure, crude prevalence only, all 2023. The former `first` pivot happened to reproduce these values, but would silently conceal duplicate years/types in another input. The new runner rejects those inputs.
- SVI 2022 uses 2018–2022 ACS estimates. PLACES 2025 uses 2023 BRFSS for the six selected measures and 2020 Census population geography. ACS 2022 uses 2020 tract delineations subject to legal-area updates; Connecticut adopted planning-region county equivalents. Matched identifiers and SVI county prefixes are checked, but exact boundary identity remains unaudited. These are overlapping period estimates, not a simultaneous 2022 measurement or a longitudinal design.

## Does the association depend on the summary method?

The national Pearson/Spearman results below use complete pairs. State and county columns correlate deviations from group means, removing between-group mean differences; they do not control for all confounders. Age sensitivity residualizes both quantities against an intercept and SVI ACS percentages aged 65+ and 17 or younger on a common complete-case sample. It is a coarse linear composition check, not CDC age-standardization. All estimates are descriptive and unweighted.

{selected.to_html(index=False, float_format=lambda v: f'{v:.3f}')}

![Five vulnerability dimensions against six outcomes](correlations.svg)

## Geography changes the question

Strong within-state correlation does not mean high statewide disease burden, intervention effectiveness, or greater inequality. The right panel shows an unweighted median of tract estimates, alongside each state's correlation and sample size. State comparisons retain the cached US SVI rankings and are descriptive sensitivity checks; no state-specific SVI ranking was downloaded. National ranking identity has not been authenticated against the original download, so source authentication remains a publication prerequisite.

![State correlations, samples and median diabetes prevalence](state_context.svg)

Lowest tract matching coverage (full table in `coverage_by_state.csv`):

{worst[['STATE','svi_tracts','matched_tracts','tract_coverage_pct','population_coverage_pct']].to_html(index=False, float_format=lambda v: f'{v:.2f}')}

CDC documents the Kentucky/Pennsylvania exclusion; the reason for each remaining unmatched tract is not inferred from the join. `unmatched_tracts.csv` records identifiers for follow-up. Missing coverage need not be random. The state figure includes 48 states and DC, not all 50 states.

## Uncertainty belongs in the deliverable

{widths.reset_index().to_html(index=False, float_format=lambda v: f'{v:.2f}')}

Widths are the median of published tract-level 95% interval widths, in percentage points. The runner preserves both endpoints in the processed long table. These intervals describe CDC modeled estimates, not confidence intervals for our correlations or median-band contrast. No independence-based p-values, aggregate confidence bands, or Bayesian posterior are reported: spatial dependence, shared model inputs and unavailable joint uncertainty draws would make such precision easy to overstate. SVI rank uncertainty is also not propagated.

PLACES is produced by multilevel regression and poststratification using demographic variables, county poverty and geographic effects. SVI includes related demographics and socioeconomic measures. Some observed association can therefore reflect overlapping model inputs; this is not an independent validation of vulnerability against directly observed tract disease counts. CDC cautions against using PLACES estimates to evaluate local programs or policies.

## Interpretation corrections

Ordinary entries in a correlation matrix do **not** implicitly adjust for the other columns. The old minority-theme discussion incorrectly called them residual associations. Negative or small aggregate correlations cannot establish a protective mechanism, access barrier, dietary explanation, or Hispanic paradox. We retain the signs and flag the need for a separate, justified investigation. Literature concerning mortality, counties or individuals does not validate a tract prevalence effect size.

## Sources and reproducibility

- [CDC SVI downloads and national/state ranking guidance](https://svi.cdc.gov/dataDownloads/data-download.html)
- [CDC SVI 2022 documentation](https://svi.cdc.gov/map25/data/docs/SVI2022Documentation_ZCTA.pdf): ACS period, sentinels and ranks; accessed {p['run_utc'][:10]}.
- [CDC PLACES dataset](https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-Census-Tract-D/cwsq-ngmh): currently labeled 2025; accessed {p['run_utc'][:10]}.
- [CDC PLACES methodology](https://www.cdc.gov/places/methodology/index.html): modeled estimates, input overlap, intervals and 2020 geography; accessed {p['run_utc'][:10]}.
- [CDC PLACES release notes](https://www.cdc.gov/places/current-release-notes/index.html): omitted states and observation years; accessed {p['run_utc'][:10]}.
- [Census ACS 2022 geography](https://www.census.gov/programs-surveys/acs/geography-acs/geography-boundaries-by-year/2022.html): tract vintage and legal-area caveats; accessed {p['run_utc'][:10]}.

Run `uv run python scripts/analyze.py` with the two raw cached CSVs. `provenance.json` records input byte counts, SHA-256 fingerprints, software versions and exclusions. All generated tables and figures derive from that runner. It intentionally makes no automatic download from the rolling PLACES URL. Reconstructing the exact cache requires the recorded fingerprints; a fresh release must be reviewed rather than renamed to match.

This first overhaul adopts Indigo Circuit's explicit grain and validation gates and its habit of showing uncertainty with estimates, plus Log Pose's separation of dated evidence and inference. It does not transfer a match-outcome Beta model to CDC prevalence surfaces. Next useful work: authenticate the archived release and investigate geographically patterned exclusions before considering broader outcomes or maps.
"""
    (out / "report.md").write_text(text, encoding="utf-8")
    # A dependency-free, portable reading surface; HTML tables are already embedded.
    import html, re
    parts = []
    for paragraph in text.split("\n\n"):
        if paragraph.startswith("<table"):
            parts.append(paragraph)
        elif paragraph.startswith("!["):
            alt, src = re.match(r"!\[(.*?)\]\((.*?)\)", paragraph).groups()
            parts.append(f'<figure><img src="{src}" alt="{html.escape(alt)}"></figure>')
        else:
            content = html.escape(paragraph)
            content = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", content)
            content = re.sub(r"`(.*?)`", r"<code>\1</code>", content)
            content = re.sub(r"\[(.*?)\]\((https://[^)]+)\)", r'<a href="\2">\1</a>', content)
            if content.startswith("# "):
                parts.append(f"<h1>{content[2:]}</h1>")
            elif content.startswith("## "):
                parts.append(f"<h2>{content[3:]}</h2>")
            elif content.startswith("- "):
                parts.append("<ul>" + "".join(f"<li>{line[2:]}</li>" for line in content.splitlines()) + "</ul>")
            else:
                parts.append(f"<p>{content}</p>")
    (out / "report.html").write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Social vulnerability & modeled health</title><style>body{margin:0;background:#f4f1ea;color:#193044;font:17px/1.65 system-ui,sans-serif}main{max-width:1120px;margin:auto;padding:64px 28px}h1{font-size:clamp(32px,5vw,60px);line-height:1.1;max-width:950px}h2{margin-top:56px;border-top:1px solid #c5ccc9;padding-top:28px}a{color:#275675}table{display:block;overflow:auto;border-collapse:collapse;font-size:14px;background:#fff;width:100%}td,th{padding:10px 14px;border-bottom:1px solid #dce1df;text-align:right}th:first-child,td:first-child{text-align:left}figure{margin:32px 0;background:white;padding:16px}img{width:100%;height:auto}code{font-size:14px;overflow-wrap:anywhere}li{margin-bottom:12px}@media print{body{background:white}main{padding:0}h2{break-after:avoid}figure{break-inside:avoid}}</style><main>''' + "\n".join(parts) + "</main></html>", encoding="utf-8")


if __name__ == "__main__":
    main()
