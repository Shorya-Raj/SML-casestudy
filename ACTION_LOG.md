# SML Action and Audit Log

**Project:** Supervised Machine Learning case study (Experiment 12 / possible CA3 scope)
**Log started:** 2026-10-13 23:16 IST
**Owner:** Student project work with Codex assistance

## Purpose

A chronological record of decisions, source checks, research, data handling, implementation, validation, and open questions. Entries distinguish course requirements from proposed choices and observed results. This log is intended to let the student review what happened, when it happened, why it happened, and what evidence supports it.

## Current working scope

- **Chosen direction:** cybersecurity, binary network-flow classification on the official prepared UNSW-NB15 split files.
- **Working question:** How well can supervised classifiers distinguish benign from attack flows in UNSW-NB15, and how do two ensemble families compare with a simple learned model and a prior-only baseline?
- **Target/grain:** verified binary `label`; one row is treated as one prepared network flow.
- **Models already run:** Dummy prior baseline, balanced Logistic Regression, Random Forest (bagging), and HistGradientBoosting (boosting). Fixed settings and fit times are in the JSON result.
- **Data processing:** inputs are checksum-verified and read without automatic missing-value conversion; `id` and target-derived `attack_cat` are excluded; numeric/categorical pipeline steps and their rationale are documented in code, JSON, Markdown, and this log.
- **Evaluation already run:** one fixed-seed grouped validation fold, the official test split, and a secondary test subset with predictor vectors unseen in training. The validation groups have zero overlap. See the result report for metrics and caveats.
- **Claim boundary:** conclusions apply to the prepared benchmark split; they do not establish production IDS performance.
- **Scope status:** the reviewed model comparison, student walkthrough, run guide, and editable Experiment 12 report draft are complete. Confirm final cover metadata, literature requirements, screenshots, and submission format. The supplied planning request names both Experiments 12 and 13; regression / Experiment 13 remains pending.

## Open questions

1. The supplied planning chat explicitly requests case-study reports for Experiments 12 and 13. The current work covers Experiment 12; plan the remaining regression study and confirm how the two reports relate to theory CA3's CO3/CO4 marking and lab submission format.
2. Which submission's metadata should appear on the cover? The lab manual identifies `0701260405` and the theory session plan identifies `0701260304`; these appear to be separate course codes rather than a contradiction. The CO-PO sheet's `2024-28` cohort differs from the signed plan/evaluation's `2025-29`, so confirm the cohort and requested cover fields.
3. Is the Evaluation Combined sheet's 23 October 2026 date still the current submission date? It is marked tentative.
4. Does the instructor require a specific year cutoff, journal quartile/indexing proof, or a particular citation style for the five-paper requirement?

## Evidence status

- **Verified in local course files:** Experiment 12 is a classification case-study template; it requires at least five recent journal papers, at most three objectives, methodology/algorithm/metrics, implementation, data source, results/visualizations, conclusion, and future scope. The manual requires code snippets, output screenshots, and explanation of testing/results.
- **Verified in local course files:** CO4 includes advanced classification and ensemble learning. The signed session plan lists cybersecurity among supervised-ML applications and maps CA3 to CO3 and CO4.
- **Verified in local course files:** the evaluation sheet assigns five marks to the Case Study Assignment (CO3: 3; CO4: 2) and gives 23 October 2026 as a tentative date.
- **Verified from official UNSW research page:** the prepared split files are `UNSW_NB15_training-set.csv` (175,341 rows) and `UNSW_NB15_testing-set.csv` (82,332 rows); academic research use is granted. The source describes normal activity plus synthetic attack activity generated in a cyber-range setting.
- **Verified locally:** prepared split file sizes, SHA-256 values, schema, labels, missing-value tokens, duplicate/predictor-vector patterns, and the leakage controls are documented in `reports/unsw_nb15_audit.json` and `reports/unsw_nb15_data_audit.md`.
- **Verified locally:** the four-model workflow ran, reported metrics were recalculated against saved confusion matrices, and the two report figures were regenerated and inspected. See `reports/unsw_nb15_model_results.md` and `.json`.
- **Still pending:** confirmation of how the two requested lab reports map to theory CA3, cover-page metadata/cohort, current due date, exact “recent papers” cutoff/citation style, and any journal-ranking requirement.
- **Still pending:** final student review of the Experiment 12 draft, literature acceptance, required code/output screenshots, and the Experiment 13 regression study/report.

## Chronological work entries

### 2026-10-13 23:16 IST — Start authorized work

- User authorized starting the project work, using relevant skills/plugins/subagents, and maintaining an audit log for later review and learning.
- Initialized this file before data acquisition or model training.
- Three research subagents were assigned: audit the current candidate papers; find/verify stronger directly relevant papers; verify official dataset facts and safe audit steps. Their findings are pending and will be reconciled here.

### 2026-10-13 23:17 IST — Rechecked project and course context

- Reviewed the earlier project chat and current local assignment/course documents.
- No UNSW-NB15 dataset files, research-paper collection, or implementation notebook are currently present in the project folder; the folder currently contains course materials and the chat export.
- The earlier chat records the selected direction as binary network-flow intrusion classification on UNSW-NB15.
- Course-scope ambiguity and cover-page metadata discrepancies remain open; they do not prevent preparing the Experiment 12 working materials, but final submission metadata must be confirmed.

### 2026-10-13 23:18 IST — Initial official-source and literature search

- Opened the official UNSW-NB15 research page. It lists the prepared train/test filenames and row counts above, grants academic research use, describes nine attack types, and says the dataset contains hybrid real normal activity and synthetic attack behaviours created in a cyber-range environment.
- The first literature search surfaced additional 2024–2025 journal candidates focused on UNSW-NB15 binary/ensemble classification. They are leads only until venue, full text, task, and fit are checked.
- No dataset files have been downloaded and no model has been trained yet.

### 2026-10-13 23:27 IST — Official SharePoint access and literature shortlist

- User opened the official UNSW SharePoint link in the Codex side browser. The authenticated read-only folder view is reachable.
- Navigated to `CSV Files/Training and Testing Sets`. The official folder lists `UNSW_NB15_training-set.csv` (30.8 MB) and `UNSW_NB15_testing-set.csv` (14.7 MB), matching the filenames and relative sizes expected from UNSW's published split counts. The exact local file contents have not yet been acquired or audited.
- An in-progress `.crdownload` archive is present in Downloads, created around 23:21 before Codex selected the two prepared rows. Its origin and contents are not confirmed from the filename alone. The user confirmed the intended download is the **full dataset**, so leave it running and inspect only after it completes.
- A public Zenodo deposit was checked as a possible fallback. The downloaded `UNSW_NB15_training-set.csv` matches Zenodo's listed MD5 (`b5a3168217dee84d94574e697130c8aa`) but contains 82,332 lines with no header, while UNSW's official page states the training set has 175,341 records. This indicates that Zenodo's prepared file names/content are unsuitable for this project without further verification. It is excluded from the working dataset. No model training was performed.
- The temporary Zenodo candidate and its zero-byte companion were removed from `data/raw/` after this mismatch was recorded; `data/raw/` is ready for the official files.
- Opened the official SharePoint folder in Chrome as a fallback. Microsoft showed a pre-saved work/school account; Codex did not select it because its ownership was not verified. The user confirmed the full dataset download is already progressing from the side-browser session, so no additional Chrome sign-in is currently needed; the unused Chrome tab was closed.
- Paper audits converged on a stronger 2023–2026 shortlist than the initial candidates. `LITERATURE_REVIEW_MATRIX.md` records five recommendations, how closely each matches the binary UNSW task, limitations, reserve candidates, and citation guardrails. Quartiles/rankings are not asserted; instructor approval remains pending.
- Confirmed primary-source facts: the 2026 Maseno et al. paper uses binary normal/attack labels on UNSW-NB15 and compares LR/RF/XGBoost with train-only selection and an untouched test partition; the 2023 Mohiuddin et al. paper uses weighted XGBoost and UNSW-NB15; the 2024 Kiflay et al. paper uses UNSW-NB15 PCAP-derived flow and payload features; the 2026 Pospíchal et al. paper evaluates separate attack-versus-normal filtered subsets; the 2024 IEEE Telikani et al. article studies cost-sensitive multitask IDS on UNSW-NB15 and BoT-IoT.
- Next data step: inspect the confirmed full SharePoint archive after it finishes, extract the official prepared training and testing CSVs, record SHA-256, then validate row counts, schema, labels, and duplicates before preprocessing.

### 2026-10-13 23:35 IST — Full dataset download confirmed

- User clarified that the in-progress full dataset download is intentional. Do not cancel or replace it with a prepared-pair-only download.
- The file `C:\Users\shory\Downloads\Unconfirmed 165002.crdownload` was still growing; at 23:34 IST it was 7,784,065,696 bytes and had a recent write time. It is still a temporary Chromium download, not a completed archive. No contents have been extracted or trusted.
- Codex opened the official folder in Chrome as a fallback. Microsoft showed a pre-saved account whose ownership was not verified; it was not selected and no credentials were entered. That unused sign-in tab was closed because the user-confirmed SharePoint download is already progressing from the side-browser session.
- Next: wait for the confirmed download to complete; identify its final archive name and type, inspect its listing, extract only required official CSV files into `data/raw/`, and validate them against the official split counts and schema before any model work.

## Next steps

1. Plan the Experiment 13 regression case study requested in the supplied planning chat. Confirm with the instructor/course portal how the two lab reports map to theory CA3; the classification report does not cover both COs.
2. Confirm the cover-page course code/cohort, the current submission date, the meaning of “recent” for the five journal papers, citation style, and any journal-ranking requirement.
3. Verify the five shortlisted papers against publisher/DOI records and full methods, then write the literature review without comparing unlike tasks or copying their scores as targets.
4. Build the full Experiment 12 submission from the course template: concise objectives, dataset/source, methodology and equations/algorithm, metric explanations, implementation/code snippets, required screenshots, results and security-error interpretation, limitations, conclusion, future scope, and references.
5. Review the report for alignment with the confirmed COs and submission format, then adapt the explanatory wording into the student's own voice for presentation and viva.

## Source links checked so far

- Official dataset source: https://research.unsw.edu.au/projects/unsw-nb15-dataset
- Working five-paper shortlist and candidate audit: see `LITERATURE_REVIEW_MATRIX.md`.
- Zenodo archival mirror examined and rejected for this build because its prepared training-set file contains 82,332 lines rather than the 175,341 records expected by the official UNSW page: https://zenodo.org/records/3768048

### 2026-10-13 23:16 IST — Preserved supplied subagent context

- Copied `CYBERSECURITY_SUBAGENT_CONTEXT.md` from Downloads into the project folder without altering its contents, so its provenance and comparison are available alongside this log.
- The note records two earlier subagent recommendations: phishing/PhiUSIIL for student-level fit, and network IDS/UNSW-NB15 for the prepared split and buildability. It explicitly says the exact topic had not yet been settled at the time that note was captured.
- The later parent chat then produced an UNSW-NB15-specific plan after the user said to move forward, and that plan is the working selection for this task. The earlier comparison remains useful rationale; its dataset/paper claims still require primary-source verification before use.
- No phishing data or papers will be acquired for the current build unless the user reopens that decision.
- Read-only research checks found that UNSW's official SharePoint download path redirects to Microsoft sign-in in the browser. The prepared files and terms are listed publicly, but local acquisition may require the user's authenticated session. No mirror has been substituted.

### 2026-10-13 23:36 IST — User asked which sites need login before stepping away

- Confirmed the official UNSW SharePoint/OneDrive dataset download remains active: `Unconfirmed 165002.crdownload` grew from 8,400,390,816 bytes at 23:35:28 to 9,201,655,806 bytes at 23:36:33. It is still incomplete and has not been inspected.
- No new sign-in is needed now. The user’s authenticated official UNSW SharePoint session is already available in the Codex side browser. Keep that browser session and the device awake while the full download continues; do not sign out or cancel it.
- No other login is currently needed for the prepared analysis or literature sources. If a publisher later blocks full text, request UNSW Library access at that point rather than signing into publisher accounts preemptively.

### 2026-10-13 23:40 IST — Download and course-template checkpoint

- The full archive file remains `Unconfirmed 165002.crdownload` at 10,924,402,839 bytes, with last write 23:38:54 IST. It had grown to 10,924,402,839 bytes by this check, but did not grow again across the latest 90-second observation; this may be a temporary pause. It is locked by the browser process, so no bytes were read or altered. C: still reports 132,785,627,136 bytes free.
- The current authenticated SharePoint folder visibly lists the official testing and training CSVs at 14.7 MB and 30.8 MB. A UI click was made on the testing file's Download action as a small acquisition fallback. No matching CSV appeared in the Downloads directory and no completion signal was observed, so the file is **not counted as locally acquired**. The full archive download was not cancelled or changed.
- `Lab Assignment_12.docx` requires a case-study classification report with at least five recent papers from good-quality journals, no more than three objectives, methodology including equations and evaluation metrics, an algorithm, a brief explanation of performance metrics, implementation, tools/libraries, linked dataset description, visualizations, metric-based results with insights, conclusion, and future scope (template headings/paragraphs 1-34).
- `13. SMLL_Lab_Manual (2) (1).docx` frames Experiment 12 as case-study classification; the manual's general report instruction asks for implementation code and output screenshots, detailed explanation of testing/results, and upload using the provided template (paragraphs 62, 65-69, and 941-943). Its preceding Gradient Boosting/XGBoost experiment specifies `GridSearchCV` and tuning `n_estimators`, `learning_rate`, `max_depth`, `subsample`, and `colsample_bytree` (paragraphs 930-936); this is algorithm practice context, not a stated exclusive requirement for Experiment 12.
- `SML_Evaluation_Plan_with ESE ...docx` includes a CA rubric emphasizing correct implementation, conceptual understanding, accurate results, documented code, appropriate analysis, and on-time submission. Its current extracted table does not establish a separate final-project metric threshold.
- Interpretation: keep the selected binary UNSW-NB15 task, but make the final model choice visibly connected to the required case study and methods taught. Exact minimum classifier count, recent-paper year window, journal quality definition, and experiment/report scope still need confirmation from the instructor.

### 2026-10-13 23:41 IST — Independent course-scope audit and correction

- A read-only subagent cross-checked the Experiment 12 assignment, lab manual, CO statements, evaluation plan, and signed session plan. No project or source documents were edited.
- The assignment form (Lab Assignment_12.docx, paragraphs 1-34) supplies the detailed report structure. It does not name a required algorithm, list an exact metric set, set a year cutoff for “recent,” define journal quality/indexing, or specify a literature-table schema/citation style.
- The Experiment 12 section of the lab manual (paragraphs 940-944) contains only the case-study classification heading and “Student Activity.” The wider course list's healthcare/finance/weather/agriculture examples are illustrative rather than exclusive; cybersecurity is not excluded.
- Course outcomes in `6. Course Outcomes (CO) Statements and CO-PO-PSO Mapping.pdf`, page 1, connect CO2 with classification and evaluation methods and CO4 with advanced classification/ensembles. Logistic Regression, Random Forest, and boosting remain defensible proposed choices, not requirements. The signed session plan (page 3, lecture 24) names confusion matrix, precision, recall, F1, ROC, and AUC; the CO mapping (page 2) also names accuracy. Report the attack class clearly and consider macro-F1 for imbalance, but do not imply every metric is mandated by the assignment.
- Scope discrepancy: Evaluation_Combined (1).pdf page 1 lists a tentative 23 October 2026 Theory CA3 case-study assignment mapped to CO3 and CO4. The signed session plan page 5 describes CA3 as a recent-literature real-world case study mapped to CO3 and CO4. CO3 is regression and CO4 advanced classification/ensembles; Experiment 12 is classification and Experiment 13 is regression. Instructor confirmation is needed on whether CA3 requires Exp 12 alone or a combined Exp 12+13 submission. The date is tentative.
- Course-code discrepancy remains: the lab-manual cover says 0701260405 (paragraph 4); the signed session-plan cover says 0701260304 (page 1). Do not put a course code on a final cover until confirmed.
- Correction to the 23:40 entry: the note about source-code upload to Moodle/Google Classroom at manual paragraph 936 sits under Experiment 11's XGBoost instructions; do not treat that upload note as a specific Experiment 12 requirement. The separate general notebook expectations at paragraphs 64-68 require code snippets, output screenshots, and explanation of tests/results.
- Open later for instructor/Moodle: CA3 scope, journal-quality and recency criteria, citation style, course code, and exact deadline.

### 2026-10-13 23:43 IST — Download pause check

- The `.crdownload` remains 10,924,402,839 bytes with last write at 23:38:54 IST; no growth was visible for about 4.5 minutes. The browser still holds the file open, so I have not inspected or changed it. A temporary network/service pause is possible; completion is not verified.
- C: has about 132.8 GB free. The active Windows power plan's sleep-after setting is 1 hour on both AC and battery; I made no power-setting changes. This is longer than the user's stated 30-minute absence.
- The optional direct testing-split download remains unconfirmed and is not counted as acquired. Do not cancel the full download.

### 2026-10-13 23:56 IST — Excel preview audit and dataset scope update

- Applied the spreadsheet and Excel live-control workflows. No local Microsoft Excel desktop app or connected Excel session is exposed in this session, so no desktop workbook was opened or edited. The user explicitly allowed OneDrive as an alternative.
- Read-only Excel web preview of `UNSW_NB15_testing-set.csv` reports one worksheet, end cell `AS82333`, and 3,704,985 populated cells. This is consistent with 82,332 data rows plus one header row across 45 columns. It verifies the preview extent only; the local file and data-quality checks remain unverified.
- Attempted to download the training CSV from the OneDrive file menu and export the testing CSV through Excel web's `File > Export > Download as CSV UTF-8`. No prepared CSV appeared in Downloads or `data/raw/` during follow-up checks. These attempts are not counted as successful acquisition.
- The previously authorized full archive finished downloading at 23:50:46 IST as `C:\Users\shory\Downloads\OneDrive_2026-10-13.zip` (20,634,321,206 bytes). A read-only ZIP integrity check failed because the End of Central Directory record is missing. The archive is therefore incomplete/unusable and was not extracted. It is no longer an active `.crdownload`.
- User updated scope: do not fetch the unnecessary full dataset; use only what this project needs. This supersedes the earlier instruction to keep the full download running. No further full-dataset downloads or extraction will be done. The completed ZIP is outside the writable project folder and has not been removed.
- Official UNSW source states that the prepared splits contain 175,341 training rows and 82,332 testing rows, while the raw traffic capture is about 100 GB. For this project, only the prepared splits are needed. Source: https://research.unsw.edu.au/projects/unsw-nb15-dataset
- The current browser-control session exposes page controls but no desktop download manager; no local Excel desktop app is available. Next: obtain only the two prepared CSVs into `data/raw/`, then hash and profile them before any transformation. Keep source copies unchanged and put derived work in separate files/workbook sheets.

### 2026-10-14 00:01 IST — Scope update, archive status, and sign-in handoff

- The user clarified to download/use only what the project requires. This supersedes the earlier request to continue downloading the full dataset.
- The 20,634,321,206-byte `OneDrive_2026-10-13.zip` was already present at 23:50:46 IST before the scope change arrived. It is stable and not an active download. A read-only integrity check found a ZIP local-file header at the start but no End of Central Directory record at the end; it cannot be opened as a valid ZIP and was not extracted. The file remains in Downloads; no deletion was attempted.
- Tried Excel web `File > Export > Download as CSV UTF-8` and `File > Create a Copy > Download a Copy` on the read-only testing preview, and tried OneDrive's file-menu Download on the training row. None produced a local prepared CSV in `Downloads/` or `data/raw/` at the subsequent checks.
- Opened the prepared-splits folder in the existing Chrome profile. Microsoft displayed a saved work account for a different person (`s2945266@ed.ac.uk`); it was not selected. No credentials or MFA codes were entered. The Chrome tab is left available for the user to choose **Use another account** and sign in with their UNSW account.
- Current blocker: local copies of the official prepared train/test CSVs are not yet available. Once the user completes the correct-account sign-in in Chrome, resume by downloading only `UNSW_NB15_training-set.csv` and `UNSW_NB15_testing-set.csv` and then verify sizes, SHA-256, row/column counts, labels, missingness, duplicates, and overlap.

### 2026-10-14 00:04 IST — Confirmed minimum source route

- The dataset audit checked the official UNSW-NB15 page and its linked prepared-data folder. The official page names the prepared training and testing CSVs but does not expose independent per-file links. The folder redirects to Microsoft sign-in before showing files.
- No account was selected, credentials entered, files downloaded, or UNSW contact made during that check. The Chrome tab remains at the sign-in handoff; use **Use another account** and the user's UNSW account if the user is ready.
- Scope remains limited to the two prepared CSVs. The ~100 GB packet-capture collection is unnecessary for the current project; no additional full-data download or extraction is authorized.
- Current blocker is access to the official prepared-splits folder with the user's account. After the folder loads, download only the two named CSVs and resume local integrity and quality checks.


### 2026-10-14 01:04 IST — Reopened SharePoint sign-in page

- User reported signing in. The existing Codex in-app browser now displays the official “Training and Testing Sets” SharePoint folder with both read-only prepared files: `UNSW_NB15_training-set.csv` (30.8 MB) and `UNSW_NB15_testing-set.csv` (14.7 MB). This confirms folder access in that browser session.
- At the user's request, opened the same official folder in a new Chrome tab, which presents Microsoft's account chooser. The tab shows a saved account that is not the user's UNSW account and a “Use another account” option. No account was selected and no credentials were entered in Chrome.
- The existing in-app browser session remains accessible. The prepared-file acquisition and data verification are still pending; the raw packet captures remain out of scope.



### 2026-10-14 01:05 IST — User confirms no UNSW account

- User clarified they do not have a UNSW account. Do not direct them to create one or use the unrelated saved account in Chrome.
- The authenticated/shared in-app OneDrive session already lists the official read-only prepared training and testing CSVs. Continue using that accessible shared folder; the separate Chrome account chooser is not required for the current in-app access.
- No credentials were entered and no dataset files have yet been verified locally.



### 2026-10-14 01:08 IST — Download attempt from accessible OneDrive folder

- Used the OneDrive row action to request download of `UNSW_NB15_training-set.csv` (30.8 MB). The action menu closed, but no matching CSV or partial download appeared in the user's Downloads folder at the verification check.
- No local dataset file was created or counted as acquired. The testing CSV has not been downloaded in this attempt. The share folder remains visible and read-only; next step is to resolve the download handoff or use an alternate official access route.



### 2026-10-14 01:10 IST — Follow-up search for downloaded files

- Searched Downloads and the SML report project for `UNSW_NB15_*`; searched Temp and OneDrive as well. No prepared CSV copies were found.
- The earlier `OneDrive_2026-10-13.zip` is the only dataset-related local download recorded so far; prior integrity checking found it incomplete/unopenable as a ZIP. It is not a verified prepared train/test pair.
- The SharePoint row-level Download action was attempted for the 30.8 MB training CSV, but no resulting local file or partial appeared. No dataset file has yet been accepted as acquired. If an ordinary UI download from the shared folder still does not save, ask the user to trigger the two individual file downloads in the visible OneDrive folder, then verify and stage those copies.



### 2026-10-14 01:15 IST — Prepared CSVs downloaded and staged locally

- Downloaded only the official prepared files from the already accessible shared OneDrive folder. No UNSW account was needed in that session.
- `UNSW_NB15_training-set.csv`: 32,293,018 bytes; SHA-256 `BEC7DD5EC88DC2A0CCC7A07879D338395ED7421750F675FD0339E07DFE0648FA`.
- `UNSW_NB15_testing-set.csv`: 15,380,800 bytes; SHA-256 `734FE6642EDF758F7C94D7D9149426B49D202FE8E7BF0BEF47392489C3C0A559`.
- Copied the unchanged files into `data/raw/` in the project. Both destination hashes matched the downloaded source files.
- The unusable 20.6 GB ZIP remains untouched in Downloads. The raw packet-capture dataset was not downloaded or extracted.
- Next: continue the model training work in the separate project chat requested by the user.


### 2026-10-14 01:18 IST — Resumed work after prepared-file staging

- Reviewed `ACTION_LOG.md`, `CYBERSECURITY_SUBAGENT_CONTEXT.md`, the exported project chat, and `LITERATURE_REVIEW_MATRIX.md`. The active direction remains Experiment 12 binary benign/attack classification on UNSW-NB15; candidate models are Logistic Regression, Random Forest, and one boosting classifier. The raw packet captures and the incomplete 20.6 GB ZIP remain out of scope.
- No `AGENTS.md` or separate project plan/data-acquisition note was present in the project tree. The active scope, acquisition provenance, open course questions, and next steps are recorded in this log.
- Re-read the Experiment 12 assignment template, CO statements, signed session plan, evaluation sheet, and relevant lab-manual sections. The assignment requires at least five recent papers, up to three objectives, methodology/equations/metrics, algorithm, implementation/tools, dataset description, visualizations/results, conclusion, and future scope. CO4 explicitly covers advanced classification and ensemble methods. The signed CA3 plan maps the case study to both CO3 and CO4; this remains a scope question, so the current work proceeds on the already-selected Experiment 12 track.
- Confirmed the project files are present at the recorded sizes; SHA-256 verification and row-level profiling are the next audit steps. No raw file has been changed and no model has been trained yet.

### 2026-10-14 01:20 IST — Model-comparison clarification and documentation preference

- User recalls that the professor recommended using multiple models and possibly an ensemble method. This supports the existing comparison plan: Logistic Regression as a reference, Random Forest as a bagging ensemble, and one boosting model. The specific boosting library and whether a combined voting model is useful remain undecided pending local runtime availability and validation results.
- User explicitly asked that every decision, change, action, and finding be logged for later review and learning. Continue adding dated entries to this file as work proceeds.
- User wants eventual materials to be proper, reproducible, and explainable, while remaining editable into a credible student-authored submission later. Keep the writing grounded and teachable; do not present drafts as the student's final voice or overstate findings.
- The first audit-script run completed the in-memory profiling pass but failed while writing report outputs: Windows returned `FileNotFoundError` for the generated path under `reports/`, even though the directory appeared present. No audit report was saved and the raw CSVs were not altered. Investigating output-folder write behavior before rerunning the script.

### 2026-10-14 01:21 IST — Processing documentation requirement

- User clarified that code must include comments and the data-processing history must be logged properly. Apply this to all scripts: explain each meaningful processing step and its rationale in comments; record source files/hashes, read settings, transformations, exclusions, split/model protocol, outputs, and verification status in `ACTION_LOG.md` and reproducible audit artifacts. Preserve raw files and keep derived processing separate.

### 2026-10-14 01:29 IST — Prepared-file audit completed and leakage-safe validation chosen

- Added a commented, read-only audit program at `scripts/audit_unsw_nb15.py` and a commented Windows runner at `scripts/run_audit.ps1`. The script records its run time and Python/pandas/NumPy versions, hashes inputs in 1 MiB chunks, reads CSV fields as strings with NA conversion disabled, profiles raw values, and records every audit stage. The runner saves derived JSON and Markdown files while leaving `data/raw/` untouched.
- The first direct Python report writes failed in this restricted OneDrive workspace (`FileNotFoundError`, then `Bad file descriptor`). The completed audit output was captured through stdout and written by PowerShell; the repeatable command is `& .\\scripts\\run_audit.ps1`. The successful run generated `reports/unsw_nb15_audit.json` and `reports/unsw_nb15_data_audit.md` at 01:28 IST.
- Both local files match the expected byte sizes, SHA-256 values, and official prepared split row counts: training 175,341 rows / 45 columns; testing 82,332 rows / 45 columns. Column names and order match. The target contains only 0 and 1. No raw empty cells or literal `NA`/`N/A`/`null`-style tokens were present. The common `service` token `-` is preserved as a source category and is not rewritten as missing.
- `label` is the target; 1 denotes attack. `attack_cat` maps deterministically to `label` in both splits (`Normal` -> 0; each of the nine named attack categories -> 1), so it is direct target leakage and is excluded. Exclude `id` too: IDs are unique within each file but each file restarts at 1, all 82,332 test ID values overlap the training range, and ID/label Pearson correlation changes from +0.727 in training to -0.387 in testing.
- Class shares differ between official partitions: training has 119,341 attack (68.06%) and 56,000 normal (31.94%); testing has 45,332 attack (55.06%) and 37,000 normal (44.94%). Report class-sensitive metrics and retain the official test mix in the primary result.
- No exact full-row matches occur across train and test. Predictor-only screening (42 fields, ignoring `id`, `label`, and `attack_cat`) found 1,302 distinct shared vectors covering 8,541 test rows; 296 matched test rows have a label not present for that same vector in training. Within training, 84,049 rows belong to repeated predictor vectors and 229 vectors (940 rows) have multiple labels; within testing, 34,704 rows repeat and 6 vectors (14 rows) have multiple labels. These are candidate feature-vector matches from deterministic pandas row hashes, not proof of invalid data; they show why a plain random row split would be misleading.
- Decision: hold out validation groups by the 42 predictor values so identical vectors cannot cross from fit to validation; use fixed-seed group-aware stratification when available and report achieved class counts. Keep the official test file untouched for final model comparison; add a clearly labeled secondary score on test rows whose predictor vectors were not seen in training. Do not delete or deduplicate the source split.
- The instructor's multiple-model suggestion is now explicitly represented as a simple reference plus Random Forest (bagging) and a boosting model. Local Python currently has pandas/NumPy but not scikit-learn or XGBoost, and its pip cache has no wheels; model training is still pending dependency resolution.

### 2026-10-14 01:31 IST — Reproducible multi-model analysis setup

- Decision following the user's clarification about the professor's recommendation: compare a Dummy prior baseline for context, Logistic Regression as the simple learned reference, Random Forest as a bagging ensemble, and HistGradientBoosting as a boosting ensemble. The ensemble pair addresses CO4 directly; the baseline helps explain whether the learned methods add value.
- Validation will use `StratifiedGroupKFold` with fixed seed and feature-vector hashes as groups, selecting one fold as validation. This attempts to preserve class proportions while preventing duplicate predictor vectors from crossing fit/validation; actual counts will be logged. The official test remains fixed until all models and parameters are set. Primary metrics are macro-F1 and attack recall; also report per-class precision/recall/F1, accuracy, and confusion matrices. A secondary official-test score will cover test vectors absent from training.
- Checked the official scikit-learn documentation for current grouped-stratification, pipelines/one-hot encoding, and ensemble classifier support. The local Python installation lacks scikit-learn/XGBoost and has no cached wheels. Proceeding with scikit-learn only in a project-local virtual environment; no global Python packages or raw inputs will be changed.

### 2026-10-14 01:32 IST — Isolated environment setup attempt

- Added `.gitignore` entries for the project-local `.venv/` and Python cache files so dependency setup does not clutter the student repo.
- Attempted `python -m venv .venv`; Python returned Windows `WinError 2` for the target directory before creating the environment. No package installation occurred and no source files were changed. Retrying after creating the destination directory with PowerShell, which has successfully created the audit outputs in this restricted OneDrive workspace.

### 2026-10-14 01:33 IST — Virtual environment creation retry

- After PowerShell created the project-local `.venv/` folder, `python -m venv .venv` progressed further but failed with `WinError 2` while creating `.venv\\Include`. No dependency installation or model training occurred. The audit scripts and reports remain complete. Next I am checking whether pre-creating this Windows venv directory structure resolves the path issue; `.venv/` is ignored by Git.

### 2026-10-14 01:34 IST — Project-local venv path remains blocked

- Pre-created `.venv\\Include`, `.venv\\Lib\\site-packages`, and `.venv\\Scripts` through PowerShell, then retried `python -m venv .venv`; Python still failed writing `.venv\\pyvenv.cfg` with `WinError 2`. No package installation occurred. The hidden `.venv/` folder contains only setup scaffolding and is excluded from Git.
- To avoid further churn inside the OneDrive project path, the next attempt will use the permitted temporary directory for this execution environment. The repository will retain dependency pins and commented run instructions so the analysis remains reproducible elsewhere.

### 2026-10-14 01:35 IST — Temporary environment setup attempt

- Retried environment creation in the permitted Windows temporary directory after the OneDrive project path rejected venv setup. Python created the environment scaffolding but its bundled `ensurepip` step failed; scikit-learn was not installed. Next I will create the venv without bundled pip and use the system pip tool to target that isolated interpreter if supported.

### 2026-10-14 01:37:51 +05:30 — Isolated model dependencies installed; fitting in progress

- The reproducible PowerShell runner created a temporary no-pip environment and installed the exact pinned requirements from requirements.txt: NumPy 2.5.3, pandas 3.0.6, and scikit-learn 1.9.1, plus their resolved dependencies. The project-local .venv remains incomplete and ignored; the temporary environment is used only within this run.
- The model workflow is now running against the verified local prepared CSVs. No result is recorded until grouped validation, full-training refits, official-test metrics, secondary unseen-vector metrics, and output checks complete.

### 2026-10-14 01:39 IST — Leakage-aware model comparison completed

- Logging correction: the first auto-generated entry interpreted Markdown backticks as PowerShell escape sequences and failed to interpolate nested input hashes. Replaced it with verified values; the runner now formats log lines without that interpolation pattern and appends UTF-8 text.
- Runner: `scripts/run_models.ps1`; model code: `scripts/train_unsw_nb15_models.py`; Python 3.12.10, pandas 3.0.6, NumPy 2.5.3, scikit-learn 1.9.1. Matplotlib 3.11.2 was installed on the analysis environment later for figures; the training metrics were not refit for that chart change.
- Verified training input: `data/raw/UNSW_NB15_training-set.csv`, 175,341 rows, 32,293,018 bytes, SHA-256 `BEC7DD5EC88DC2A0CCC7A07879D338395ED7421750F675FD0339E07DFE0648FA`. Testing input: `data/raw/UNSW_NB15_testing-set.csv`, 82,332 rows, 15,380,800 bytes, SHA-256 `734FE6642EDF758F7C94D7D9149426B49D202FE8E7BF0BEF47392489C3C0A559`. Raw files were not changed.
- Target: `label` (attack=1). Used 42 predictor fields; excluded `id` and `attack_cat`. Seed=42. Validation: first fold from `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)`, grouped by hashes of parsed predictors. Fit rows=140,274; validation rows=35,067; group overlap=0. Fit class counts={"0":44,800,"1":95,474}; validation counts={"0":11,200,"1":23,867}.
- Official test has 82,332 rows: 8,541 with training-seen predictor vectors and 73,791 unseen predictor vectors. All official and unseen-subset result rows were retained; no source rows were dropped.
- Fixed comparison: Dummy prior reference, balanced Logistic Regression, balanced Random Forest (bagging), and balanced HistGradientBoosting (boosting). Preprocessing was inside each pipeline. Full settings, per-class metrics, confusion matrices, warnings, timings, and step-by-step processing are saved in `reports/unsw_nb15_model_results.json` and `.md`.
- Official-test summary (macro-F1 / attack recall / accuracy): Dummy 0.3551 / 1.0000 / 0.5506; Logistic Regression 0.8292 / 0.9306 / 0.8353; Random Forest 0.9008 / 0.9731 / 0.9036; HistGradientBoosting 0.9080 / 0.9665 / 0.9102. The dummy model predicts every row as attack, so its perfect attack recall comes with zero normal recall and is not useful by itself. Random Forest has the highest attack recall; HistGradientBoosting has the best macro-F1 and accuracy. These are dataset benchmark results, not live-network evidence.
- Secondary unseen-predictor macro-F1 / attack recall: Dummy 0.3415 / 1.0000; Logistic Regression 0.8200 / 0.9180; Random Forest 0.8973 / 0.9685; HistGradientBoosting 0.9048 / 0.9607. No fitting warnings were recorded.
- Model outputs: `reports/unsw_nb15_model_results.json`, `reports/unsw_nb15_model_results.md`, `reports/unsw_nb15_model_metrics.csv`. Initial custom SVG figures were superseded by Matplotlib PNG figures in a separately logged chart regeneration; no models were retrained for that chart update.
### 2026-10-14 01:45:58 +05:30 — Figure generation and result-file checks

- Added `scripts/plot_unsw_nb15_results.py` with explanatory comments. It reads only the saved model-result JSON and builds a grouped official-test macro-F1/attack-recall chart plus a four-panel confusion-matrix figure using Matplotlib 3.11.2. Added the exact Matplotlib pin to `requirements.txt`; `scripts/run_models.ps1` now regenerates and saves the PNGs from JSON on future reruns.
- The first figure-generation attempt failed before saving files because the plot parser treated nested confusion-matrix integer arrays as strings. Inspection of the JSON showed the stored shape is a 2-by-2 integer array. Updated the parser to match that schema; the rerun completed and both PNGs passed signature checks.
- Updated `reports/unsw_nb15_model_results.md` and JSON processing/runtime records to name the PNG charts and Matplotlib version. Removed the two superseded SVG files from `reports/` after checking the Markdown references pointed to the new PNGs.
- Recalculated accuracy, attack recall, macro-F1, and confusion-matrix row totals for validation, official test, and unseen-vector test results for all four models: all 12 confusion matrices matched their recorded row counts and all checked metrics agreed within floating-point tolerance. Verified both input hashes again and confirmed fit/validation group overlap=0 and seen-plus-unseen test rows=82,332.
- Visually inspected both rendered charts. This was a report-only change: no source data changed and no models were refit. The earlier plotting error and correction are retained here so the processing history is complete.
### 2026-10-14 01:47:01 +05:30 — Data-processing detail added to the model record

- Expanded the commented model script, JSON processing record, and Markdown report after checking the actual pipeline code. The raw CSV remains text-preserved on read (`keep_default_na=False`, `na_filter=False`); `label` becomes binary `y`, while `id` and `attack_cat` are excluded before feature preparation.
- Numeric fields are coerced explicitly, and any invalid numeric values stop the run for inspection. The pipeline includes median imputation; Logistic Regression additionally standardizes numeric columns. Categorical `proto`, `service`, and `state` use a constant `__MISSING__` fill followed by one-hot encoding with unseen categories ignored. The literal service token `-` remains a category. The audit found no empty source cells, so the imputation steps are safeguards rather than evidence that missing values were present.
- Every learned preprocessing component is fitted within its model pipeline on the current fit partition (then on full official training for final test scoring). No resampling or raw-file rewriting occurs. The processing record now says these steps explicitly instead of using the broader phrase “preprocessing inside each pipeline.”
### 2026-10-14 01:48:13 +05:30 — Removed failed virtual-environment scaffold

- Removed the exact project `.venv` directory after confirming it contained only four empty folders (`Include`, `Lib`, `Lib/site-packages`, `Scripts`) from the earlier failed setup attempts. No environment files or packages were present. The reproducible runner still uses an isolated temporary environment and the project `.gitignore` continues to exclude `.venv/` if setup is retried elsewhere.
### 2026-10-14 01:48:22 +05:30 — Final report/log consistency check

- The closing consistency pass found the Markdown processing list differed from its JSON companion only by a comma in step 10. Aligned the Markdown text; no processing step or metric changed. Final checks confirmed the two PNG links resolve, the JSON/Markdown processing steps match, both source hashes match their recorded values, group overlap remains zero, and test seen/unseen counts sum to all 82,332 official test rows.

### 2026-10-14 01:50 IST — Current status summary refreshed after model completion

- Updated the overview and next-step sections of this log because their earlier checklist still described dataset acquisition and model training as pending. The chronological entries remain intact as historical records.
- Current remaining work is course-scope/metadata confirmation, final source verification for the literature review, and the full course-template report with its required screenshots. Experiment 13 is conditional on the instructor confirming that CA3 includes it.

### 2026-10-14 02:17:34 IST — Applying the authorized review suggestions

- User authorized applying the changes reported in the preceding review. The review had left all 29 project files unchanged and independently reproduced every model metric, all 2,890 audit fields, and the figures. These findings are now being recorded in this log.
- Preserved the original reports, scripts, requirements, literature matrix, and action log in reports/runs/20261014-021734-before-review before changing them. This snapshot retains the original fitted-result evidence and source code.
- Planned changes: simplify the unused imputation policy; record effective model parameters and explain fixed choices; add a student walkthrough and run guide; record successful/failed audit and model runs in dated folders; improve chart labels/layout and result interpretation; correct the literature page range and distinguish theory/lab scope.

### 2026-10-14 02:27:41 IST — audit run: failed

- Dated evidence: reports/runs/20261014-022741-448-audit/
- Task: audit; started IST: 2026-10-14T02:27:41.4485128+05:30
- Python command: C:\Users\shory\AppData\Local\Temp\sml-revision-c2eb87323244431b94ec84c05c37ad14\deliberately-missing-python.exe
- Failure: The term 'C:\Users\shory\AppData\Local\Temp\sml-revision-c2eb87323244431b94ec84c05c37ad14\deliberately-missing-python.exe' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
- Finished IST: 2026-10-14T02:27:41.5647726+05:30; status: failed

### 2026-10-14 02:28:08 IST — audit run: success

- Dated evidence: reports/runs/20261014-022741-763-audit/
- Task: audit; started IST: 2026-10-14T02:27:41.7639516+05:30
- Python command: C:\Users\shory\AppData\Local\Temp\sml-revision-c2eb87323244431b94ec84c05c37ad14\Scripts\python.exe
- 1. Read-only source audit: opened the prepared CSVs under data/raw; source bytes were not changed.
- 2. Integrity: computed SHA-256 in 1 MiB chunks and compared digest, byte size, and row count to the acquisition record.
- 3. Parsing: read as strings with keep_default_na=False and na_filter=False to preserve empty cells and literal text.
- 4. Profiling: counted empty/whitespace/blank-like cells, distinct and frequent values, and numeric ranges/quantiles; numeric coercion was temporary and diagnostic only.
- 5. Target audit: counted label values and cross-tabulated attack_cat against label; label is y and attack_cat is excluded as target-derived.
- 6. Split screen: omitted id, label, and attack_cat from candidate predictors; hashed full rows and predictor-only rows to screen overlap.
- 7. Reporting: generated derived JSON and Markdown outputs; this audit did not train a model.
- Input testing: 82332 rows; 15380800 bytes; SHA-256 734FE6642EDF758F7C94D7D9149426B49D202FE8E7BF0BEF47392489C3C0A559
- Input training: 175341 rows; 32293018 bytes; SHA-256 BEC7DD5EC88DC2A0CCC7A07879D338395ED7421750F675FD0339E07DFE0648FA
- Finished IST: 2026-10-14T02:28:08.1224265+05:30; status: success

### 2026-10-14 02:30:06 IST — models run: success

- Dated evidence: reports/runs/20261014-022808-214-models/
- Task: models; started IST: 2026-10-14T02:28:08.2146166+05:30
- Python command: C:\Users\shory\AppData\Local\Temp\sml-revision-c2eb87323244431b94ec84c05c37ad14\Scripts\python.exe
- 1. Re-verified staged training/testing file sizes, SHA-256 digests, and row counts before modeling.
- 2. Read source CSVs as strings with NA coercion disabled; did not alter or rewrite raw files.
- 3. Constructed y from label and X from the 42 flow predictors only; removed id and attack_cat before preprocessing.
- 4. Parsed the 39 numeric predictors with numeric coercion and an explicit invalid-value check; retained proto, service, and state as categories, including service '-'.
- 5. Hashed parsed X vectors only to create feature groups; group hashes were never input to any estimator.
- 6. Selected the first fixed-seed StratifiedGroupKFold split; verified zero feature groups crossed fit/validation.
- 7. Verified complete/finite numeric and nonempty categorical fields; applied no imputation. Inside training-only pipelines, standardized numeric fields for Logistic Regression and one-hot encoded categories with unknown-category ignore; fit the predefined Dummy, Logistic Regression, Random Forest, and histogram boosting models, with no resampling or hyperparameter tuning.
- 8. Recorded validation metrics, then refit each unchanged model configuration on all official training rows and evaluated the official test rows.
- 9. Calculated a secondary metric set only on test rows whose predictor vectors were absent from the full training split.
- 10. Generated result JSON, Markdown, Matplotlib PNG charts, and a tidy CSV using derived outputs only.
- Input testing: 82332 rows; 15380800 bytes; SHA-256 734FE6642EDF758F7C94D7D9149426B49D202FE8E7BF0BEF47392489C3C0A559
- Input training: 175341 rows; 32293018 bytes; SHA-256 BEC7DD5EC88DC2A0CCC7A07879D338395ED7421750F675FD0339E07DFE0648FA
- dummy_prior: official-test accuracy=0.5506, macro-F1=0.3551, attack recall=1.0000; fixed settings={"strategy":"training class prior"}
- hist_gradient_boosting: official-test accuracy=0.9102, macro-F1=0.9080, attack recall=0.9665; fixed settings={"class_weight":"balanced","early_stopping":false,"l2_regularization":0.1,"learning_rate":0.1,"max_iter":100,"max_leaf_nodes":31,"min_samples_leaf":20,"random_state":42}
- logistic_regression: official-test accuracy=0.8353, macro-F1=0.8292, attack recall=0.9306; fixed settings={"C":1.0,"class_weight":"balanced","max_iter":500,"random_state":42,"solver":"lbfgs"}
- random_forest: official-test accuracy=0.9036, macro-F1=0.9008, attack recall=0.9731; fixed settings={"class_weight":"balanced_subsample","max_depth":20,"max_features":"sqrt","min_samples_leaf":2,"n_estimators":150,"n_jobs":-1,"random_state":42}
- Validation group overlap: 0
- Full effective classifier parameters, preprocessing policy, fit warnings, timings, and runtime versions are in the archived JSON.
- Finished IST: 2026-10-14T02:30:06.8385916+05:30; status: success

### 2026-10-14 02:37:42 IST — Review fixes completed and verified

- Simplified missing-value handling: removed unused imputers, retained training-only numeric scaling for Logistic Regression and one-hot encoding for the three categories, and added explicit checks for empty/invalid/infinite inputs. Four meaningful guard checks rejected blank duration, infinite duration, empty protocol, and an invalid label that could otherwise overflow int8; the service token `-` was accepted unchanged.
- Added the omitted explicit settings (boosting early_stopping=False, random seeds, forest parallelism), full effective classifier parameters, preprocessing policy, and dependency versions to the model JSON. Added plain explanations of the fixed starter settings; no parameter/threshold tuning or new classifier was introduced.
- Added README.md, STUDENT_WALKTHROUGH.md, and EXPERIMENT_12_REPORT_DRAFT.md. The draft follows the classification template with five related studies, three objectives, algorithm/equations, metrics, implementation, actual results, limitations, conclusion, and future work. Cover details, literature acceptance, screenshots, and student review remain pending.
- Clarified one grouped holdout rather than averaged five-fold CV; separated unfamiliar predictor combinations from new attack types; described completed/precomputed flow prediction and the false-alarm trade-off. The report explains the Dummy baseline and Random Forest's 299 additional detections versus 845 additional false alarms relative to boosting.
- Replaced duplicated Windows setup wrappers with a shared, commented runner using one explicitly selected environment. Both audit and model runs keep dated source/output snapshots, manifests with file hashes, and success/failure notes. Latest reports are published only after all calculations and figures complete.
- Checked the failure branch with a deliberately nonexistent Python interpreter. The expected failed run is preserved under reports/runs/ with a failed manifest; the latest audit stayed unchanged. This was a deliberate logging test, not an unexplained analysis failure.
- Successful audit and model reruns are preserved in reports/runs/20261014-022741-763-audit/ and reports/runs/20261014-022808-214-models/. Every new model metric and confusion matrix matched the preserved original run within floating-point tolerance; the grouped validation overlap remained zero. Raw CSV hashes still match the acquisition record.
- Changed confusion figures to a readable 2-by-2 layout and model labels to ordinary names. Corrected Telikani et al.'s page range to 3880–3890, and marked advanced methods in the five papers as related work rather than implemented methods.
- Corrected current scope wording: theory code 0701260304 and lab code 0701260405 appear to identify separate courses. The historical planning chat explicitly requests both case studies, so Experiment 13 regression is pending; do not treat the current classification study as complete for CO3. Moved the earlier 01:50 status entry into chronological order while retaining historical entries.

### 2026-10-14 02:37:42 IST — Authorized GitHub upload preparation

- User explicitly requested uploading the completed project to Shorya-Raj/SML-casestudy using GitHub formatting. The connected GitHub account and Git credential manager are Shorya-Raj; repository metadata confirms private visibility, write access, default main branch, and no existing remote refs. Preserve private visibility.
- Organized nine original course documents under course_materials/ and two historical notes under notes/ without modifying their contents. Added folder guides, input provenance/creator attribution, and repository links in standard Markdown. Existing historical file locations in older log entries describe where files were at that time.
- Included the prepared CSVs, code, reports, dated evidence, draft, logs, literature material, and course references in the upload scope. Virtual environments, cache files, credential/config folders, and temporary files are excluded. No blanket license is assigned to third-party data or course documents.
- Added Git attributes protecting raw CSVs and dated archives from newline normalization so their recorded byte hashes remain valid after checkout. Publication and remote verification will be recorded after the initial upload.

### 2026-10-14 02:42:26 IST — GitHub publication verified

- Uploaded all 88 project files to the private repository [Shorya-Raj/SML-casestudy](https://github.com/Shorya-Raj/SML-casestudy) on main. Initial project commit: 942333d9ab22398739570e83d758130b5e21cb08.
- Verified the remote main reference equals the local project commit. Fetched README.md through the connected GitHub service and confirmed its Markdown content, report links, relative chart image, setup commands, scope, and limitations are present remotely. Repository metadata still reports private visibility.
- Before upload, compared Git's staged bytes against all 47 dated manifest entries and both raw CSVs; every digest matched. This verifies the archive and raw-data newline protections. Standard current Markdown/code files use Git-compatible text formatting.
- Local working tree was clean after the initial upload. This publication record is being committed as a follow-up documentation update; no source code, data, or model outputs changed during publication.
- Submission work remains: final cover details, instructor acceptance of the literature selection, code/output screenshots and final course-format report, plus Experiment 13 regression.

### 2026-10-14 — Case study learning guide created

- Added 12 linked Markdown learning documents under CASE_STUDY_LEARNING_GUIDE/: scope, sourcing, audit/features, preprocessing, grouped splitting, model families, code tour, metric calculations, alternatives, literature/limitations, and viva self-check.
- Used the saved audit and model reports plus the current scripts as evidence; linked the existing generated comparison and confusion-matrix figures. No raw CSV, model, metric, or figure was changed, and no model rerun was claimed.
- Highlighted that the grouped validation used one fold, forest led validation macro-F1 slightly, boosting led official-test macro-F1, and the current Python 3.15 source requirement differs from the saved Python 3.12 run record.


### 2026-10-15 — Learning guide Part 01 expanded and exported

- Rewrote CASE_STUDY_LEARNING_GUIDE/01_PROBLEM_AND_SCOPE.md in slower, plain-language teaching order: flow record, imaginary example, X and y, training versus prediction, four possible outcomes, excluded fields, prediction timing, and answer checks.
- Created CASE_STUDY_LEARNING_GUIDE/DOCX/01_PROBLEM_AND_SCOPE.docx with an embedded flow diagram and tables. Installed Word converted this DOCX to a temporary four-page PDF for layout review after the packaged LibreOffice renderer was unavailable; all four rendered pages were visually inspected. The PDF and page images are QA files under .docx_build, not deliverables.
- The remaining chapter DOCX drafts were held under .docx_build/drafts while their explanations await the same simplification. No raw data, model code, or results changed in this step.


### 2026-10-15 — Complete plain-language learning guide exported

- Expanded Parts 02–11 into slower, worked explanations with small examples, decision reasons, answer checks, diagrams, and the saved case-study evidence. Part 01 remains the recommended starting point.
- Exported eleven individual Word chapters and one 31-page combined guide to CASE_STUDY_LEARNING_GUIDE/DOCX/ using scripts/export_learning_guide_docx.py. The earlier note that chapter drafts were held is superseded by this completed export.
- Checked all twelve DOCX packages for integrity and rendered their pages through installed Word for layout review. The packaged LibreOffice renderer was unavailable. No dataset, model training, or reported result was changed.

### 2026-10-15 — Parts 02–11 simplified to match Part 01

- Expanded all ten later learning chapters from roughly 900–1,200 words each to roughly 1,500–1,750 words each, using everyday explanations, small imaginary examples, worked reasoning, common confusions, and explicit links back to the saved case-study evidence. Part 01 was retained as the teaching-style reference.
- Regenerated all eleven chapter DOCX files and the 41-page complete Word guide with scripts/export_learning_guide_docx.py. Added direct Word links in README.md.
- Checked all twelve DOCX packages, local Markdown links, and Word-rendered PDF page layouts. The rendered PDFs and contact sheets were temporary quality-assurance files, not deliverables. No source CSV, model training, or saved metric was changed.

### 2026-10-19 — Experiment 12 report rewritten

- Created `Experiment_12_UNSW_NB15_Case_Study_Report_Rewritten.docx` from the supplied classification report template, retaining its section order and department header. The earlier Word report remains available separately.
- Rechecked five primary journal papers and four further references. The literature section has per-paper fields for reference, task, method, finding, contribution, limitation, and research gap, followed by a comparison across studies. The limited access to Mohiuddin et al.'s full methods and result tables is stated in the report.
- Matched the displayed test metrics and confusion counts to the saved 2026-10-14 model JSON at the shown precision; both figures match the dated run copies by SHA-256. The report identifies that archived run as the source of its numbers because the current training script has since changed.
- Rendered the report with Word and inspected the page layout. The final report has 10 pages, 10 tables, two figures, references [1]–[9], and a conclusion that starts on a new page. Checked the DOCX package for corruption, hidden text, invisible control characters, comments, custom XML, and embedded extras; none of those markers were found.
- Local phrase searches and comparison with the earlier draft found no obvious lifted source prose, but cannot establish a 0% similarity score. Automatic approval review rejected sending unpublished report text to QuillBot for an external AI scan because the service is a third party and the report may contain private project material. No external checker result is claimed.
### 2026-10-19 — Course-level review and student workflow

- Read the supplied third-semester SML lab manual. Experiment 12 is an open classification case study; its earlier exercises cover EDA, encoding, scaling, Logistic Regression, Random Forest, and boosting ideas. XGBoost with grid search belongs to Experiment 11, so it is not presented as an Experiment 12 requirement.
- Checked the official UNSW-NB15 source and scikit-learn/Python documentation. Kept the prepared official train/test split, the three learned model families plus a Dummy baseline, and the existing report limits. Histogram Gradient Boosting remains accurately named; it is not described as XGBoost.
- Added scripts/explore_unsw_nb15.py and generated reports/unsw_nb15_eda_summary.md plus reports/unsw_nb15_eda_charts.png. The EDA confirms 175,341/82,332 rows, class counts, no missing or exact empty cells, and no exact full-row duplicates in either supplied file. The raw CSVs were not changed.
- Simplified scripts/train_unsw_nb15_models.py to ordinary Python imports and a short official train/test comparison without in-code explanatory comments. Detailed grouped validation, data audit, and run archives remain in separate supporting files. Adjusted the runner's minimum Python version from 3.15 to 3.12.
- Re-ran the final compact trainer with temporary local dependencies. All four official-test accuracy, macro-F1, attack precision/recall, and confusion counts matched the saved report at displayed precision. The separate research validation check found zero shared predictor groups. No new model tuning was performed.
- Updated README.md, STUDENT_WALKTHROUGH.md, the course review, and the code-tour Markdown/Word guides to explain the split between professor-facing and supporting code. Rendered and visually checked the revised Word guides. The rewritten Experiment 12 report and earlier draft remain separate; instructor cover details, screenshots, and Experiment 13 regression still need separate work.

### 2026-10-27 01:59:35 IST — Experiment 12 report cross-validation and limited edit

- User supplied the Project Report Making Guide and selected its "Editing an existing report" approach. The clarified scope was to cross-check the current Experiment 12 DOCX and improve only supported issues. Kept Experiment_12_UNSW_NB15_Case_Study_Report_Rewritten.docx unchanged as the source (SHA-256 54E9B8BEE02421F81DDFC8436A83466F86F6275C34BF8E93B4744FFC63DC7B92); saved a separate Experiment_12_UNSW_NB15_Case_Study_Report_Reviewed.docx (SHA-256 2D93F22BED8D4B0E16D22A242ED350155A1136A29B160A543729BB63F42269A2).
- Read the specific Lab Assignment 12 template and the SML lab manual. The DOCX covers the required title, aim, problem, literature, three objectives, steps/equations/metrics, implementation/tools, linked data, results/figures, conclusion, and future scope. It reviews five recent journal papers. The manual's broader lab-notebook instruction also asks for code snippets and output screenshots; the current case-study DOCX links code and contains actual generated figures but has no code or terminal screenshot pages. Add genuine student-run evidence if this DOCX must also serve as that notebook; do not invent screenshots.
- Independently streamed both prepared CSV files without changing them. Confirmed 42 allowed predictors, training 175,341 rows (56,000 normal; 119,341 attack), testing 82,332 rows (37,000 normal; 45,332 attack), and both stored SHA-256 hashes. An independent BLAKE2b vector screen reproduced 8,541 test rows with a training predictor-vector match and 296 matched rows whose label conflicts with the training label.
- Compared all 28 numeric cells in the Word test-metrics and error-count tables with reports/unsw_nb15_model_results.json; they match at displayed precision. Recomputed the 299 additional Random Forest detections, 845 additional false alarms, and the 15.88%/18.16% normal-flow false-alarm rates. The three grouped-validation and three unseen-vector macro-F1 values also match. The model metadata records 140,274 fitting and 35,067 validation rows with zero overlapping predictor groups. The two PNGs embedded in Word have byte-for-byte matching SHA-256 hashes with the saved report figures.
- Checked the wording and citation metadata against the official UNSW dataset page; full publisher or institution-hosted papers for Maseno, Kiflay, Pospíchal, Telikani, and Apruzzese; the Viegas author-hosted paper; and the accessible publisher record for Mohiuddin. The Mohiuddin full methods/results remain inaccessible, so its claim was narrowed. Scikit-learn's RandomForestClassifier documentation confirms that class probabilities are averaged across trees.
- Made four narrow text edits in the reviewed copy: replaced two unverified first-person claims with neutral report wording; described Random Forest probability averaging accurately; and removed an unverified binary/multiclass detail from the Mohiuddin paper table. Added a page break before Table 3 so that its caption and complete table stay together instead of a clipped continuation across pages. No other paragraph text, table cell text, styles, margins, or embedded images changed.
- Exported source and reviewed DOCX files through Microsoft Word for visual QA after the bundled LibreOffice renderer was unavailable. Both versions have 10 pages. Rendered and inspected all 10 pages of the reviewed copy; no clipping, overlap, broken tables, or missing glyphs observed. Temporary QA PDF/PNG files are not report deliverables. No new model fit or change to raw data occurred in this report review.
- Still pending before hand-in: student/cover details, instructor acceptance of literature and submission format, and any genuine code/output screenshots required by the lab notebook. This is a reviewed working report, not a submitted assignment.
### 2026-10-27 — Experiment 12 report revised in the requested student voice

- User asked for the Experiment 12 report wording to follow the plain, student-like voice requested during the SML CA3 report work, while keeping the current project context. I used direct first-person explanations for project choices and findings, simpler descriptions of technical steps, and restrained commentary suited to intrusion detection rather than carrying over sports language.
- Created Experiment_12_UNSW_NB15_Case_Study_Report_Student_Voice.docx as a separate copy. The earlier reviewed file was open in another process, so I used the unchanged rewritten source and reapplied its fact-check corrections and Table 3 page break before the voice edit. Neither earlier DOCX was overwritten.
- Reworded 41 narrative paragraphs across the aim, problem, literature discussion, methodology, implementation, results, conclusion, and future scope. Revised five table cells for consistent project-focused language and to keep the Mohiuddin claim narrow. Kept headings, references, citation numbers, result tables, figures, class counts, metrics, and model settings unchanged.
- Updated the Random Forest explanation to say that it averages class probabilities from its trees before selecting a class. Retained the limitation that the test results concern the prepared benchmark and do not establish live or unknown-attack detection.
- Compared the new DOCX with its source: 102 paragraphs, 10 tables and two embedded figures remain; the references and numeric result tables are unchanged; the package is valid. No dataset, training run, or model output changed.
- Exported the final copy through Microsoft Word and inspected all ten page images. No clipping, overlap, missing glyphs, or broken tables were observed. Temporary PDF and page images are QA files, not deliverables.
- SHA-256 for the new DOCX: 38FEADC098FD5E9B7C13EEDEF6FBE44116DE4E139F2591DABFF6D0A16E36B44E.
