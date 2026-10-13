# Cybersecurity case study: reusable subagent research context

**Captured:** 13 October 2026  
**Purpose:** Preserve the cybersecurity topic and dataset research from the subagents so a later chat in this SML report folder can continue without reconstructing the discussion.

## Quick context

- This is for the Supervised Machine Learning Experiment 12 case study, which is a **classification** assignment and should demonstrate advanced classification/ensemble learning. The prior course-material review recorded a requirement for at least five recent papers, a methodology, implementation, dataset/source, results and interpretation. Check the actual course manual/rubric before final submission if any requirement has changed.
- The user selected **cybersecurity as the broad domain**. The exact problem and dataset should be treated as **not conclusively settled by the subagent research captured here**.
- Two research directions emerged:
  1. **Phishing website classification with UCI PhiUSIIL**: strongest student-level balance of a recognizable real-world problem, a sizable tabular dataset and manageable pandas/scikit-learn work; requires careful domain-level splitting and a literature-fit check.
  2. **Network intrusion detection with UNSW-NB15**: strongest for a ready-to-use, substantial labeled flow dataset and a pre-defined train/test partition; the domain has extensive research, but the benchmark is controlled rather than live organizational traffic.
- These are not contradictory dataset recommendations: one agent compared *cybersecurity project topics* and favored phishing; another audited *network IDS datasets* and favored UNSW-NB15 for buildability.
- Do not claim either model is a deployable security product. Both are benchmark case studies, with limits on generalization to changing real-world threats.

## Research from Agent: project fit and topic comparison

### Phishing website classification — strongest student-level fit

**Possible question:** Can classical and ensemble classifiers distinguish phishing websites from legitimate websites, and how does performance change when test domains were not seen in training?

- **Classification unit and target:** one website record; binary classes are phishing and legitimate.
- **Dataset:** UCI PhiUSIIL Phishing URL dataset. The agent reported 235,795 records, 54 features, 100,945 phishing and 134,850 legitimate examples, no missing values listed by UCI, and a 54.2 MB CSV under CC BY 4.0. The feature table includes URL and webpage-source measurements, so describe it as URL-plus-webpage-feature classification, not URL-string-only classification. Verify the current dataset card and downloaded file before implementation.
- **Feasible student workflow:** pandas inspection and cleaning; a baseline such as Logistic Regression or Decision Tree; Random Forest and one boosting classifier using scikit-learn; confusion matrix, phishing-class precision/recall/F1, macro-F1 or balanced accuracy, and optionally PR-AUC. A bounded comparison could test a carefully selected URL-only feature subset against the full feature set.
- **Leakage and evaluation risks:** do not feed raw `URL` or `Domain` identifiers as ordinary predictors; the model may memorize examples or domains. Keep domain groups separate between train and test where feasible, and inspect feature definitions for variables that could be near-direct proxies for the label. The UCI page does not establish timestamps for every record, so do not promise a chronological test unless the full data documentation supports it.
- **Literature:** the agent found a viable recent literature base on phishing website/URL detection, including:
  - 2023 *Journal of Information Security and Applications* study: [DOI 10.1016/j.jisa.2023.103553](https://doi.org/10.1016/j.jisa.2023.103553)
  - PhishingRTDS, *Computers & Security* (2024): [DOI 10.1016/j.cose.2024.103843](https://doi.org/10.1016/j.cose.2024.103843)
  - Global/local website features, *Computers & Security*: [DOI 10.1016/j.cose.2023.103641](https://doi.org/10.1016/j.cose.2023.103641)
  - Feature-selection study, *Expert Systems* (2025): [DOI 10.1111/exsy.13824](https://doi.org/10.1111/exsy.13824)
  - Phishing-detection systematic review, *Journal of King Saud University—Computer and Information Sciences* (2023): [DOI 10.1016/j.jksuci.2023.01.004](https://doi.org/10.1016/j.jksuci.2023.01.004)
- **Literature caveat:** these papers support the broader phishing-classification problem; the agent did not establish that all five use PhiUSIIL or the exact same features and split. Describe them honestly as related studies and check whether the instructor accepts closely related studies rather than requiring five papers on the identical dataset.
- **Overall agent assessment:** manageable with second-year pandas/scikit-learn skills, a clear binary target, and a real security use case. Main risks are overclaiming, domain overlap/leakage, and overly optimistic evaluation.

### Network intrusion detection — strong literature, higher evaluation burden

**Possible question:** Can a classifier label an individual network flow as benign or attack traffic?

- CIC-IDS2017 offers labeled flow CSVs and more than 80 extracted features. It covers five capture days and multiple attack scenarios. The dataset was made in a testbed; the agent noted that benign-only traffic was recorded Monday and attack activity on later days. A random split or fields such as timestamps, IPs and identifiers may let a model learn the collection schedule rather than general attack behavior.
- A peer-reviewed audit by Engelen et al. found issues in traffic generation, flow construction, feature extraction and labeling; its corrected workflow reconstructed or relabeled more than 20% of traces: [IEEE Security and Privacy Workshops paper](https://doi.org/10.1109/SPW53761.2021.00009).
- A day- or session-aware evaluation is more defensible than randomly splitting related flows, but requires careful investigation and may produce harder results. CIC-IDS2017 is a viable option only if the report addresses these construction and split issues explicitly.
- The agent cited a 2025 *Computers & Security* systematic comparison of public intrusion datasets: [DOI 10.1016/j.cose.2025.104510](https://doi.org/10.1016/j.cose.2025.104510), plus examples from [IEEE Transactions on Network and Service Management](https://doi.org/10.1109/TNSM.2023.3259474) and [Journal of Big Data (2024)](https://link.springer.com/article/10.1186/s40537-024-00886-w).

### Malware-file classification — possible, but less suitable

**Possible question:** Using static features from a Windows executable, classify it as benign or malicious.

- Elastic EMBER provides extracted PE-file features rather than the executable files themselves. The agent described roughly 1.1 million files in the 2017 version and 1 million in 2018: [EMBER repository](https://github.com/elastic/ember), [dataset paper](https://arxiv.org/abs/1804.04637).
- The thousands of input features can increase memory/training complexity; the data date from 2017–2018; and the foundational dataset paper is not a recent journal article. The agent judged this less straightforward than phishing or binary IDS for this coursework.

## Research from Agent: dataset audit for network IDS

### UNSW-NB15 — most manageable network IDS starting point

- Official UNSW page provides four CSV files totaling approximately 2.54 million records and a prepared train/test pair of **175,341 training** and **82,332 test** records (257,673 total). It describes 49 features and nine attack families. See the [official UNSW-NB15 page](https://research.unsw.edu.au/projects/unsw-nb15-dataset).
- The dataset is flow-level: each row summarizes network communication with features such as duration, packet/byte counts, rates and protocol information. A binary target is normal vs attack, using `label`. For that task, remove `id` and `attack_cat` from inputs. For multiclass attack-family classification, use `attack_cat` as the target and remove `label` and `id` from inputs.
- Three categorical features need encoding. The attack-family classes are uneven; the rarest class reportedly has only 130 training and 44 test rows. Thus binary normal/attack classification is safer for a first case study than a 10-class task.
- UNSW permits free academic research use with citation; commercial use requires agreement with the authors. Read the [official terms](https://research.unsw.edu.au/projects/unsw-nb15-dataset) directly before redistribution or other use.
- Dataset limitation: UNSW describes normal activity as modern real traffic and attack activity as synthetic. It is a controlled cyber-range benchmark, not live traffic from organizations. Limit claims to classification performance on this benchmark.
- Suggested split: use the dataset's published train/test files as the final holdout; make a validation split from the training file for model selection. Do not tune against the held-out test set. Fit encoders, scalers, feature selection and any balancing methods using training data only.
- Difficulty estimate: **moderate and manageable** for a second-year student with pandas and scikit-learn. Work includes basic data checks, encoding categorical columns, comparing a baseline/simple model with an ensemble such as Random Forest, and interpreting class-wise metrics.

### Alternative IDS datasets and why they may be harder

| Dataset | What the agents found | Main caution |
|---|---|---|
| **CIC-IDS2017** | Official CSV flows and raw PCAPs; five days; more than 80 features; multi-attack testbed. [Official dataset page](https://www.unb.ca/cic/datasets/ids-2017.html) | Known data-generation, flow, feature and labeling concerns; day and address fields can leak the capture setup. Raw PCAP feature extraction adds work. |
| **CSE-CIC-IDS2018** | Official dataset describes 50 attacker and 420 victim machines, more than 80 features and seven attack scenarios; data are available from public AWS S3. [Official dataset page](https://www.unb.ca/cic/datasets/ids-2018.html) | Large download and processing burden. The agent cited a survey reporting about 16.2 million flows over 10 days and concerns about imbalance, overfitting and incomplete cleaning reports: [Journal of Big Data survey](https://doi.org/10.1186/s40537-020-00382-x). |
| **TON_IoT** | UNSW provides processed CSVs and train/test files for network, Windows, Linux and IoT/IIoT telemetry. [Official dataset page and terms](https://research.unsw.edu.au/projects/toniot-datasets) | More specialized and mixed data modalities than needed for a straightforward tabular case study; purpose-built testbed and ground truth uses IP/time links. |

## Synthesis and decision points

The agents made recommendations at different levels:

- **Phishing + PhiUSIIL** is the project-fit recommendation if the priority is a recognizable real-world application, sizable tabular data, and student-manageable scikit-learn work. Its key extra burden is domain-held-out evaluation and ensuring the five-paper review is close enough to the exact problem.
- **Binary IDS + UNSW-NB15** is the dataset-buildability recommendation if the priority is a prepared partition, a clear normal/attack label and large ready-made flow data. Its key burden is clearly explaining the controlled benchmark and resisting claims about live-network deployment.
- CIC-IDS2017 has extensive use in literature, but the dataset audit suggests materially more cleaning/splitting caveats than UNSW-NB15. CSE-CIC-IDS2018 is likely too heavy for the intended low-friction course build. Malware-file classification is feasible but more technically and literature-wise awkward.
- A comparison should use a simple baseline and at least one ensemble; do not select a complex method merely to sound advanced. Report confusion matrix and class-sensitive measures (precision, recall, macro-F1 or balanced accuracy), not accuracy alone. Explain false positives and false negatives in security terms.
- For any direction, state the prediction unit and label, identify which inputs are available at prediction time, remove IDs/target-derived fields, split at the right grouping/time level, and limit conclusions to the dataset and evaluation used.

### Open decisions before implementation

1. Confirm the exact case-study problem: phishing website classification or network-flow intrusion classification.
2. Confirm whether the instructor requires five recent papers tightly matching the problem, or accepts high-quality related studies. For phishing, the agent found five relevant papers on the broader task, not five confirmed PhiUSIIL studies. IDS has a broad literature base, but individual papers must still be checked for journal quality, recency and relevance.
3. If choosing phishing, inspect PhiUSIIL feature definitions and test a domain-grouped split. If choosing IDS, compare the official UNSW split with the assignment's expectations and state what the dataset's benchmark does and does not represent.
4. Verify current dataset versions, terms, paper bibliographic details, and the lab manual before writing the final case study.

## Reuse note for a future chat

Read this file first as carried-forward research, not as a final approved topic. The user selected cybersecurity as a domain. Preserve the distinction between the phishing project-fit recommendation and the UNSW-NB15 dataset-audit recommendation. Do not silently treat either exact project as instructor-approved. Before producing a final literature review, verify each paper's title, journal, year, peer-review status, methods, limitations and relevance from publisher or DOI pages.
