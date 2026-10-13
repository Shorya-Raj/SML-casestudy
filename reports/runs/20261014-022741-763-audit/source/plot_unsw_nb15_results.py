"""Render report figures from saved model metrics without fitting models again.

The figure inputs are the derived JSON result file; this script never opens or
changes either raw CSV. Bundle mode returns encoded PNGs so the PowerShell
runner can save them in a workspace where Python file writes are restricted.
"""

from __future__ import annotations

import base64
import argparse
import io
import json
from pathlib import Path

import matplotlib

# Select a non-interactive backend so the script also works on headless systems.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = PROJECT_ROOT / "reports" / "unsw_nb15_model_results.json"
MODEL_ORDER = [
    "dummy_prior",
    "logistic_regression",
    "random_forest",
    "hist_gradient_boosting",
]
MODEL_NAMES = {
    "dummy_prior": "Dummy baseline",
    "logistic_regression": "Logistic Regression",
    "random_forest": "Random Forest",
    "hist_gradient_boosting": "Histogram Gradient\nBoosting",
}


def png_base64(figure: plt.Figure) -> str:
    """Encode a finished figure in memory for the PowerShell file writer."""
    buffer = io.BytesIO()
    figure.savefig(buffer, format="png", dpi=180, bbox_inches="tight")
    plt.close(figure)
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def make_metric_comparison(results: dict[str, object]) -> str:
    """Compare macro-F1 and attack recall on the official test split."""
    names = [name for name in MODEL_ORDER if name in results]
    positions = np.arange(len(names))
    bar_width = 0.36
    macro_f1 = [results[name]["metrics"]["test_official"]["macro_f1"] for name in names]
    attack_recall = [results[name]["metrics"]["test_official"]["attack_recall"] for name in names]

    # Plot separate series side by side so the baseline's high recall and poor
    # balance across classes are both visible.
    fig, ax = plt.subplots(figsize=(10, 5.2), layout="constrained")
    macro_bars = ax.bar(positions - bar_width / 2, macro_f1, bar_width, label="Macro-F1", color="#3569A8")
    recall_bars = ax.bar(positions + bar_width / 2, attack_recall, bar_width, label="Attack recall", color="#E07A2D")
    ax.bar_label(macro_bars, fmt="%.3f", padding=3, fontsize=9)
    ax.bar_label(recall_bars, fmt="%.3f", padding=3, fontsize=9)
    ax.set_title("UNSW-NB15 official test: model comparison")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.12)
    ax.set_yticks(np.arange(0, 1.01, 0.2))
    ax.set_xticks(positions, [MODEL_NAMES[name] for name in names])
    ax.grid(axis="y", color="#d9dee7", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncols=2, loc="upper center")
    return png_base64(fig)


def parse_matrix(rows: list[list[int]]) -> np.ndarray:
    """Convert the saved two-row count list into a numeric 2x2 matrix."""
    return np.asarray([[int(value) for value in row] for row in rows], dtype=int)


def make_confusion_matrices(results: dict[str, object]) -> str:
    """Draw four comparable actual-versus-predicted count matrices."""
    names = [name for name in MODEL_ORDER if name in results]
    matrices = {
        name: parse_matrix(results[name]["metrics"]["test_official"]["confusion_matrix_labels_0_then_1"])
        for name in names
    }
    common_max = max(int(matrix.max()) for matrix in matrices.values())

    # Use one shared color scale to make the cell shading comparable across
    # models. Each panel prints exact counts so color is not the only cue.
    # Two rows keep panel labels readable at a normal report page width.
    fig, axes = plt.subplots(2, 2, figsize=(8, 7.5), layout="constrained")
    axes = np.asarray(axes).ravel()
    image = None
    for ax, name in zip(axes, names):
        matrix = matrices[name]
        image = ax.imshow(matrix, cmap="Blues", vmin=0, vmax=common_max)
        ax.set_title(MODEL_NAMES[name].replace("\n", " "), fontsize=11)
        ax.set_xticks([0, 1], ["Normal (0)", "Attack (1)"])
        ax.set_yticks([0, 1], ["Normal (0)", "Attack (1)"])
        ax.set_xlabel("Predicted class")
        ax.set_ylabel("Actual class")
        for row in range(2):
            for column in range(2):
                value = int(matrix[row, column])
                text_color = "white" if value > common_max * 0.45 else "#172033"
                ax.text(column, row, f"{value:,}", ha="center", va="center", color=text_color, fontsize=12)

    fig.suptitle("Official test confusion matrices (shared count scale)")
    if image is not None:
        fig.colorbar(image, ax=axes.tolist(), shrink=0.82, label="Number of flows")
    return png_base64(fig)


def main() -> None:
    """Read saved metrics and emit figures for the report runner."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=RESULTS_PATH)
    parser.add_argument("--emit-bundle", action="store_true")
    args = parser.parse_args()
    with args.results.open("r", encoding="utf-8") as result_file:
        saved = json.load(result_file)

    # The code intentionally reads model metrics only; raw data and fitted
    # estimators are not needed to make these figures.
    results = saved["models"]
    bundle = {
        "metric_comparison_png_base64": make_metric_comparison(results),
        "confusion_matrices_png_base64": make_confusion_matrices(results),
    }
    if args.emit_bundle:
        print(json.dumps(bundle))
        return

    # On an ordinary Python setup, save beside the selected result JSON.
    directory = args.results.parent
    (directory / "unsw_nb15_model_comparison.png").write_bytes(base64.b64decode(bundle["metric_comparison_png_base64"]))
    (directory / "unsw_nb15_confusion_matrices.png").write_bytes(base64.b64decode(bundle["confusion_matrices_png_base64"]))


if __name__ == "__main__":
    main()
