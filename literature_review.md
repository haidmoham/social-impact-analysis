# Literature Review — Phase 1 Context

> Curated peer-reviewed sources to layer academic nuance onto the technical findings. Use these to inform the markdown interpretation cells in the notebook (the TODOs).

The notebook produced four findings worth contextualizing:
1. SVI strongly correlates with diabetes (1.64x ratio between vulnerable and non-vulnerable tracts)
2. Socioeconomic theme dominates over other SVI themes
3. Minority Status theme has near-zero or slightly negative correlation with several outcomes
4. The South + DC show the sharpest within-state SVI→diabetes relationships

For each finding below: the headline you can claim with confidence, the specific source(s) supporting it, and the nuance/caveat that elevates the interpretation beyond "I ran a correlation."

---

## Finding 1: SVI predicts diabetes prevalence

**What you found:** Diabetes prevalence is 1.64x higher in highly-vulnerable tracts (15.6%) vs. low-vulnerability tracts (9.5%).

**Established in the literature:**
- Bevan et al. (2024), *Journal of the American Heart Association* — quantified SVI's relationship to diabetes-related cardiovascular mortality, finding social vulnerability "exacerbates the health burden associated with CVDs and diabetes" via medication affordability, treatment compliance, and healthcare navigation barriers.
  → https://www.ahajournals.org/doi/10.1161/JAHA.123.029649
- Ji et al. (2025), examining National Diabetes Prevention Program access — found counties with high SVI had **2.63x higher odds** of having no organizations with full DPP recognition, suggesting the disparity is reinforced by unequal access to evidence-based prevention infrastructure.
  → https://pmc.ncbi.nlm.nih.gov/articles/PMC11936411/

**The nuance to add:**
The 1.64x ratio you measured isn't just a correlation — there's a documented mechanism. Vulnerable communities have less access to diabetes prevention programs, so the disparity compounds over time. Your finding is a snapshot of an active equity gap, not a static demographic fact.

**Caveat to flag explicitly:**
SDOH research literature suggests socioeconomic factors alone may account for 47 percent of health outcomes, while clinical care impacts only about 20 percent of county-level variation. The SVI captures part — but not all — of the SDOH picture. Adding nuance about what SVI doesn't capture (healthcare access infrastructure specifically, food environment, environmental exposures) is a sophisticated move.

---

## Finding 2: Socioeconomic theme dominates the predictive signal

**What you found:** The socioeconomic theme (poverty, unemployment, low education, no health insurance) has the strongest correlations across outcomes — particularly diabetes (0.60), poor mental health (0.68), and smoking (0.65).

**Established in the literature:**
- Cromer et al. (2026), *medRxiv* — applied Healthy People 2030 framework to All of Us survey data, found "**income and education generally captured the majority of disease-related signal** from more complex individual-level data." Worth citing specifically because it tested whether more nuanced individual-level data outperformed area-level socioeconomic measures — and largely it didn't.
  → https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12869669/
- HHS ASPE Report (2022) — found social and economic factors accounted for two of the three largest impacts on health and life expectancy.
  → https://aspe.hhs.gov/sites/default/files/documents/e2b650cd64cf84aae8ff0fae7474af82/SDOH-Evidence-Review.pdf
- The SDOH framing is so well-established that educational attainment is often used as a proxy measure of socioeconomic status when more complete measures are lacking.

**The nuance to add:**
Your finding aligns with decades of social epidemiology. The "fundamental causes" framework (Link & Phelan, 1995) argues that socioeconomic status is a *fundamental* determinant of health because resources (money, knowledge, power, social connections) can be deployed flexibly against whatever health threat is most salient at the moment. Even when specific risk factors change (smoking → COVID → opioids), the SES gradient persists.

**Why this matters for interpretation:**
Don't oversell "socioeconomic vulnerability causes diabetes." The cleaner framing: socioeconomic resources are a *fundamental* determinant of which communities can effectively respond to diabetes risk. This is more accurate and reflects mechanism.

---

## Finding 3: Minority Status theme shows near-zero/negative correlations

**What you found:** Minority Status correlates -0.19 with coronary heart disease, -0.05 with high blood pressure — counterintuitive given racial health disparity literature.

**Why this happens (the analytically important point):**
This finding doesn't contradict the racial health disparity literature — it reflects how SVI's Minority Status theme is constructed and how it interacts with the socioeconomic theme.

The research literature consistently finds that observed racial disparities in health are **mediated through socioeconomic factors**:
- The Florida diabetes investigation (Owusu Sekyere et al., 2020) found that observed racial and ethnic diabetes disparities may be a reflection of differences in socioeconomic factors that are associated with race.
  → https://pmc.ncbi.nlm.nih.gov/articles/PMC7425001/
- The Wikipedia synthesis (well-cited): Overall, racial health disparities appear to be rooted in social disadvantages associated with race such as implicit stereotyping and average differences in socioeconomic status.

**The mechanism — this is the key interpretive move:**
When you control for socioeconomic theme (which is partially done implicitly when both themes are in the same correlation matrix), the residual variance in Minority Status that's *not* explained by SES sometimes correlates with health protective factors — possibly reflecting:
1. **Hispanic Paradox**: Despite socioeconomic disadvantage, Hispanic populations in the US show better-than-expected outcomes for some chronic diseases.
2. **Geographic confounding**: Some highly-Hispanic areas (parts of California, Texas) have specific food and lifestyle patterns associated with lower CHD risk.
3. **Selection effects**: Immigrant health advantages (the "healthy immigrant effect").

**What to actually write in the notebook:**
A sophisticated interpretation does NOT say "minority status doesn't matter for health." It says: "When examined alongside socioeconomic vulnerability, the Minority Status theme's residual association with several outcomes is small or slightly negative — consistent with research showing that racial health disparities operate primarily through socioeconomic mechanisms rather than through demographics directly. The Hispanic Paradox literature is relevant here."

This interpretation flexes statistical thinking AND domain knowledge.

---

## Finding 4: Geographic concentration in the South + DC

**What you found:** DC, Connecticut, Louisiana, Texas, Ohio, New Jersey, Alabama show the sharpest within-state SVI→diabetes correlations.

**Established in the literature:**
- The "Diabetes Belt" is a documented epidemiological region: In 2010, high prevalence of diagnosed diabetes was concentrated primarily in 644 counties within 15 southern states. The prevalence was 40% higher in this 'diabetes belt' (11.7%) compared to the average of all other U.S.
  → https://pmc.ncbi.nlm.nih.gov/articles/PMC5807217/
- Myers et al. (2017) found that the *predictors* of diabetes prevalence differ inside vs. outside the Diabetes Belt — meaning the same SVI score doesn't translate to diabetes risk uniformly across geography.
  → https://pmc.ncbi.nlm.nih.gov/articles/PMC5269515/
- Lord & Roberson (2022) examined regional variation and concluded the magnitude of the effect of these factors on the diabetes risks varied markedly across the four geographic regions.
  → https://pmc.ncbi.nlm.nih.gov/articles/PMC9126863/

**The nuance to add:**
Your state-level chart shows mostly southern states topping the list — this is consistent with the established "Diabetes Belt" literature. The interesting outliers are:
- **DC** at the top — consistent with extreme intra-city inequality (Wards 7-8 vs. NW DC) producing strong within-jurisdiction gradients
- **Connecticut** unexpectedly high — likely reflecting Hartford/New Haven vs. wealthy suburbs; an inequality story rather than a Southern-belt story
- **Vermont, Wyoming, North Dakota** at bottom — likely homogeneous demographics produce smaller within-state gradients (low variance in both SVI and outcomes)

**The sophisticated framing:**
A state with a strong SVI-diabetes correlation isn't necessarily the unhealthiest state. It's a state with **high inequality where SVI is doing its job as a measurement tool**. A state at the bottom of your chart could be uniformly healthy OR uniformly struggling — your analysis can't distinguish those without adding the absolute prevalence dimension. **This is an explicit limitation worth flagging in your writeup, and a clean Phase 2 follow-up.**

---

## Suggested Citation Blocks for Notebook Markdown

When you replace the TODO markdown cells, use citations like this for credibility:

```markdown
### Interpretation

The diabetes-SVI relationship documented here aligns with growing evidence in social epidemiology. Bevan et al. (2024) found social vulnerability significantly worsens diabetes-related cardiovascular mortality through documented mechanisms including medication affordability and treatment access barriers [cite]. The 1.64x prevalence ratio measured in this dataset is consistent with the magnitude of disparity reported across the literature.

The socioeconomic theme's dominance — outpacing the household, minority status, and housing/transportation themes — reflects what the SDOH literature has consistently established: socioeconomic factors alone account for an estimated 47% of variation in health outcomes (HHS ASPE, 2022), and in disease-specific modeling, "income and education generally capture the majority of disease-related signal" even when richer individual-level data are available (Cromer et al., 2026).
```

This kind of writing turns "I correlated some columns" into "I situated my findings within established literature."

---

## Bibliography (formatted for easy copy-paste)

1. Bevan, G. H., et al. (2024). Impact of Social Vulnerability on Diabetes-Related Cardiovascular Mortality in the United States. *Journal of the American Heart Association*, 13(2). https://www.ahajournals.org/doi/10.1161/JAHA.123.029649

2. Cromer, S., et al. (2026). Practical Considerations for using Social Determinants of Health for Disease Prediction in All of Us. *medRxiv preprint*. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12869669/

3. HHS ASPE (2022). Addressing Social Determinants of Health: Examples of Successful Evidence-Based Strategies. https://aspe.hhs.gov/sites/default/files/documents/e2b650cd64cf84aae8ff0fae7474af82/SDOH-Evidence-Review.pdf

4. Ji, X., et al. (2025). Social Vulnerability and National Diabetes Prevention Program Recognition Status. https://pmc.ncbi.nlm.nih.gov/articles/PMC11936411/

5. Myers, C. A., et al. (2017). Diabetes Prevalence is Associated with Different Community Factors in the Diabetes Belt versus the Rest of the United States. *Obesity*. https://pmc.ncbi.nlm.nih.gov/articles/PMC5269515/

6. Cunningham, S. A., et al. (2018). County-level Contextual Factors Associated with Diabetes Incidence in the United States. *Annals of Epidemiology*. https://pmc.ncbi.nlm.nih.gov/articles/PMC5807217/

7. Lord, J., & Roberson, S. (2022). A Geo-Stratified Analysis of Associations Between Socio-Economic Factors and Diabetes Risk. https://pmc.ncbi.nlm.nih.gov/articles/PMC9126863/

8. Drewnowski, A., et al. (2014). The Geography of Diabetes by Census Tract in a Large Sample of Insured Adults in King County, Washington. *Preventing Chronic Disease*. https://pmc.ncbi.nlm.nih.gov/articles/PMC4112927/

9. Owusu Sekyere, F., et al. (2020). Investigation of geographic disparities of pre-diabetes and diabetes in Florida. https://pmc.ncbi.nlm.nih.gov/articles/PMC7425001/

---

## A note on workflow

Use this document as a starting point — verify each source by clicking through, reading the relevant sections, and confirming the claims match what the paper actually says. **I (Claude) generated this synthesis from search results; the academic credibility of your final write-up depends on you verifying the specifics.**

For Phase 2 and beyond, consider using a reference manager like Zotero (free) to organize papers as you accumulate them. The browser plugin grabs citations with one click, and you can export to BibTeX if you ever decide to convert this to a more formal write-up.
