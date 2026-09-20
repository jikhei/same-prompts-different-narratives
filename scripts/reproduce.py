#!/usr/bin/env python3
"""Create compact descriptive tables from the released analysis data."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs"


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    stories = pd.read_csv(ROOT / "data/processed/stories.csv")
    metrics = pd.read_csv(ROOT / "data/metrics/metrics_raw.csv")
    scores = pd.read_csv(ROOT / "data/ratings/final_scores.csv")

    story_summary = (
        stories.groupby("model")[["word_count", "wc_diff"]]
        .agg(["count", "min", "max", "mean", "median"])
        .round(3)
    )
    metric_summary = metrics.groupby("model").agg(["mean", "std"]).round(4)
    score_summary = (
        scores.groupby("model")[["RE", "CH", "EM", "SU", "EG", "CX"]]
        .agg(["mean", "std"])
        .round(4)
    )
    score_metric_correlation = (
        scores.merge(metrics, on=["story_id", "prompt_id", "model"], validate="one_to_one")
        .select_dtypes("number")
        .drop(columns=["story_id", "prompt_id"])
        .corr(method="spearman")
        .round(4)
    )

    story_summary.to_csv(OUTPUT / "story_descriptives.csv")
    metric_summary.to_csv(OUTPUT / "metric_descriptives.csv")
    score_summary.to_csv(OUTPUT / "score_descriptives.csv")
    score_metric_correlation.to_csv(OUTPUT / "score_metric_correlations.csv")
    print(f"Wrote reproducibility tables to {OUTPUT}")


if __name__ == "__main__":
    main()
