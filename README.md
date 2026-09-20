# Same prompts, different narratives

Data, code, and supporting results for *Same prompts, different narratives: Evaluating readability and interestingness in human-authored and LM-generated stories*.

## Repository contents

- `data/raw/generated_candidates.csv`: all 369 generated candidates before length-based selection.
- `data/external/hanna_subset.csv`: the 105 HANNA stories used in the study.
- `data/external/hanna_mean_scores.csv`: the published HANNA mean ratings used in this study.
- `data/processed/stories.csv`: the final 228-story analysis dataset.
- `data/processed/candidate_selection.csv`: candidate validity and selection decisions.
- `data/ratings/ratings_anonymized.csv`: final numerical ratings from `Rater A` and `Rater B` for the 123 newly generated stories.
- `data/ratings/final_scores.csv`: six aggregated human scores for all 228 stories.
- `data/metrics/metrics_raw.csv`: the 11 automatic metrics used in the paper.
- `data/metrics/*_standardized.csv`: standardized inputs used by the statistical models.
- `notebooks/`: cleaned story-generation, metric-computation, and analysis notebooks.
- `scripts/mixed_effects.R`: mixed-effects model code.
- `figures/`: the eight principal SVG figures from the study.

Definitions, units, primary keys, and transformations are documented in [`data/DATA_DICTIONARY.md`](data/DATA_DICTIONARY.md).

## Data provenance

The HANNA source data come from Chhun, Suchanek, and Clavel's public benchmark. The analysis is pinned to commit [`282f27536a5d05ad4ce14298abcd70c45668fed2`](https://github.com/dig-team/hanna-benchmark-asg/tree/282f27536a5d05ad4ce14298abcd70c45668fed2), rather than the moving `main` branch. The complete raw HANNA annotations remain available at the pinned source; this repository contains only the selected stories and aggregated scores required by this study.

The six human rating dimensions follow the protocol in:

> Chhun, C., Colombo, P., Suchanek, F. M., & Clavel, C. (2022). *Of Human Criteria and Automatic Metrics: A Benchmark of the Evaluation of Story Generation*. Proceedings of COLING 2022, 5794–5836. [ACL Anthology](https://aclanthology.org/2022.coling-1.509/).

The scoring rubric itself is not redistributed here.

## Environment and reproduction materials

The released CSV files are the authoritative inputs for inspecting and rebuilding the downstream analysis tables. Dependency versions and the original compute context are recorded in [`ENVIRONMENT.md`](ENVIRONMENT.md).

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
make verify
make reproduce
```

`make reproduce` creates descriptive tables in `outputs/`; it does not execute the notebooks. `make analysis` is an optional convenience target for environments that can run the cleaned analysis notebook. The scripts `prepare_data.py` and `prepare_scores.py` rebuild the candidate-selection and score-aggregation tables from the published inputs.

The original story generation and the GPU-dependent Pythia 6.9B metric calculation were run in a Google Colab GPU runtime. The notebooks document those procedures, and `requirements.txt` defines the Python dependencies, but this archive does not claim that every notebook is portable or runnable out of the box on arbitrary hardware. The released `metrics_raw.csv` lets reviewers inspect the exact metric values used without downloading model weights.

The original generation run used three runs per prompt, `temperature=0.7`, `top_p=0.9`, and `max_new_tokens=800`. Exact model commit hashes and random seeds were not recorded during that run, so the released 369-candidate snapshot—not a claim of bit-for-bit regeneration—is the raw source for downstream reproduction.

## Privacy

The anonymous labels `Rater A` and `Rater B` are stable only within this release.

## License and third-party material

Original material in this repository is released under CC BY 4.0. Third-party data, model weights, and cited methods retain their original terms; see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
