# Experiment 12 Literature Review Matrix

**Working topic:** Binary benign-versus-attack network-flow classification on UNSW-NB15  
**Status:** Evidence-based shortlist for the report; no paper has yet been approved by the instructor.  
**Prepared:** 2026-10-13

The course template asks for at least five recent journal papers. These five are recent and closely connected to UNSW-NB15, but they do not all study the same label setup or features. Use them to support the background and method rationale; do not compare their reported scores directly with our implementation results.

## Recommended five-paper shortlist

| Paper | Dataset and task | Method and useful contribution | Fit and caveat |
|---|---|---|---|
| **Maseno, E. M., Sun, Y., & Wang, Z. (2026). “Reliability auditing of explanations for machine-learning-based intrusion detection systems.” _Journal of Computer Virology and Hacking Techniques_, 22, article 80.** [Publisher full text](https://link.springer.com/article/10.1007/s11416-026-00664-7) | UNSW-NB15 and IoT-ToN; binary normal (0) versus attack (1). Retains UNSW's official train/test partitions. | Compares Logistic Regression, Random Forest, and XGBoost; preprocessing is fit on training data, model selection uses stratified five-fold CV, and the official test partition is kept untouched. The main contribution is reliability auditing of SHAP explanations. | **Closest match to our planned task and model comparison.** The explanation-audit machinery is beyond our required scope. Use its split discipline and model-family rationale, not its scores as targets. Its 2026 publication date is verified on the publisher page.
| **Kiflay, A., Tsokanos, A., Fazlali, M., & Kirner, R. (2024). “Network intrusion detection leveraging multimodal features.” _Array_, 22, 100349.** [Publisher page](https://www.sciencedirect.com/science/article/pii/S2590005624000158) · [Publisher-version PDF](https://uhra.herts.ac.uk/id/eprint/11182/1/1-s2.0-S2590005624000158-main.pdf) | UNSW-NB15 packet captures; studies binary and multiclass detection. | Combines Random Forest models on selected flow features and the first 32 payload bytes using soft voting. | **Direct dataset relevance; adjacent input representation.** It derives flow/payload features from PCAPs, whereas our working plan uses the prepared CSV files only. Avoid presenting it as a like-for-like CSV experiment.
| **Pospíchal, J., Augustín, A., Huraj, L., Střelec, P., & Gabriška, D. (2026). “Random Forest-Based Network Intrusion Detection with Feature Selection and Class Balancing on UNSW-NB15 Traffic.” _Information_, 17(9), 836.** [Publisher full text](https://www.mdpi.com/2078-2489/17/9/836) | UNSW-NB15; five separate attack-versus-normal binary tasks: DoS, Exploit, Backdoor, Analysis, and Reconnaissance. | Random Forest with mutual-information feature selection, threshold tuning, and fixed-target SMOTE variants; reports attack-specific precision/recall trade-offs. | **Useful for class imbalance and attack-specific metrics.** Each task filters out non-target attacks, so it does not estimate benign-versus-all-attacks performance on mixed traffic. The paper compares separately optimized full pipelines; its results do not isolate SMOTE alone.
| **Mohiuddin, G., Lin, Z., Zheng, J., Wu, J., Li, W., Fang, Y., Wang, S., Chen, J., & Zeng, X. (2023). “Intrusion Detection using hybridized Meta-heuristic techniques with Weighted XGBoost Classifier.” _Expert Systems with Applications_, 232, 120596.** [Publisher page](https://www.sciencedirect.com/science/article/pii/S0957417423010989) | UNSW-NB15 and CICIDS2018; binary and multiclass detection. | Weighted XGBoost with a wrapper-based hybrid metaheuristic feature-selection and optimization method; discusses minority-class weighting and boosting. | **Direct dataset and boosting context.** The optimization method is much more complex than our proposed baseline study. Published values are not comparable unless task, split, preprocessing, and features are harmonized.
| **Telikani, A., Rudbardeh, N. E., Soleymanpour, S., Shahbahrami, A., Shen, J., Gaydadjiev, G., & Hassanpour, R. (2024 issue; published online 2023). “A Cost-Sensitive Machine Learning Model With Multitask Learning for Intrusion Detection in IoT.” _IEEE Transactions on Industrial Informatics_, 20(3), 3880–3890.** [IEEE publisher record](https://ieeexplore.ieee.org/document/10268649/) · [Publisher-version PDF](https://pure.rug.nl/ws/files/937973441/A_Cost-Sensitive_Machine_Learning_Model_With_Multitask_Learning_for_Intrusion_Detection_in_IoT.pdf) | UNSW-NB15 and BoT-IoT; cost-sensitive, multitask intrusion detection with attention to rare and unknown attacks. | Hybrid autoencoder and SVM, with cost-sensitive learning for low-frequency classes and multitask handling of unknown attacks. | **Adjacent methodological context** for recall and minority-class errors. It is not the same benign-versus-all-attack binary task or the same model family. Check the full methods before describing its exact UNSW label decomposition in the final report.

## Reserve / replacement candidate

**Al-Bakaa & Al-Musawi (2022), “A new intrusion detection system based on using non-linear statistical analysis and features selection techniques,” _Computers & Security_, 122, article 102906.** [Publisher record](https://www.sciencedirect.com/science/article/pii/S0167404822002991). The paper studies binary normal/attack detection on UNSW-NB15 and is the strongest direct replacement for the earlier shortlist's Elnakib et al. (2023), which uses CICIDS2017 and 15 classes. Its recurrence-quantification-analysis features differ substantially from raw flow-row modelling. Keep it in reserve if the instructor prefers a direct binary UNSW paper over a newer imbalance or cost-sensitive context paper.

## Earlier candidates audited

- **Khan et al. (2023), _Journal of Network and Computer Applications_, 212, 103560:** uses UNSW-NB15 and CICIDS2017 with an AutoML soft-voting ensemble. The accessible abstract did not settle whether the UNSW setup is binary; verify the full method before making that claim. Do not copy percentage-formatted metrics from its abstract without checking the results table.
- **Thakkar & Lohiya (2023), _Information Fusion_, 90, 353–363:** feature selection and DNN across NSL-KDD, UNSW-NB15, and CICIDS2017; likely task setup differs from our binary baseline, and the accessible abstract does not make the label mapping explicit.
- **Catillo et al. (2022), _Software Quality Journal_, 30, 955–981:** studies transfer from CICIDS2017 to a second dataset. Keep as an optional source for benchmark transfer limitations; it does not use UNSW-NB15.
- **Elnakib et al. (2023), _Journal of Supercomputing_, 79, 13241–13261:** uses CICIDS2017 for 15 traffic classes (normal plus 14 attacks); weakest fit to the selected dataset and task, so replaced in the working list.
- **Al-Essa et al. (2024), _Machine Learning_, 113, 5379–5422:** includes UNSW-NB15 but focuses on multiclass neural ensembles and explainability; useful only if the report needs that broader context.

## Citation and comparison guardrails

1. The five-paper shortlist is **recommended, not instructor-approved**. Confirm whether “recent” means a specific year window and whether journal quartiles or indexing evidence are required.
2. No journal quartiles or ranking claims are made here; they have not been checked through an official metrics source.
3. Reported accuracy, F1, recall, or AUC values are study-specific context, never targets for our implementation. Label mapping, train/test partition, preprocessing, features, and task grain must match before metrics are compared.
4. Cite the dataset creators separately from these five literature-review papers, following the official UNSW dataset page's academic-use citation request.
5. Keep the study's synthetic-attack and benchmark limitations visible in the final report; benchmark results do not establish production IDS performance.

## Primary source checked for dataset facts

- [UNSW Research: The UNSW-NB15 Dataset](https://research.unsw.edu.au/projects/unsw-nb15-dataset) — official prepared split names/counts, dataset construction description, and academic-use/citation notes.

## Boundary between the papers and this implementation

The papers include SHAP explanation audits, payload/PCAP extraction, metaheuristic feature selection, autoencoders, and multitask learning. Our implementation uses the prepared CSVs, standard encoding/scaling, Logistic Regression, Random Forest, and Histogram Gradient Boosting with fixed configurations. Those advanced paper methods are related work and are not reproduced here. Explain only the relevant idea and its limitation when discussing each paper; their scores are not directly comparable with our benchmark.

Bibliographic correction after primary-source review: Telikani et al.'s published page range is 3880–3890, as shown in the publisher-version PDF linked above. Journal rankings and the instructor's precise definition of recent/good-quality papers remain unconfirmed.