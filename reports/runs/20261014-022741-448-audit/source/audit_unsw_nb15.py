#!/usr/bin/env python3
"""Reproducible, read-only audit of the staged UNSW-NB15 prepared CSV splits."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
import sys
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
REPORTS = ROOT / "reports"
FILES = {
    "training": {
        "name": "UNSW_NB15_training-set.csv",
        "bytes": 32_293_018,
        "sha256": "BEC7DD5EC88DC2A0CCC7A07879D338395ED7421750F675FD0339E07DFE0648FA",
        "rows": 175_341,
    },
    "testing": {
        "name": "UNSW_NB15_testing-set.csv",
        "bytes": 15_380_800,
        "sha256": "734FE6642EDF758F7C94D7D9149426B49D202FE8E7BF0BEF47392489C3C0A559",
        "rows": 82_332,
    },
}
CATEGORICAL = {"proto", "service", "state"}
TARGET = "label"
TARGET_DERIVED = {"attack_cat", TARGET}
IDENTIFIERS = {"id"}
EXCLUDED_FROM_FEATURES = TARGET_DERIVED | IDENTIFIERS
BLANK_LIKE = {"na", "n/a", "null", "none", "nan"}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def read_raw_csv(path: Path) -> pd.DataFrame:
    # Keep strings and empty fields intact so this audit reports source values
    # without silently converting blanks or sentinel text into missing values.
    return pd.read_csv(path, dtype=str, keep_default_na=False, na_filter=False, low_memory=False)


def profile_split(key: str, spec: dict[str, object], frame: pd.DataFrame) -> dict[str, object]:
    # Profile source strings as read. Trimming is used only to flag blanks and
    # is never written back into the source CSV or feature values.
    cols: dict[str, object] = {}
    for column in frame.columns:
        series = frame[column]
        stripped = series.str.strip()
        entry: dict[str, object] = {
            "dtype_as_read": "string",
            "empty_count": int(series.eq("").sum()),
            "whitespace_only_count": int((series.ne("") & stripped.eq("")).sum()),
            "blank_like_token_count": int(stripped.str.casefold().isin(BLANK_LIKE).sum()),
            "distinct_count": int(series.nunique(dropna=False)),
            "top_values": [
                {"value": str(value), "count": int(count)}
                for value, count in series.value_counts(dropna=False).head(5).items()
            ],
        }
        # Numeric conversion is diagnostic only; modeling will preprocess its
        # own fit partition inside a separate leakage-safe pipeline.
        if column not in CATEGORICAL and column not in TARGET_DERIVED:
            numeric = pd.to_numeric(series, errors="coerce")
            invalid = series.ne("") & numeric.isna()
            values = numeric.dropna().to_numpy(dtype=np.float64)
            finite = values[np.isfinite(values)]
            if finite.size:
                quantiles = np.quantile(finite, [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
                entry["numeric"] = {
                    "min": float(np.min(finite)),
                    "max": float(np.max(finite)),
                    "mean": float(np.mean(finite)),
                    "std": float(np.std(finite, ddof=1)) if finite.size > 1 else 0.0,
                    "p01": float(quantiles[0]),
                    "p05": float(quantiles[1]),
                    "p25": float(quantiles[2]),
                    "median": float(quantiles[3]),
                    "p75": float(quantiles[4]),
                    "p95": float(quantiles[5]),
                    "p99": float(quantiles[6]),
                    "zero_count": int(np.count_nonzero(finite == 0)),
                    "negative_count": int(np.count_nonzero(finite < 0)),
                    "infinite_count": int(np.count_nonzero(~np.isfinite(values))),
                    "invalid_nonblank_count": int(invalid.sum()),
                }
        cols[column] = entry

    # Keep target and target-derived category checks separate from predictors.
    label_counts: dict[str, int] = {}
    if TARGET in frame:
        label_counts = {str(k): int(v) for k, v in frame[TARGET].value_counts(dropna=False).items()}
    attack_label_counts: dict[str, dict[str, int]] = {}
    attack_mapping: dict[str, list[str]] = {}
    if "attack_cat" in frame and TARGET in frame:
        attacks = frame["attack_cat"].str.strip().replace("", "<EMPTY>")
        cross = pd.crosstab(attacks, frame[TARGET], dropna=False)
        attack_label_counts = {
            str(category): {str(label): int(count) for label, count in row.items() if count}
            for category, row in cross.iterrows()
        }
        attack_mapping = {
            str(category): sorted(str(x) for x in frame.loc[attacks.eq(category), TARGET].unique())
            for category in attacks.unique()
        }

    # The prepared `id` field is diagnostic only and is excluded from X later.
    id_stats: dict[str, object] = {}
    if "id" in frame and TARGET in frame:
        ids = pd.to_numeric(frame["id"], errors="coerce")
        labels = pd.to_numeric(frame[TARGET], errors="coerce")
        valid = ids.notna() & labels.notna()
        if valid.any():
            corr = np.corrcoef(ids[valid].to_numpy(dtype=float), labels[valid].to_numpy(dtype=float))[0, 1]
            bins = pd.qcut(ids[valid], q=10, duplicates="drop")
            rates = labels[valid].groupby(bins, observed=False).mean()
            id_stats = {
                "unique_count": int(ids.nunique(dropna=True)),
                "row_count": int(len(ids)),
                "min": float(ids.min()),
                "max": float(ids.max()),
                "pearson_correlation_with_label": float(corr) if np.isfinite(corr) else None,
                "attack_rate_by_id_quantile": [float(x) for x in rates.tolist()],
            }

    digest = file_sha256(RAW / str(spec["name"]))
    actual_bytes = (RAW / str(spec["name"])).stat().st_size
    result = {
        "file": spec["name"],
        "actual_bytes": int(actual_bytes),
        "expected_bytes": spec["bytes"],
        "size_matches_expected": actual_bytes == spec["bytes"],
        "sha256": digest,
        "expected_sha256": spec["sha256"],
        "hash_matches_expected": digest == spec["sha256"],
        "rows": int(len(frame)),
        "expected_rows": spec["rows"],
        "row_count_matches_expected": len(frame) == spec["rows"],
        "columns": int(frame.shape[1]),
        "column_names": list(frame.columns),
        "duplicate_column_names": sorted(frame.columns[frame.columns.duplicated()].unique().tolist()),
        "empty_header_names": int(sum(not str(c).strip() for c in frame.columns)),
        "blank_cell_count": int(frame.eq("").to_numpy().sum()),
        "literal_blank_like_token_count": int(
            frame.apply(lambda s: s.str.strip().str.casefold().isin(BLANK_LIKE)).to_numpy().sum()
        ),
        "duplicate_full_rows": int(frame.duplicated().sum()),
        "duplicate_rows_excluding_id": int(frame.drop(columns=[c for c in IDENTIFIERS if c in frame]).duplicated().sum()),
        "label_counts": label_counts,
        "attack_label_counts": attack_label_counts,
        "attack_to_label_values": attack_mapping,
        "id_diagnostics": id_stats,
        "column_profile": cols,
    }
    return result


def hash_rows(frame: pd.DataFrame) -> pd.Series:
    # Efficient candidate-match screen only; these hashes never enter a model.
    return pd.util.hash_pandas_object(frame, index=False, categorize=True).astype("uint64")


def audit() -> dict[str, object]:
    # Read as strings and disable pandas' NA coercion so empty cells and
    # literal sentinel-looking values remain distinguishable in the audit.
    frames: dict[str, pd.DataFrame] = {}
    splits: dict[str, dict[str, object]] = {}
    for key, spec in FILES.items():
        path = RAW / str(spec["name"])
        if not path.exists():
            raise FileNotFoundError(f"Expected prepared CSV is missing: {path}")
        frames[key] = read_raw_csv(path)
        splits[key] = profile_split(key, spec, frames[key])

    train, test = frames["training"], frames["testing"]
    # Use the same ordered columns for split comparisons, then form X only from
    # measured candidate predictors, explicitly omitting id and target fields.
    shared_columns = sorted(set(train.columns) & set(test.columns))
    same_schema = list(train.columns) == list(test.columns)
    feature_columns = [c for c in train.columns if c not in EXCLUDED_FROM_FEATURES]
    # Compare complete source rows and predictor-only rows as separate screens.
    # Within each split, count repeated predictor vectors and cases where one
    # vector is associated with more than one target value.
    for split_name, frame in frames.items():
        predictor_hashes = hash_rows(frame[feature_columns])
        predictor_labels = pd.DataFrame({"feature_hash": predictor_hashes, "label": frame[TARGET]})
        label_groups = predictor_labels.groupby("feature_hash")["label"].nunique()
        conflicting_groups = label_groups[label_groups > 1]
        group_sizes = predictor_hashes.value_counts()
        repeated_hashes = group_sizes[group_sizes > 1]
        splits[split_name]["predictor_duplicate_screen"] = {
            "rows_with_repeated_predictor_vector": int(predictor_hashes.duplicated(keep=False).sum()),
            "excess_rows_after_first_predictor_vector": int(predictor_hashes.duplicated().sum()),
            "distinct_repeated_predictor_vectors": int(len(repeated_hashes)),
            "predictor_vectors_with_multiple_labels": int(len(conflicting_groups)),
            "rows_in_predictor_vectors_with_multiple_labels": int(group_sizes.reindex(conflicting_groups.index).sum()),
        }
    feature_sets = {
        name: hash_rows(frame[feature_columns])
        for name, frame in (("training", train), ("testing", test))
    }
    full_sets = {
        name: hash_rows(frame[shared_columns])
        for name, frame in (("training", train), ("testing", test))
    }
    train_full_unique = set(full_sets["training"].tolist())
    train_features_unique = set(feature_sets["training"].tolist())
    test_full_hits = full_sets["testing"].isin(train_full_unique)
    test_feature_hits = feature_sets["testing"].isin(train_features_unique)
    train_feature_labels = pd.DataFrame(
        {"feature_hash": feature_sets["training"], "label": train[TARGET]}
    ).groupby("feature_hash")["label"].agg(lambda x: set(x.astype(str)))
    conflicting = 0
    for feature_hash, label in zip(feature_sets["testing"], test[TARGET]):
        train_labels = train_feature_labels.get(feature_hash, set())
        if train_labels and str(label) not in train_labels:
            conflicting += 1
    train_ids = pd.to_numeric(train["id"], errors="coerce") if "id" in train else pd.Series(dtype=float)
    test_ids = pd.to_numeric(test["id"], errors="coerce") if "id" in test else pd.Series(dtype=float)

    # If attack_cat maps deterministically to label, it exposes the target and
    # must stay out of X even when its blank/category values differ by split.
    labels_valid = all(set(frame[TARGET].unique()) <= {"0", "1"} for frame in frames.values())
    attack_mapping_deterministic = all(
        len(labels) == 1
        for split in splits.values()
        for labels in split["attack_to_label_values"].values()
    )
    category_label_conflicts = {
        key: {k: v for k, v in value["attack_to_label_values"].items() if len(v) > 1}
        for key, value in splits.items()
    }
    result: dict[str, object] = {
        "audit_version": 1,
        "audit_timestamp_local": datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat(timespec="seconds"),
        "runtime": {"python": platform.python_version(), "pandas": pd.__version__, "numpy": np.__version__},
        "processing_log": [
            "1. Read-only source audit: opened the prepared CSVs under data/raw; source bytes were not changed.",
            "2. Integrity: computed SHA-256 in 1 MiB chunks and compared digest, byte size, and row count to the acquisition record.",
            "3. Parsing: read as strings with keep_default_na=False and na_filter=False to preserve empty cells and literal text.",
            "4. Profiling: counted empty/whitespace/blank-like cells, distinct and frequent values, and numeric ranges/quantiles; numeric coercion was temporary and diagnostic only.",
            "5. Target audit: counted label values and cross-tabulated attack_cat against label; label is y and attack_cat is excluded as target-derived.",
            "6. Split screen: omitted id, label, and attack_cat from candidate predictors; hashed full rows and predictor-only rows to screen overlap.",
            "7. Reporting: generated derived JSON and Markdown outputs; this audit did not train a model.",
        ],
        "source_and_scope": {
            "source_as_recorded": "Official UNSW shared OneDrive folder: CSV Files/Training and Testing Sets",
            "raw_files_modified": False,
            "raw_packet_captures_in_scope": False,
            "feature_grain": "one prepared dataset row, intended to represent one network flow record",
            "target": TARGET,
            "positive_class": "1 = attack",
            "planned_exclusions_from_predictors": sorted(EXCLUDED_FROM_FEATURES),
            "categorical_predictors_expected": sorted(CATEGORICAL & set(feature_columns)),
            "feature_predictors": feature_columns,
        },
        "schema": {
            "same_train_test_column_order": same_schema,
            "same_train_test_columns": set(train.columns) == set(test.columns),
            "train_only_columns": sorted(set(train.columns) - set(test.columns)),
            "test_only_columns": sorted(set(test.columns) - set(train.columns)),
            "column_count": len(train.columns),
            "predictor_count_after_exclusions": len(feature_columns),
            "predictor_columns": feature_columns,
            "numeric_candidate_predictors": [c for c in feature_columns if c not in CATEGORICAL],
            "categorical_predictors": [c for c in feature_columns if c in CATEGORICAL],
        },
        "cross_split_checks": {
            "full_row_matches_in_test": int(test_full_hits.sum()),
            "distinct_full_row_hashes_shared": len(train_full_unique & set(full_sets["testing"].tolist())),
            "feature_matches_in_test_ignoring_id_target_and_attack_cat": int(test_feature_hits.sum()),
            "distinct_feature_hashes_shared": len(train_features_unique & set(feature_sets["testing"].tolist())),
            "test_rows_with_same_predictors_but_conflicting_label_in_training": int(conflicting),
            "id_values_shared_between_splits": int(len(set(train_ids.dropna()) & set(test_ids.dropna()))),
            "hash_method": "pandas hash_pandas_object over source string fields; interpreted as a duplicate-screening check",
        },
        "duplicate_aware_validation": {
            "validation_partition": "split official training rows by groups formed from the 42 predictor values; keep each repeated predictor vector on one side only",
            "class_balance": "use fixed-seed group-aware stratification if available and report resulting class counts because repeated groups constrain exact stratification",
            "official_test": "keep the official test split untouched for final evaluation after model selection",
            "secondary_test_slice": "report a secondary result for test rows whose predictor-vector hash was not observed in the full official training split",
        },
        "integrity_and_scope_checks": {
            "all_sizes_match_expected": all(x["size_matches_expected"] for x in splits.values()),
            "all_hashes_match_expected": all(x["hash_matches_expected"] for x in splits.values()),
            "all_row_counts_match_expected": all(x["row_count_matches_expected"] for x in splits.values()),
            "same_train_test_schema": same_schema,
            "label_values_only_0_or_1": labels_valid,
            "attack_category_mapping_is_deterministic_across_splits": attack_mapping_deterministic,
            "attack_category_label_conflicts_by_split": category_label_conflicts,
        },
        "splits": splits,
    }
    return result


def render_markdown(result: dict[str, object]) -> str:
    integrity = result["integrity_and_scope_checks"]
    schema = result["schema"]
    checks = result["cross_split_checks"]
    lines = [
        "# UNSW-NB15 Prepared CSV Data Audit",
        "",
        f"Generated {result['audit_timestamp_local']} with Python {result['runtime']['python']}, pandas {result['runtime']['pandas']}, and NumPy {result['runtime']['numpy']}.",
        "The audit reads the prepared CSVs without editing them; processing steps are recorded below and in the JSON companion.",
        "",
        "## Scope and target",
        "",
        "- Source as recorded in the project log: official UNSW shared OneDrive folder, `CSV Files/Training and Testing Sets`.",
        "- Grain: one prepared row per network-flow record, as described by the source dataset documentation.",
        "- Target: `label`; positive class `1` means attack.",
        "- Predictor exclusions: `label` (target), `attack_cat` (direct target-derived category), and `id` (row identifier).",
        f"- Predictor count after exclusions: {schema['predictor_count_after_exclusions']} ({len(schema['categorical_predictors'])} categorical and {len(schema['numeric_candidate_predictors'])} numeric candidates).",
        "- Raw PCAP files and the incomplete archive are out of scope.",
        "",
        "## File integrity and dimensions",
        "",
        "| Split | Rows | Columns | Bytes | SHA-256 | Matches recorded value |",
        "|---|---:|---:|---:|---|---|",
    ]
    for key, split in result["splits"].items():
        lines.append(
            f"| {key} | {split['rows']:,} | {split['columns']} | {split['actual_bytes']:,} | `{split['sha256']}` | {split['hash_matches_expected']} |"
        )
    lines.extend(
        [
            "",
            f"- Train/test columns and order match: {schema['same_train_test_column_order']}.",
            f"- All expected byte sizes, SHA-256 hashes, and row counts match: {integrity['all_sizes_match_expected'] and integrity['all_hashes_match_expected'] and integrity['all_row_counts_match_expected']}.",
            "",
            "## Target and split checks",
            "",
            f"- Labels are only 0/1 in both files: {integrity['label_values_only_0_or_1']}.",
            f"- Exact full-row matches from training found in test: {checks['full_row_matches_in_test']:,}.",
            f"- Test rows with the same predictors as training after excluding `id`, `label`, and `attack_cat`: {checks['feature_matches_in_test_ignoring_id_target_and_attack_cat']:,}.",
            f"- Among those matched predictor rows, test rows whose label conflicts with the training label: {checks['test_rows_with_same_predictors_but_conflicting_label_in_training']:,}.",
            "- These overlap counts are screening diagnostics; repeated flow feature vectors are not automatically proof of invalid partitioning.",
            f"- `attack_cat` maps deterministically to `label` in both splits: {integrity['attack_category_mapping_is_deterministic_across_splits']}; this is why it is excluded as a direct target-derived field.",
            "",
            "### Class distribution",
            "",
            "| Split | Label | Rows | Share |",
            "|---|---:|---:|---:|",
        ]
    )
    for key, split in result["splits"].items():
        for label, count in split["label_counts"].items():
            share = 100 * count / split["rows"] if split["rows"] else 0
            lines.append(f"| {key} | {label} | {count:,} | {share:.2f}% |")
    lines.extend(
        [
            "",
            "### Attack category-to-label diagnostic",
            "",
            "| Split | `attack_cat` value | Label counts |",
            "|---|---|---|",
        ]
    )
    for key, split in result["splits"].items():
        for category, counts in split["attack_label_counts"].items():
            rendered = ", ".join(f"{label}: {count:,}" for label, count in counts.items())
            lines.append(f"| {key} | {category} | {rendered} |")
    lines.extend(
        [
            "",
            "## Missing and duplicate screening",
            "",
            "| Split | Empty cells | Blank-like literal tokens | Duplicate complete rows | Duplicate rows excluding `id` | Rows with repeated predictors | Predictor groups with conflicting labels | Rows in conflicting groups |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for key, split in result["splits"].items():
        lines.append(
            f"| {key} | {split['blank_cell_count']:,} | {split['literal_blank_like_token_count']:,} | {split['duplicate_full_rows']:,} | {split['duplicate_rows_excluding_id']:,} | {split['predictor_duplicate_screen']['rows_with_repeated_predictor_vector']:,} | {split['predictor_duplicate_screen']['predictor_vectors_with_multiple_labels']:,} | {split['predictor_duplicate_screen']['rows_in_predictor_vectors_with_multiple_labels']:,} |"
        )
    lines.extend(["", "### Per-column profile", "", "| Column | Distinct | Empty | Blank-like token | Top values (count) |", "|---|---:|---:|---:|---|"])
    for key, split in result["splits"].items():
        lines.extend(["", f"#### {key.title()}", ""])
        for column, entry in split["column_profile"].items():
            top = ", ".join(f"`{x['value']}` ({x['count']:,})" for x in entry["top_values"])
            lines.append(
                f"| `{column}` | {entry['distinct_count']:,} | {entry['empty_count']:,} | {entry['blank_like_token_count']:,} | {top} |"
            )
    train_id = result["splits"]["training"]["id_diagnostics"]
    test_id = result["splits"]["testing"]["id_diagnostics"]
    lines.extend(["", "## Processing record", ""])
    lines.extend(f"- {step}" for step in result["processing_log"])
    lines.extend(
        [
            "",
            "## Leakage guardrails and evaluation plan",
            "",
            "1. Set `y = label`, with attack as the positive class.",
            "2. Exclude `attack_cat` because it encodes the attack family and reveals the binary target; exclude `id` because it is an identifier, not a network measurement.",
            "3. Keep the official test file untouched while selecting models. Create a fixed-seed group-aware fit/validation split from official training using the 42-predictor vector as the group; repeated vectors must not cross fit and validation. Approximate stratification and report actual class counts.",
            "4. Put categorical encoding and numeric imputation/scaling inside each model pipeline so they are fitted only on that model's training partition. Do not resample or fit preprocessing on validation or test rows.",
            "5. Fix model choices and settings using training/validation only, refit selected pipelines on full official training, then evaluate the official test file once. Also report a clearly labeled secondary score on test rows whose predictor vector is unseen in training.",
            "6. Report attack-class precision/recall/F1, macro-F1, confusion matrix, and accuracy with class counts; restrict conclusions to this benchmark split.",
            "",
            "### Identifier diagnostics (excluded from predictors)",
            "",
            f"- Training `id`: {train_id.get('unique_count')} unique for {train_id.get('row_count')} rows; range {train_id.get('min')} to {train_id.get('max')}; Pearson correlation with `label` {train_id.get('pearson_correlation_with_label')}.",
            f"- Testing `id`: {test_id.get('unique_count')} unique for {test_id.get('row_count')} rows; range {test_id.get('min')} to {test_id.get('max')}; Pearson correlation with `label` {test_id.get('pearson_correlation_with_label')}.",
            f"- Numeric IDs shared by both files: {checks['id_values_shared_between_splits']:,}. The ID ranges reset and label association differs between splits, so `id` is excluded from predictors.",
            "- Identifier correlations are diagnostic only and are not a reason to use the identifier as a feature.",
            "",
            "## Caveats",
            "",
            "- Hash equality was used as a scalable screening method for cross-split duplicate checks; hash matches should be treated as candidate duplicate rows.",
            "- `attack_cat` is omitted from the model feature matrix regardless of whether its raw strings are blank for benign rows.",
            "- This audit does not establish real-world network generalization, and no model performance is included here.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    # stdout bundle mode is used with PowerShell redirection on this desktop
    # because the restricted Python process cannot create OneDrive files.
    result = audit()
    if "--emit-bundle" in sys.argv:
        bundle = {
            "json_text": json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False),
            "markdown_text": render_markdown(result),
        }
        print(json.dumps(bundle, ensure_ascii=False))
        return

    REPORTS.mkdir(parents=True, exist_ok=True)
    json_path = REPORTS / "unsw_nb15_audit.json"
    md_path = REPORTS / "unsw_nb15_data_audit.md"
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(result), encoding="utf-8")
    print(f"Wrote {md_path}")
    print(f"Wrote {json_path}")
    print(json.dumps(result["integrity_and_scope_checks"], indent=2, sort_keys=True))
    print(json.dumps(result["cross_split_checks"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
