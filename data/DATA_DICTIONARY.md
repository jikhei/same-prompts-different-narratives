# Data dictionary

## Keys and common fields

| Field | Definition |
|---|---|
| `story_id` | Stable story identifier. Primary key in final story, metric, and final-score tables. |
| `prompt_id` | Identifier shared by stories written from the same prompt. |
| `model` | Story source: Human, GPT-2, GPT-2 (tag), Qwen2.5-7B, Falcon3-7B, or gemma-2. |
| `run_id` | Zero-based generation run within a model and prompt. Together with `model` and `prompt_id`, identifies a candidate. |
| `prompt` | Writing prompt supplied to the human author or language model. |
| `story` | Cleaned story text used for validation and analysis. |
| `response` | Raw decoded model response retained in the candidate dataset. |
| `word_count` | Number of tokens matching the regular expression `\w+`. |
| `wc_human` | Word count of the human story for the same prompt. |
| `wc_diff` | Absolute difference between `word_count` and `wc_human`. |
| `valid` | Candidate is within 100 words of the paired human story and contains no generation error marker. |
| `selected` | First valid run for a model and prompt; selected candidates form the generated portion of the final dataset. |

## Human scores

All raw human scores use a 1–5 scale. The detailed scoring protocol is cited in the repository README and is not reproduced here.

| Field | Dimension | Aggregation in `final_scores.csv` |
|---|---|---|
| `RE` | Relevance | HANNA: mean of three source ratings; new stories: mean of Rater A and Rater B. |
| `CH` | Coherence | Same aggregation. |
| `EM` | Empathy | Same aggregation. |
| `SU` | Surprise | Same aggregation. |
| `EG` | Engagement | Same aggregation. |
| `CX` | Complexity | Same aggregation. |

`ratings_anonymized.csv` has primary key (`story_id`, `rater_id`) and contains only the 123 newly generated stories. Text comments and adjudication discussions are excluded.

`hanna_mean_scores.csv` contains one row per selected HANNA story and is the published source for the 105 legacy-story rows in `final_scores.csv`. `score_source` records whether a final row is the HANNA three-rating mean or the mean of the two anonymous raters for the newly generated stories.

## Automatic metrics

| Field | Definition |
|---|---|
| `SMOG` | SMOG readability index. |
| `ARI` | Automated Readability Index. |
| `LFP` | Proportion of lexical tokens with English Zipf frequency at or below 3.0. |
| `MDD` | Mean dependency distance across sentences. |
| `SRP` | Mean sentence-level surprisal using `EleutherAI/pythia-6.9b-deduped` at revision `step3000`. |
| `SPD` | Mean distance between successive semantic word vectors. |
| `SCC` | Observed semantic path length relative to a nearest-neighbor path. |
| `SVL` | Semantic volume derived from the minimum-volume enclosing ellipsoid. |
| `EPD` | Mean distance between successive sentence-level VADER sentiment values. |
| `ECC` | Observed emotional path length relative to a nearest-neighbor path. |
| `EVL` | Sum of the absolute sentence-level VADER sentiment values. |

The standardized tables contain z-scores used by the statistical models. Their `label` field is 1 for Human and 0 for language-model stories.
