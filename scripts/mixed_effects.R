library(tidyverse)
library(lme4)

library(Matrix)
packageVersion("Matrix") 

scores_data <- read.csv('data/metrics/scores_standardized.csv') |>
    mutate(
        label = factor(label),
        model = factor(model),
        prompt_id = factor(prompt_id)
    )
metrics_data <- read.csv('data/metrics/metrics_standardized.csv') |>
    mutate(
        label = factor(label),
        model = factor(model),
        prompt_id = factor(prompt_id)
    )

scores_model <- glm(formula = label ~ 0 + RE + CH + EM + SU + EG + CX, data = scores_data, family = 'binomial')

scores_model <- glmer(formula = label ~ 0 + RE + CH + EM + SU + EG + CX + (1|model) + (1|prompt_id), data = scores_data, family = 'binomial')

summary(scores_model)

metrics_model <- glm(formula = label ~ 0 + SMOG + ARI + LFP + MDD + SRP + SPD + SCC +SVL + EPD + ECC + EVL, data = metrics_data, family = 'binomial')

metrics_model <- glmer(formula = label ~ 0 + SMOG + ARI + LFP + MDD + SRP + SPD + SCC +SVL + EPD + ECC + EVL + (1|prompt_id) + (1|model), data = metrics_data, family = 'binomial')

summary(metrics_model)
