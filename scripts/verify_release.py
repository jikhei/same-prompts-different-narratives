#!/usr/bin/env python3
"""Verify public-release schemas, counts, anonymity, and prohibited formats."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COUNTS = {
    "data/raw/generated_candidates.csv": 369,
    "data/external/hanna_subset.csv": 105,
    "data/external/hanna_mean_scores.csv": 105,
    "data/processed/stories.csv": 228,
    "data/processed/candidate_selection.csv": 369,
    "data/metrics/metrics_raw.csv": 228,
    "data/metrics/metrics_standardized.csv": 228,
    "data/metrics/scores_standardized.csv": 228,
    "data/ratings/ratings_anonymized.csv": 246,
    "data/ratings/final_scores.csv": 228,
}
TEXT_SUFFIXES = {".csv", ".json", ".md", ".py", ".ipynb", ".txt", ".R", ".yml", ".yaml", ".toml"}
PROHIBITED_SUFFIXES = {".xlsx", ".xls", ".pkl", ".pptx", ".pdf", ".DS_Store"}
PROHIBITED_PATTERNS = {
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "local macOS user path": re.compile("/" + r"Users/[^/\s]+"),
    "local Linux user path": re.compile("/" + r"home/[^/\s]+"),
    "personal Colab drive path": re.compile("/content/drive/" + "MyDrive"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    "OpenAI key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "Hugging Face token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b"),
    "internal feedback path": re.compile("feedback" + "-0301", re.IGNORECASE),
    "conversation instruction marker": re.compile(
        r"(?:recommended_plugins|environment_context|collaboration_mode|"
        r"request_user_input|desired oververbosity|you are codex)",
        re.IGNORECASE,
    ),
}
FORBIDDEN_NOTEBOOK_METADATA_KEYS = {
    "author",
    "creator",
    "displayname",
    "email",
    "executioninfo",
    "lastmodifiedby",
    "owner",
    "user",
    "userid",
    "username",
}


def read_rows(relative_path: str) -> list[dict[str, str]]:
    with (ROOT / relative_path).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def notebook_identity_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key != "display_name":
                normalized = key.lower().replace("_", "")
                if normalized in FORBIDDEN_NOTEBOOK_METADATA_KEYS:
                    keys.add(key)
            keys.update(notebook_identity_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(notebook_identity_keys(child))
    return keys


def main() -> int:
    failures: list[str] = []
    for relative_path, expected in EXPECTED_COUNTS.items():
        path = ROOT / relative_path
        if not path.is_file():
            fail(f"missing: {relative_path}", failures)
            continue
        actual = len(read_rows(relative_path))
        if actual != expected:
            fail(f"{relative_path}: expected {expected} rows, found {actual}", failures)

    stories = read_rows("data/processed/stories.csv")
    story_ids = [row["story_id"] for row in stories]
    if len(story_ids) != len(set(story_ids)):
        fail("stories.csv has duplicate story_id values", failures)

    expected_models = {
        "Human": 41,
        "GPT-2": 32,
        "GPT-2 (tag)": 32,
        "Qwen2.5-7B": 41,
        "Falcon3-7B": 41,
        "gemma-2": 41,
    }
    actual_models = {name: 0 for name in expected_models}
    for row in stories:
        actual_models[row["model"]] = actual_models.get(row["model"], 0) + 1
    if actual_models != expected_models:
        fail(f"unexpected model counts: {actual_models}", failures)

    ratings = read_rows("data/ratings/ratings_anonymized.csv")
    if {row["rater_id"] for row in ratings} != {"Rater A", "Rater B"}:
        fail("ratings contain unexpected rater identifiers", failures)
    for row in ratings:
        for field in ["Relevance", "Coherence", "Empathy", "Surprise", "Engagement", "Complexity"]:
            value = float(row[field])
            if not 1 <= value <= 5:
                fail(f"rating outside 1-5: {field}={value}", failures)

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix in PROHIBITED_SUFFIXES or path.name == ".DS_Store":
            fail(f"prohibited file type: {path.relative_to(ROOT)}", failures)
        if path.resolve() == Path(__file__).resolve():
            continue
        if path.suffix in TEXT_SUFFIXES or path.name in {"LICENSE", "Makefile"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for label, pattern in PROHIBITED_PATTERNS.items():
                if pattern.search(text):
                    fail(f"{label} found in {path.relative_to(ROOT)}", failures)

    for path in (ROOT / "notebooks").glob("*.ipynb"):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        identity_keys = notebook_identity_keys(notebook)
        if identity_keys:
            fail(
                f"identity metadata {sorted(identity_keys)} found in {path.relative_to(ROOT)}",
                failures,
            )

    figures = list((ROOT / "figures").glob("*.svg"))
    if len(figures) != 8:
        fail(f"expected 8 SVG figures, found {len(figures)}", failures)

    manifest = json.loads((ROOT / "release-manifest.json").read_text())
    if manifest.get("dataset_counts", {}).get("stories") != 228:
        fail("release manifest has an unexpected story count", failures)
    for relative_path, expected_hash in manifest.get("sha256", {}).items():
        path = ROOT / relative_path
        if not path.is_file():
            fail(f"checksum target missing: {relative_path}", failures)
        elif sha256(path) != expected_hash:
            fail(f"checksum mismatch: {relative_path}", failures)

    if failures:
        print("Release verification failed:")
        for message in failures:
            print(f"- {message}")
        return 1
    print("Release verification passed: schemas, counts, anonymity, and file types are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
