# Computation environment

## Python

The Python packages used by the released scripts and notebooks are pinned in `requirements.txt`. The release was prepared and checked with Python 3.12. Package pins document the intended software environment; they are not a guarantee that every notebook will run unchanged on every operating system or hardware configuration.

The metric notebook additionally expects the spaCy `en_core_web_lg` pipeline and the NLTK VADER lexicon. After installing the pinned packages, these resources can be installed with `python -m spacy download en_core_web_lg` and `python -m nltk.downloader vader_lexicon`. Model weights referenced by the generation and metric notebooks are fetched from their respective Hugging Face repositories and are not redistributed here.

## GPU work

The original story-generation runs and the Pythia 6.9B surprisal calculation were performed in a Google Colab GPU runtime. The exact Colab GPU model was not recorded. The cleaned notebooks preserve the model identifiers and generation or metric settings used in the study, while avoiding personal Google Drive paths.

Exact model revision hashes and random seeds were not recorded during the original generation run. For that reason, `data/raw/generated_candidates.csv` is the authoritative raw generation snapshot and `data/metrics/metrics_raw.csv` is the authoritative metric snapshot used in the paper. Neither bit-for-bit regeneration nor out-of-the-box execution on non-Colab hardware is claimed.

The downstream CSV preparation and descriptive summaries do not require a GPU.

## R

The mixed-effects analysis script uses `tidyverse`, `lme4`, `lmerTest`, `effectsize`, `performance`, and `report`. Notebook metadata records R 4.5.3, tidyverse 2.0.0, and Matrix 1.7-5. The complete original R package lockfile was not retained, so remaining package versions are not asserted.
