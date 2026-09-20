#!/usr/bin/env python3
"""Rebuild candidate-selection decisions from the released raw candidates."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs" / "rebuilt")
    args = parser.parse_args()

    candidates = pd.read_csv(ROOT / "data/raw/generated_candidates.csv")
    hanna = pd.read_csv(ROOT / "data/external/hanna_subset.csv")
    human_words = (
        hanna[hanna["model"] == "Human"]
        .set_index("prompt_id")["word_count"]
        .to_dict()
    )

    selection = candidates.copy()
    selection["word_count"] = selection["story"].map(
        lambda text: len(re.findall(r"\w+", str(text)))
    )
    selection["wc_human"] = selection["prompt_id"].map(human_words)
    selection["wc_diff"] = (selection["word_count"] - selection["wc_human"]).abs()
    selection["valid"] = (selection["wc_diff"] <= 100) & ~selection[
        "story"
    ].str.contains("[ERR]", regex=False, na=False)
    selection["selected"] = False
    first_valid = (
        selection[selection["valid"]]
        .groupby(["model", "prompt_id"], sort=False)
        .head(1)
        .index
    )
    selection.loc[first_valid, "selected"] = True
    if int(selection["selected"].sum()) != 123:
        raise ValueError("selection did not produce the expected 123 generated stories")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    selection.to_csv(args.output_dir / "candidate_selection.csv", index=False)
    print(f"Wrote {len(selection)} candidate decisions to {args.output_dir}")


if __name__ == "__main__":
    main()
