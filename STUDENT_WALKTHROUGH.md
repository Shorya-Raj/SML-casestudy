# Understanding the classification study

The question is: **using the prepared features of a network flow, how well can three classifiers distinguish normal traffic from attack traffic?** We compare a simple learned model with two tree ensembles and examine the kinds of errors they make.

This is ordinary pandas/scikit-learn work. The libraries implement the algorithms; our work is preparing the inputs, choosing a sensible comparison, evaluating it fairly, and explaining its limits. The full audit and report-generating helpers support the study.

## 1. Understand one row and the target

Each prepared row is a flow record. `label = 0` means normal and `label = 1` means attack. These features have already been extracted from traffic; the project does not capture packets itself.

Some easy-to-understand inputs are `proto` (protocol), `service` (service category), `state` (connection state), `dur` (flow duration), `spkts`/`dpkts` (source/destination packet counts), and `sbytes`/`dbytes` (source/destination byte counts). Check exact definitions and units in the official feature description before quoting them in a report. Total counts and duration generally require observing the recorded flow, so this experiment is not evidence of early detection.

## 2. Audit before changing values

The audit reads source fields as strings and disables automatic missing-value conversion. It checks file hashes, rows/columns, blank values, numeric values, class counts, duplicate inputs, and label relationships. Raw CSVs are preserved. The prepared pair has 175,341 training rows and 82,332 test rows, with 45 columns each.

```python
# Preserve literal source tokens while examining the CSV.
frame = pd.read_csv(path, dtype=str, keep_default_na=False, na_filter=False)
```

The actual audit is `scripts/audit_unsw_nb15.py`. Its long per-column output belongs in supporting evidence rather than the main results discussion.

## 3. Make X and y

`y` is the answer the model must predict. `X` contains inputs available for prediction. Remove `label`, `attack_cat`, and `id` before fitting:

```python
# attack_cat reveals the target; id is a prepared row identifier.
X = frame.drop(columns=["label", "attack_cat", "id"])
y = pd.to_numeric(frame["label"])
```

`attack_cat` describes the known attack family: every normal category maps to label 0 and attack categories map to 1. Including it would let the model read the answer. IDs restart between the files and are not traffic measurements. After these exclusions there are 42 predictors.

The real `prepare_features()` function also checks column order and valid 0/1 labels, parses numeric values, and stops on incomplete or invalid inputs. These files are complete, so no values are imputed. The literal service value `-` stays a category.

## 4. Keep identical inputs together in validation

Many rows have the same predictor values. A random row split could put identical inputs in both fitting and validation data. We give identical predictor vectors the same group and keep each group on one side.

```python
# Group keys are used for splitting only; they are never model inputs.
groups = pd.util.hash_pandas_object(X, index=False).to_numpy()
splitter = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
fit_rows, validation_rows = next(splitter.split(X, y, groups=groups))
```

`next(...)` takes only the first fold. It gives one approximately 80/20 grouped holdout, not five fitted folds with averaged scores. The recorded split has 140,274 fitting rows and 35,067 validation rows, with zero shared predictor groups. Grouping exact inputs does not prove that hosts, sessions, or capture days are independent.

## 5. Encode and scale inside the training pipeline

The three category fields are one-hot encoded: categories become separate indicator columns. Unknown test categories are ignored by the encoder. The encoder learns categories from the fitting rows only.

```python
encoder = OneHotEncoder(handle_unknown="ignore")
```

Logistic Regression uses `StandardScaler` for the 39 numeric fields, which have different ranges. The tree models use their original numeric values. A `ColumnTransformer` applies the appropriate transformation to each type of column. A `Pipeline` fits these transformations and the classifier together, preventing validation/test information from influencing learned preprocessing.

## 6. Compare the fixed models

- **Dummy baseline:** uses the training class prior. Here it predicts every row as attack. This shows why high attack recall alone can be unhelpful.
- **Logistic Regression:** learns a linear relationship between the features and the log odds of attack. It is the simple learned reference.
- **Random Forest:** builds many trees on bootstrap samples and random subsets of features. Combining them is a form of bagging.
- **Histogram Gradient Boosting:** builds trees sequentially to improve the previous predictions. Binning feature values makes this built-in implementation efficient for a large table.

Random Forest and boosting are each ensembles of trees. We do not combine the three learned classifiers into a separate voting/stacking model.

Read `model_pipelines()` for the exact code. The report explains chosen settings such as 150 forest trees, depth 20, and 100 boosting iterations. They are fixed starter settings, not the outcome of a hyperparameter search. Class weights balance the total influence of normal and attack rows; they do not create synthetic rows. Seed 42 helps repeat the experiment.

## 7. Fit, predict, and score

For every model, fit on the fitting partition and score the grouped holdout. Then create the same model configuration again, fit on all official training rows, and score the official test file. Never fit encoders/scalers on the test file or adjust the settings to improve its results.

```python
# The same pipeline fits preprocessing on training rows only.
model.fit(X_fit, y_fit)
validation_predictions = model.predict(X_validation)
```

`run_analysis()` performs this comparison; `measure()` calculates the metrics. The second fit uses full training rather than adding validation/test rows to the final test file.

## 8. Explain the measures

With attack as the positive class:

- **TP:** attack correctly detected. **FN:** attack incorrectly called normal.
- **FP:** normal flow incorrectly flagged as attack. **TN:** normal flow correctly called normal.
- Accuracy = `(TP + TN) / all rows`.
- Attack precision = `TP / (TP + FP)`; how many attack flags are correct?
- Attack recall = `TP / (TP + FN)`; how many attacks are found?
- F1 = `2 * precision * recall / (precision + recall)`.
- Macro-F1 = the mean of normal-class F1 and attack-class F1, giving both classes equal importance.
- Balanced accuracy = the mean of the two class recalls.
- ROC-AUC measures how well attack scores rank attacks above normal flows across thresholds. It is not accuracy at the chosen prediction threshold.

The code uses the classifier's ordinary `predict()` decision rule and records attack probabilities for ROC-AUC. No decision-threshold tuning was performed.

## 9. Interpret actual errors

The report shows that Random Forest finds 299 more attacks than boosting but produces 845 more false alarms on this test set. Boosting's 91.0% accuracy still comes with a 15.9% false-alarm rate among normal flows. Which trade-off is preferable depends on the application's cost of missed attacks and unnecessary alarms.

The official test contains 8,541 rows whose predictors also appeared in training. We preserve the official result and add a secondary score on the other 73,791 rows. This is a subset of the same test file and does not establish detection of new attack families.

## 10. Connect evidence to the submission

Use the README commands so the run saves dated evidence and records success or failure. The current source files and output hashes are preserved in each run folder. The JSON records software versions, effective classifier parameters, preprocessing policy, group counts, warnings, and fit times.

For the course report, explain the aim, up to three objectives, relevant literature, dataset, algorithm steps, equations, implementation, results, limitations, conclusion, and future work. Add real code/output screenshots as required by the lab manual. Confirm whether the professor wants lab Experiment 12 alone or theory CA3 with regression evidence too. The current study covers classification.

## Questions to practise answering

Why remove `attack_cat` and `id`? Why fit the encoder/scaler only on training rows? Why group identical inputs? How does bagging differ from boosting? Why can the Dummy baseline have perfect attack recall? What do the false alarms and missed attacks imply? What does the unseen-input subset actually measure?
