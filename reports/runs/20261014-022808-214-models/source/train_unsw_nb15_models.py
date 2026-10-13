#!/usr/bin/env python3
"""Run the documented leakage-aware binary UNSW-NB15 model comparison."""

from __future__ import annotations

import hashlib
import json
from importlib.metadata import version
import platform
import sys
import time
import warnings
from datetime import datetime, timedelta, timezone
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
REPORTS = ROOT / "reports"
SEED = 42
N_SPLITS = 5
TARGET = "label"
EXCLUDED = {"id", "attack_cat", TARGET}
CATEGORICAL = ["proto", "service", "state"]
MODEL_NAMES = {
    "dummy_prior": "Dummy baseline",
    "logistic_regression": "Logistic Regression",
    "random_forest": "Random Forest",
    "hist_gradient_boosting": "Histogram Gradient Boosting",
}
EXPECTED = {
    "training": {
        "name": "UNSW_NB15_training-set.csv",
        "rows": 175_341,
        "bytes": 32_293_018,
        "sha256": "BEC7DD5EC88DC2A0CCC7A07879D338395ED7421750F675FD0339E07DFE0648FA",
    },
    "testing": {
        "name": "UNSW_NB15_testing-set.csv",
        "rows": 82_332,
        "bytes": 15_380_800,
        "sha256": "734FE6642EDF758F7C94D7D9149426B49D202FE8E7BF0BEF47392489C3C0A559",
    },
}


def sha256_file(path: Path) -> str:
    """Hash source bytes in chunks so the audit does not load a file at once."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def load_source_split(name: str) -> tuple[pd.DataFrame, dict[str, object]]:
    """Verify the staged official file, then preserve its raw text fields."""
    spec = EXPECTED[name]
    path = RAW / str(spec["name"])
    actual_size = path.stat().st_size
    actual_hash = sha256_file(path)
    if actual_size != spec["bytes"] or actual_hash != spec["sha256"]:
        raise ValueError(f"Integrity check failed for {path.name}; see ACTION_LOG.md for expected values.")

    # Prevent pandas from silently changing empty strings or category tokens.
    frame = pd.read_csv(path, dtype=str, keep_default_na=False, na_filter=False, low_memory=False)
    if len(frame) != spec["rows"]:
        raise ValueError(f"Unexpected row count in {path.name}: {len(frame):,}")
    return frame, {"file": path.name, "bytes": actual_size, "sha256": actual_hash, "rows": len(frame)}


def prepare_features(frame: pd.DataFrame, expected_columns: list[str] | None = None) -> tuple[pd.DataFrame, pd.Series]:
    """Create X/y without target-derived fields or row identifiers."""
    if TARGET not in frame:
        raise ValueError(f"Missing target column {TARGET!r}")
    # Drop both target columns and the prepared row ID before any fit or scoring.
    predictors = [column for column in frame.columns if column not in EXCLUDED]
    if expected_columns is not None and predictors != expected_columns:
        raise ValueError("Training and testing predictor columns differ or changed order.")
    X = frame.loc[:, predictors].copy()
    y = pd.to_numeric(frame[TARGET], errors="raise")
    if y.isna().any() or not set(y.unique()) <= {0, 1}:
        raise ValueError("Target must contain only binary 0/1 labels.")
    y = y.astype("int8")

    # Numeric parsing is deterministic; learned scaling and one-hot
    # category discovery happen inside each training-only sklearn Pipeline.
    numeric_columns = [column for column in predictors if column not in CATEGORICAL]
    for column in numeric_columns:
        X[column] = pd.to_numeric(X[column], errors="coerce")
    # The verified files have no missing values. Stop for a new audit if that
    # changes; we do not claim to have imputed data that was already complete.
    if not np.isfinite(X[numeric_columns].to_numpy(dtype=float)).all():
        raise ValueError("Missing, invalid, or infinite numeric values; inspect the audit before modeling.")
    if any(X[column].str.strip().eq("").any() for column in CATEGORICAL):
        raise ValueError("Empty categorical values; inspect the audit before modeling.")
    return X, y


def make_preprocessor(numeric: list[str], categorical: list[str], *, scale: bool, dense: bool) -> ColumnTransformer:
    """Fit encoders/scalers inside the pipeline using training rows only."""
    # Keep '-' as a service category. No imputer is needed for these complete
    # files. Trees receive original numeric values; Logistic Regression scales.
    category_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=not dense, dtype=np.float32)
    numeric_transformer = StandardScaler() if scale else "passthrough"
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, numeric),
            ("categorical", category_encoder, categorical),
        ],
        remainder="drop",
        sparse_threshold=0.3 if not dense else 0.0,
    )


def model_pipelines(numeric: list[str], categorical: list[str]) -> dict[str, tuple[object, dict[str, object]]]:
    """Declare a fixed, teachable comparison before the official test is used."""
    lr = Pipeline(
        steps=[
            ("preprocess", make_preprocessor(numeric, categorical, scale=True, dense=False)),
            (
                "classifier",
                LogisticRegression(
                    C=1.0,
                    solver="lbfgs",
                    max_iter=500,
                    class_weight="balanced",
                    random_state=SEED,
                ),
            ),
        ]
    )
    rf = Pipeline(
        steps=[
            ("preprocess", make_preprocessor(numeric, categorical, scale=False, dense=False)),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=150,
                    max_depth=20,
                    min_samples_leaf=2,
                    max_features="sqrt",
                    class_weight="balanced_subsample",
                    n_jobs=-1,
                    random_state=SEED,
                ),
            ),
        ]
    )
    hist = Pipeline(
        steps=[
            ("preprocess", make_preprocessor(numeric, categorical, scale=False, dense=True)),
            (
                "classifier",
                HistGradientBoostingClassifier(
                    learning_rate=0.1,
                    max_iter=100,
                    max_leaf_nodes=31,
                    min_samples_leaf=20,
                    l2_regularization=0.1,
                    class_weight="balanced",
                    early_stopping=False,
                    random_state=SEED,
                ),
            ),
        ]
    )
    return {
        "dummy_prior": (DummyClassifier(strategy="prior"), {"strategy": "training class prior"}),
        "logistic_regression": (
            lr,
            {"C": 1.0, "solver": "lbfgs", "max_iter": 500, "class_weight": "balanced", "random_state": SEED},
        ),
        "random_forest": (
            rf,
            {
                "n_estimators": 150,
                "max_depth": 20,
                "min_samples_leaf": 2,
                "max_features": "sqrt",
                "class_weight": "balanced_subsample",
                "random_state": SEED,
                "n_jobs": -1,
            },
        ),
        "hist_gradient_boosting": (
            hist,
            {
                "learning_rate": 0.1,
                "max_iter": 100,
                "max_leaf_nodes": 31,
                "min_samples_leaf": 20,
                "l2_regularization": 0.1,
                "class_weight": "balanced",
                "early_stopping": False,
                "random_state": SEED,
            },
        ),
    }


def measure(y_true: pd.Series | np.ndarray, y_pred: np.ndarray, attack_scores: np.ndarray) -> dict[str, object]:
    """Return fixed-label metrics, keeping attack class (1) explicit."""
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=[0, 1], zero_division=0
    )
    return {
        "rows": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "attack_precision": float(precision[1]),
        "attack_recall": float(recall[1]),
        "attack_f1": float(f1[1]),
        "normal_precision": float(precision[0]),
        "normal_recall": float(recall[0]),
        "normal_f1": float(f1[0]),
        "roc_auc": float(roc_auc_score(y_true, attack_scores)) if len(np.unique(y_true)) == 2 else None,
        "confusion_matrix_labels_0_then_1": confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist(),
    }


def prediction_scores(model: object, X: pd.DataFrame, y_train: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    """Return predicted classes and attack probabilities for metric calculation."""
    predicted = model.predict(X)
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X)[:, 1]
    else:
        probabilities = np.full(len(X), float(y_train.mean()))
    return predicted, probabilities


def metric_rows(results: dict[str, object]) -> list[dict[str, object]]:
    """Flatten nested results to a small CSV that is easy to reuse in a report."""
    rows: list[dict[str, object]] = []
    for model_name, item in results.items():
        for split_name, metrics in item["metrics"].items():
            rows.append({"model": model_name, "split": split_name, **metrics})
    return rows


def render_metrics_markdown(results: dict[str, object], metadata: dict[str, object]) -> str:
    lines = [
        "# UNSW-NB15 Binary Classification: Model Comparison",
        "",
        f"Run time: {metadata['run_timestamp_local']} ({metadata['runtime']['python']}, pandas {metadata['runtime']['pandas']}, scikit-learn {metadata['runtime']['scikit_learn']}, Matplotlib {metadata['runtime']['matplotlib']}).",
        "",
        "This is a benchmark comparison using the official prepared train/test files. It does not establish production IDS performance.",
        "",
        "## Method and leakage controls",
        "",
        "- Source: [official UNSW-NB15 research page](https://research.unsw.edu.au/projects/unsw-nb15-dataset); use the prepared 175,341-row training file and 82,332-row test file. Raw data remains under `data/raw/`.",
        "- Target: `label` (1 = attack, 0 = normal). `id` and `attack_cat` are excluded from predictors.",
        "- `attack_cat` was excluded because the audit showed a deterministic mapping from each category to the binary target.",
        "- Predictors are the 42 remaining flow fields. `proto`, `service`, and `state` are one-hot encoded; `service = '-'` stays a category.",
        "- The audit found complete data. Missing, invalid, or infinite numeric values and empty categorical values stop the model run for inspection. No missing values are imputed.",
        "- Logistic Regression standardizes numeric fields; the trees use their original numeric values. `proto`, `service`, and `state` use one-hot encoding with unseen categories ignored. `service = '-'` stays a regular category. These transformers fit only on each training partition; no resampling is used.",
        "- Validation groups are hashed from predictor values, so identical vectors stay on one side of the fit/validation boundary.",
        "- Model settings were fixed before evaluating the official test file. Every model is first checked on the grouped validation fold, then fit on the full official training split and evaluated on the official test split.",
        "- The secondary `test_unseen_predictor_vectors` score is limited to official-test rows whose 42 predictors were absent from all official training rows.",
        "- Validation uses one approximately 80/20 grouped holdout from a five-fold splitter, not an average over five fitted folds. No hyperparameter search or tuning was performed.",
        "- Predictions use precomputed flow features, including totals/statistics. This study classifies prepared flow records; it has not tested early detection while a flow is still arriving.",
        "",
        "## Model families",
        "",
        "| Model | Role | Fixed settings |",
        "|---|---|---|",
    ]
    for model_name, item in results.items():
        settings = ", ".join(f"{k}={v}" for k, v in item["settings"].items())
        lines.append(f"| {MODEL_NAMES[model_name]} | {item['role']} | {settings} |")
    lines.extend([
        "", "## Why these fixed settings?", "",
        "Logistic Regression is the simple learned reference. C=1 is a starting regularization setting, and 500 iterations allow the solver time to converge. Numeric scaling is useful because flow fields have different units and ranges.", "",
        "Random Forest uses 150 trees for a manageable comparison. A depth limit of 20 and at least two samples per leaf constrain very specific branches. Random feature subsets make its trees diverse. These are chosen starter settings rather than optimized values.", "",
        "Boosting uses 100 iterations at learning rate 0.1. The leaf and minimum-sample limits constrain individual trees; L2=0.1 provides modest regularization. Early stopping is explicitly disabled so the grouped holdout remains the validation boundary and all 100 iterations are used.", "",
        "Class weights balance the total influence of the two training classes. They do not create or delete rows. All learned classifiers use seed 42. The Dummy baseline provides a reference with no learned relationship between flow features and labels.", "",
        "Random Forest and boosting are each ensembles of trees. The three learned classifiers are compared separately; there is no voting or stacking model that combines them.",
    ])
    for split_name, title in [
        ("validation", "Grouped validation results"),
        ("test_official", "Official test results"),
        ("test_unseen_predictor_vectors", "Secondary test results on unseen predictor vectors"),
    ]:
        lines.extend(
            [
                "",
                f"## {title}",
                "",
                "| Model | Rows | Accuracy | Balanced accuracy | Macro-F1 | Attack precision | Attack recall | Attack F1 | ROC-AUC |",
                "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
            ]
        )
        if split_name == "test_official":
            lines[len(lines) - 2:len(lines) - 2] = ["![Macro-F1 and attack recall comparison](unsw_nb15_model_comparison.png)", ""]
        for model_name, item in results.items():
            metrics = item["metrics"].get(split_name)
            if metrics is None:
                continue
            lines.append(
                f"| {MODEL_NAMES[model_name]} | {metrics['rows']:,} | {metrics['accuracy']:.4f} | {metrics['balanced_accuracy']:.4f} | {metrics['macro_f1']:.4f} | {metrics['attack_precision']:.4f} | {metrics['attack_recall']:.4f} | {metrics['attack_f1']:.4f} | {metrics['roc_auc']:.4f} |"
            )
    lines.extend(
        [
            "",
            "## Confusion matrices",
            "",
            "![Official test confusion matrices](unsw_nb15_confusion_matrices.png)",
            "",
            "Rows are actual labels [0, 1]; columns are predicted labels [0, 1].",
        ]
    )
    for model_name, item in results.items():
        matrix = item["metrics"]["test_official"]["confusion_matrix_labels_0_then_1"]
        lines.extend(
            [
                "",
                f"### {MODEL_NAMES[model_name]}",
                "",
                f"| | Predicted normal (0) | Predicted attack (1) |",
                "|---|---:|---:|",
                f"| Actual normal (0) | {matrix[0][0]:,} | {matrix[0][1]:,} |",
                f"| Actual attack (1) | {matrix[1][0]:,} | {matrix[1][1]:,} |",
            ]
        )
    lines.extend(
        [
            "",
            "## Reading the results",
            "",
            "Use macro-F1 to summarize both classes evenly and attack recall to show how many attack flows were found. Accuracy alone can hide a weak result for one class. The training and test attack proportions differ, so compare per-class results and avoid attributing a metric gap to the model alone.",
            "",
            "The official test split contains repeated predictor vectors, including some whose label differs from the label attached to that same vector in training. The secondary unseen-vector score is a subset of the same official test file. It describes unfamiliar input combinations, not unseen attack types or an independent new dataset. Exact-vector grouping does not establish separation by capture day, host, or session.",
            "",
            "## Reproducibility record",
            "",
            f"- Random seed: {metadata['seed']}; validation method: {metadata['validation']['method']}.",
            f"- Fit rows: {metadata['validation']['fit_rows']:,}; validation rows: {metadata['validation']['validation_rows']:,}; predictor groups shared across fit/validation: {metadata['validation']['group_overlap_count']}.",
            f"- Official-test rows: {metadata['test_rows']:,}; rows with a predictor vector previously seen in training: {metadata['test_seen_predictor_rows']:,}; unseen rows: {metadata['test_unseen_predictor_rows']:,}.",
            "- The JSON companion records input hashes, processing steps, software versions, group split counts, model settings, fit times, and all reported metrics.",
            "",
            "## Processing log",
            "",
        ]
    )
    # Explain errors as counts as well as scores, so the security trade-off is
    # visible even to a reader who is still learning precision and recall.
    forest = results["random_forest"]["metrics"]["test_official"]
    boosting = results["hist_gradient_boosting"]["metrics"]["test_official"]
    rf_cm = forest["confusion_matrix_labels_0_then_1"]
    gb_cm = boosting["confusion_matrix_labels_0_then_1"]
    interpretation = [
        "", "### False alarms and missed attacks", "",
        "The Dummy baseline predicts every row as an attack because attacks are the majority in training. Its attack recall is 1.0, but it incorrectly flags every normal flow. Recall alone therefore cannot select a useful model.", "",
        f"Random Forest misses {rf_cm[1][0]:,} attacks and flags {rf_cm[0][1]:,} normal flows. Boosting misses {gb_cm[1][0]:,} attacks and flags {gb_cm[0][1]:,} normal flows. In this test set, Random Forest finds {gb_cm[1][0] - rf_cm[1][0]:,} additional attacks while producing {rf_cm[0][1] - gb_cm[0][1]:,} additional false alarms.", "",
        f"Boosting has the highest official-test macro-F1 ({boosting['macro_f1']:.4f}) and accuracy ({boosting['accuracy']:.2%}), while Random Forest has higher attack recall ({forest['attack_recall']:.2%}). Boosting still flags {gb_cm[0][1] / sum(gb_cm[0]):.2%} of normal test flows as attacks; Random Forest flags {rf_cm[0][1] / sum(rf_cm[0]):.2%}. A working network system would need to consider that false-alarm burden.", "",
        "These are descriptive comparisons of fixed models on this benchmark. One holdout does not supply a cross-validation mean, spread, or a statistical significance claim. The selected parameter values should not be called the best possible settings.",
    ]
    insert_at = lines.index("## Reproducibility record") - 1
    lines[insert_at:insert_at] = interpretation
    lines.extend(f"- {step}" for step in metadata["processing_log"])
    lines.append("")
    return "\n".join(lines)


def run_analysis() -> dict[str, object]:
    """Execute one grouped validation pass and one official-test evaluation."""
    train_raw, train_source = load_source_split("training")
    test_raw, test_source = load_source_split("testing")
    X_train, y_train = prepare_features(train_raw)
    X_test, y_test = prepare_features(test_raw, list(X_train.columns))
    numeric_columns = [column for column in X_train.columns if column not in CATEGORICAL]

    # Group on the model's parsed predictor values (not IDs or labels), so rows
    # that become the same X after numeric parsing cannot cross the fold.
    train_groups = pd.util.hash_pandas_object(X_train, index=False, categorize=True).to_numpy(dtype="uint64")
    test_groups = pd.util.hash_pandas_object(X_test, index=False, categorize=True).to_numpy(dtype="uint64")
    splitter = StratifiedGroupKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    fit_indices, validation_indices = next(splitter.split(X_train, y_train, groups=train_groups))
    fit_group_set = set(train_groups[fit_indices].tolist())
    validation_group_set = set(train_groups[validation_indices].tolist())
    group_overlap = len(fit_group_set & validation_group_set)
    if group_overlap:
        raise ValueError(f"Feature groups crossed the fit/validation boundary: {group_overlap}")
    X_fit, y_fit = X_train.iloc[fit_indices], y_train.iloc[fit_indices]
    X_validation, y_validation = X_train.iloc[validation_indices], y_train.iloc[validation_indices]
    models = model_pipelines(numeric_columns, CATEGORICAL)
    results: dict[str, object] = {}
    fit_notes: dict[str, object] = {}
    test_seen = np.isin(test_groups, train_groups)
    test_unseen = ~test_seen

    # The validation fold is diagnostic for the predefined model comparison;
    # no parameter changes will be made after seeing official-test metrics.
    for model_name, (estimator, settings) in models.items():
        role = {
            "dummy_prior": "prior-only reference",
            "logistic_regression": "linear reference classifier",
            "random_forest": "bagging ensemble",
            "hist_gradient_boosting": "boosting ensemble",
        }[model_name]
        started = time.perf_counter()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            estimator.fit(X_fit, y_fit)
        validation_seconds = time.perf_counter() - started
        val_prediction, val_score = prediction_scores(estimator, X_validation, y_fit)
        val_metrics = measure(y_validation, val_prediction, val_score)

        # Refit the same fixed configuration on the full official training
        # file; only then touch official test predictors for final scoring.
        final_estimator, _ = model_pipelines(numeric_columns, CATEGORICAL)[model_name]
        started = time.perf_counter()
        with warnings.catch_warnings(record=True) as final_caught:
            warnings.simplefilter("always")
            final_estimator.fit(X_train, y_train)
        final_fit_seconds = time.perf_counter() - started
        test_prediction, test_score = prediction_scores(final_estimator, X_test, y_train)
        test_metrics = measure(y_test, test_prediction, test_score)
        unseen_metrics = measure(y_test[test_unseen], test_prediction[test_unseen], test_score[test_unseen])
        results[model_name] = {
            "role": role,
            "settings": settings,
            "classifier_parameters": (final_estimator.named_steps["classifier"] if isinstance(final_estimator, Pipeline) else final_estimator).get_params(deep=False),
            "metrics": {
                "validation": val_metrics,
                "test_official": test_metrics,
                "test_unseen_predictor_vectors": unseen_metrics,
            },
        }
        fit_notes[model_name] = {
            "validation_fit_seconds": round(validation_seconds, 3),
            "full_training_fit_seconds": round(final_fit_seconds, 3),
            "validation_warnings": [str(item.message) for item in caught],
            "final_fit_warnings": [str(item.message) for item in final_caught],
        }

    group_class_counts = {
        split_name: {str(label): int(count) for label, count in y_part.value_counts().sort_index().items()}
        for split_name, y_part in (("fit", y_fit), ("validation", y_validation))
    }
    metadata = {
        "run_timestamp_local": datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat(timespec="seconds"),
        "runtime": {
            "python": platform.python_version(),
            "pandas": pd.__version__,
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
            "scikit_learn": sklearn.__version__,
            "scipy": version("scipy"),
            "joblib": version("joblib"),
            "threadpoolctl": version("threadpoolctl"),
        },
        "seed": SEED,
        "inputs": {"training": train_source, "testing": test_source},
        "feature_count": int(X_train.shape[1]),
        "categorical_features": CATEGORICAL,
        "numeric_features": numeric_columns,
        "excluded_predictor_columns": sorted(EXCLUDED),
        "preprocessing": {
            "missing_values": "No imputation; stop on missing/invalid/infinite numeric or empty categorical fields",
            "numeric_scaling": "StandardScaler for Logistic Regression only",
            "categorical_encoding": "OneHotEncoder(handle_unknown='ignore', dtype=float32)",
            "output_format": "dense for histogram boosting; sparse permitted for Logistic Regression and Random Forest",
            "resampling": "none",
            "fitting_boundary": "current training partition only",
        },
        "model_selection": "Predefined fixed configurations; no hyperparameter search",
        "validation": {
            "method": "first fold from StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42), groups=hash of parsed 42 predictor values",
            "fit_rows": int(len(fit_indices)),
            "validation_rows": int(len(validation_indices)),
            "fit_class_counts": group_class_counts["fit"],
            "validation_class_counts": group_class_counts["validation"],
            "unique_fit_groups": len(fit_group_set),
            "unique_validation_groups": len(validation_group_set),
            "group_overlap_count": group_overlap,
        },
        "test_rows": int(len(y_test)),
        "test_seen_predictor_rows": int(test_seen.sum()),
        "test_unseen_predictor_rows": int(test_unseen.sum()),
        "processing_log": [
            "1. Re-verified staged training/testing file sizes, SHA-256 digests, and row counts before modeling.",
            "2. Read source CSVs as strings with NA coercion disabled; did not alter or rewrite raw files.",
            "3. Constructed y from label and X from the 42 flow predictors only; removed id and attack_cat before preprocessing.",
            "4. Parsed the 39 numeric predictors with numeric coercion and an explicit invalid-value check; retained proto, service, and state as categories, including service '-'.",
            "5. Hashed parsed X vectors only to create feature groups; group hashes were never input to any estimator.",
            "6. Selected the first fixed-seed StratifiedGroupKFold split; verified zero feature groups crossed fit/validation.",
            "7. Verified complete/finite numeric and nonempty categorical fields; applied no imputation. Inside training-only pipelines, standardized numeric fields for Logistic Regression and one-hot encoded categories with unknown-category ignore; fit the predefined Dummy, Logistic Regression, Random Forest, and histogram boosting models, with no resampling or hyperparameter tuning.",
            "8. Recorded validation metrics, then refit each unchanged model configuration on all official training rows and evaluated the official test rows.",
            "9. Calculated a secondary metric set only on test rows whose predictor vectors were absent from the full training split.",
            "10. Generated result JSON, Markdown, Matplotlib PNG charts, and a tidy CSV using derived outputs only.",
        ],
        "fit_notes": fit_notes,
    }
    return {"metadata": metadata, "models": results}


def main() -> None:
    # Bundle mode avoids direct Python writes in the restricted OneDrive
    # workspace; scripts/run_models.ps1 saves these derived strings.
    output = run_analysis()
    csv_text = pd.DataFrame(metric_rows(output["models"])).to_csv(index=False)
    bundle = {
        "json_text": json.dumps(output, indent=2, sort_keys=True, ensure_ascii=False),
        "markdown_text": render_metrics_markdown(output["models"], output["metadata"]),
        "csv_text": csv_text,
    }
    if "--emit-bundle" in sys.argv:
        print(json.dumps(bundle, ensure_ascii=False))
        return
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "unsw_nb15_model_results.json").write_text(bundle["json_text"] + "\n", encoding="utf-8")
    (REPORTS / "unsw_nb15_model_results.md").write_text(bundle["markdown_text"], encoding="utf-8")
    (REPORTS / "unsw_nb15_model_metrics.csv").write_text(bundle["csv_text"], encoding="utf-8")
    # Ordinary Python users also get the figures referenced by the report.
    # Use the PowerShell runner for dated snapshots and automatic action logs.
    import base64
    from plot_unsw_nb15_results import make_metric_comparison, make_confusion_matrices
    (REPORTS / "unsw_nb15_model_comparison.png").write_bytes(base64.b64decode(make_metric_comparison(output["models"])))
    (REPORTS / "unsw_nb15_confusion_matrices.png").write_bytes(base64.b64decode(make_confusion_matrices(output["models"])))


if __name__ == "__main__":
    main()
