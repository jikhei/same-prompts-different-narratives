#!/usr/bin/env python3
"""Rebuild the aggregated score table from the released ratings."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RATING_COLUMNS = [
    "Relevance",
    "Coherence",
    "Empathy",
    "Surprise",
    "Engagement",
    "Complexity",
]
SHORT_COLUMNS = ["RE", "CH", "EM", "SU", "EG", "CX"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs" / "rebuilt")
    args = parser.parse_args()

    ratings = pd.read_csv(ROOT / "data/ratings/ratings_anonymized.csv")
    stories = pd.read_csv(ROOT / "data/processed/stories.csv")
    hanna_scores = pd.read_csv(ROOT / "data/external/hanna_mean_scores.csv")
    new_scores = (
        ratings.groupby("story_id", as_index=False)[RATING_COLUMNS]
        .mean()
        .round(1)
        .rename(columns=dict(zip(RATING_COLUMNS, SHORT_COLUMNS)))
    )
    final_scores = pd.concat([hanna_scores, new_scores], ignore_index=True).merge(
        stories[["story_id", "prompt_id", "model"]],
        on="story_id",
        validate="one_to_one",
    )
    final_scores["score_source"] = np.where(
        final_scores["story_id"] < 1100,
        "HANNA mean of three ratings",
        "Mean of Rater A and Rater B",
    )
    final_scores = final_scores[
        ["story_id", "prompt_id", "model"] + SHORT_COLUMNS + ["score_source"]
    ].sort_values("story_id", ignore_index=True)
    if len(final_scores) != 228:
        raise ValueError("score aggregation did not produce the expected 228 stories")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    final_scores.to_csv(args.output_dir / "final_scores.csv", index=False)
    print(f"Wrote aggregated scores to {args.output_dir}")


if __name__ == "__main__":
    main()
