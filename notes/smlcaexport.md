# Chat Export — SML Case Study (Exp 12 & 13) Planning
*Exported: October 10, 2026*

---

### User
For my SML CA evaluation, experiment 12 and 13 have to be case study reports. i have uploaded all the files i have, analyze them all and tell me what all i can do for this report. i have no idea. if u need i can upload source material as well later

### Assistant
Went through the lab manual, experiment list, both assignment templates, and the CO-PO/evaluation documents.

**What Experiment 12 and 13 actually are:** capstone case-study reports (Exp 12 = classification, Exp 13 = regression), not regular lab exercises. Template structure for both:

Title → Aim → Problem Statement → Literature Review (≥5 recent papers, tabulated) → Objectives (max 3) → Methodology (algorithm steps + equations + evaluation metrics explained) → Implementation → Tools/Libraries → Data/Input (with dataset link) → Results (visualizations + metric-based insights) → Conclusion → Future Scope

**CO-PO mapping drives technique choice:**

| Report | CO | What it requires |
|---|---|---|
| Exp 12 (Classification) | CO4 | Advanced classification and ensemble learning techniques |
| Exp 13 (Regression) | CO3 | Regression techniques and performance evaluation methods |

- Exp 12 should use advanced/ensemble methods (Random Forest, Bagging, Boosting/AdaBoost/XGBoost) — not basic classifiers like Naive Bayes/SVM (that's CO2's territory, already covered in earlier labs).
- Exp 13 should draw from CO3 session-plan topics: OLS, Simple/Multiple/Polynomial Regression, Gradient Descent, Ridge/Lasso, evaluated with R² and MSE.
- A strong report compares 2–3 models rather than running just one algorithm.

**Section guidance:**
- Problem Statement: one narrowly-framed real-world prediction problem.
- Literature Work: 5 recent papers (last 3–5 years), tabulated as `[Author/Year | Technique Used | Dataset | Key Finding/Metric]`.
- Methodology: write out actual algorithm steps (not just the name) + define metrics used.
- Results: correlation heatmap, distribution plot, confusion matrix (Exp 12) or residual plot (Exp 13), metrics comparison table.

**Domain suggestions (from lab manual):** Healthcare, Finance, Weather Forecasting, Agriculture — plus datasets: Heart Disease UCI, Telco Churn, Pima Diabetes, Rain in Australia, Crop Recommendation (classification); Boston/California Housing, Medical Insurance Cost, Student Performance, Crop Yield, Energy Consumption (regression).

**Timeline note (from Evaluation Plan):** Case Study component (CO3+CO4, 5 marks, 16.60% theory weight) tentative date was 23/10/2026; also feeds into continuous Lab Performance & Submission marks (CO3 = 27.28%, CO4 = 18.18%).

*(Offered a task-list next step.)*

---

### User
we have to give it on wednesday next week

### Assistant
Computed as **Wednesday, 21 Oct 2026** — 11 days out. Provided a day-by-day plan:

- **Day 1–2 (Sat–Sun, Oct 10–11):** Lock domain + dataset for both; pick model shortlists (Exp 12: Random Forest + one Boosting method; Exp 13: Linear/Ridge/Lasso + one ensemble regressor); start pulling 5 papers per report.
- **Day 3–5 (Mon–Wed, Oct 12–14):** Implementation — preprocessing, EDA, train models, metrics, comparison tables for both reports.
- **Day 6–8 (Thu–Sat, Oct 15–17):** Writing — Problem Statement, Literature table, Methodology, Results for both.
- **Day 9–11 (Sun–Tue, Oct 18–20):** Polish, Conclusion, Future Scope, proofread, buffer.

---

### User
oct 14

### Assistant
Corrected: **4 days**, not 11 (Oct 14 is this coming Wednesday). Compressed plan:

- **Today (Sat, Oct 10):** Lock both datasets now (clean, ready-to-use CSVs); skim-shortlist 5 papers per report fast (not deep reads); model shortlists kept to 2 models per report — Exp 12: Random Forest + one boosting method; Exp 13: Linear/Ridge + one ensemble regressor.
- **Sun (Oct 11):** Code both end-to-end — preprocessing, EDA (2–3 plots max), train models, metrics, comparison tables. No writing yet.
- **Mon (Oct 12):** Write both reports — Problem Statement, Literature table, Methodology, Implementation for both.
- **Tue (Oct 13):** Results, Conclusion, Future Scope, full proofread. Treat Tue night as the real deadline.
- **Wed (Oct 14):** Submit, buffer only.

---

### User
okay lets start with 12. what topics can i actually do it on? i need to stand out somehow. not too hard and difficult but needs to be a bit different. can i do it on topics im interested in like sports, gaming, etc etc or does it have to be proper real world things. research well take your time and explain to me wekk

### Assistant
**Yes, sports/gaming is completely fine** — the lab manual's domain list (Healthcare, Finance, Weather, Agriculture) ends with "etc.," meaning it's illustrative, not restrictive. What actually matters: a real dataset, a problem that genuinely needs ensemble methods (CO4), and satisfiable literature — sports/gaming analytics is an active, published research area, so all three check out.

**Why it helps you stand out:** most of the batch will default to Healthcare/Finance Kaggle datasets; a domain you're interested in makes the Problem Statement and Future Scope read as genuinely thought through, and the literature review won't be the same five papers everyone else cites.

**Three researched options:**

1. **Esports match outcome prediction (League of Legends)** — Kaggle "LoL Diamond Ranked Games (10 min)" dataset, ~10k matches, clean. Models: Random Forest + XGBoost vs. Logistic Regression baseline. Strong literature (multiple 2023–2024 papers, ~73% accuracy benchmarks). Caveat: most popular student ML dataset on Kaggle — likely common in the batch too.

2. **Mobile game player churn prediction** (recommended pick) — Kaggle churn/game-analytics datasets (session length, level reached, purchases, rolling losses). Models: Random Forest/Gradient Boosting ensemble vs. single baseline — natural fit since churn data is typically imbalanced, giving a genuine "why ensemble beats one model" story. Literature: real industry-research papers on ensemble learning for player engagement/churn and survival ensembles — less saturated among students, directly mirrors real gaming-industry data science work.

3. **Football match outcome prediction (EPL/top-5 leagues)** — multiple clean Kaggle datasets. Models: Random Forest + XGBoost ensemble. Abundant 2023–2024 literature; one paper claimed 99.5% accuracy with a voting ensemble, worth noting skeptically (possible data leakage) as a critical-thinking point in the report.

**Recommendation:** Mobile game churn prediction — less saturated, strong legitimate literature, naturally justifies ensemble methods via class imbalance, clean real-world business angle.

Offered to help find the specific Kaggle dataset link and build the 5-paper literature table next.

---

### User
export chats

### Assistant
Explained chat export isn't something Claude can trigger directly — it's a Settings-based feature in the app, location varies between web and mobile.

---

### User
export chat to .md

### Assistant
Generated a markdown export of the conversation up to that point.

---

### User
i think mobile games churn prediction would be too niche. lets move with sports. research well and tell me what i can do in this domain, are there enough papaers, datasets, etc etc etc for me to work on and get full in my report

### Assistant
Deep research pass into sports as a domain, covering academic legitimacy, datasets, literature, limitations, and ranked sub-domain options.

**Academic legitimacy:** Found five separate systematic reviews published 2024–2026 specifically on ML in sports — a Frontiers 2026 review analyzing 118 journal articles (2020–2025) across match outcome prediction, in-game event prediction, injury prediction, and player performance prediction; a PRISMA-registered review of 36 ML-in-sports-performance studies; a PROSPERO-registered systematic review of ML in sport injury prediction/prevention; a PRISMA soccer-specific systematic review; and a 2024 sports betting ML review spanning soccer, basketball, tennis, and cricket. These can anchor the literature table with high-authority sources.

**The good:**
- Data volume is enormous and clean across football (4,070+ matches, 113 features per match in one Kaggle set), NBA (2004-05 to 2024-25 seasons across multiple Kaggle sources), and cricket/IPL (179,078 ball-by-ball observations, 21 columns).
- Recent (2023–2026) papers exist for every major sub-domain, easily satisfying the "5 recent papers" requirement.
- Ensemble methods consistently win in this literature (NBA: Random Forest at 85.71% accuracy in one 2023 study; IPL: ensemble strategies outperforming simpler tactics) — directly supports the CO4 angle.

**The bad (useful for the report's Limitations/Future Scope):**
- Data leakage is the most documented failure mode — a dedicated paper describes it as independent variables containing information about the dependent variable, causing unreliable results; must exclude post-match stats as features.
- Sports prediction has a humbling ceiling — a peer-reviewed critique concluded it's "exceedingly difficult, arguably futile" to beat bookmakers profitably with ML; the largest-ever injury prediction study (880 elite athletes) only reached ~65% accuracy, with researchers warning easy-to-use ML tools make it simple to produce promising-looking models by chance.
- Watch for synthetic datasets masquerading as real ones — flagged a Kaggle "Injury Prediction Dataset" that explicitly describes itself as synthetic (NumPy/Pandas simulated) — avoid for a "real-world case study."
- Overfitting/selection bias are structurally common in sports ML due to small samples and temporal dependence.

**Ranked sub-domain options:**

| Domain | Data depth | Literature depth | Differentiation | Verdict |
|---|---|---|---|---|
| IPL Cricket | Excellent (match + ball-by-ball) | Strong, 2018–2025 | High | Top pick |
| NBA | Excellent (20+ seasons) | Very strong | High | Strong alt |
| Football (EPL) | Excellent | Very strong | Low (most-picked) | Safe but generic |
| Injury prediction (real dataset: competitive runners, 2020 peer-reviewed) | Moderate, niche | Strong, research-grade | Very high | Best for standing out, higher setup effort |
| Esports (LoL) | Excellent | Strong | Low (most-picked overall) | Backup only |

**Recommendation held from before the deep dive:** IPL Cricket — best balance of rich real data, recent strong literature, built-in "ensembles win" narrative for CO4, and relatively uncommon as a classification case study pick. NBA is the close second if zero classmate overlap is the priority.

Offered to lock in IPL and start the 5-paper literature table, or weigh NBA further first.

---

### User
export chat as .md

### Assistant
*(This file.)*
