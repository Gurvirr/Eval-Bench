# Dropped Tasks

These 7 tasks were piloted and then cut from the final benchmark. Each had oracle=1 and nop=0, but gemini-3.5-flash passed them too reliably to be useful as difficulty signal against this model.

## Why they were cut

### simpsons-paradox (pass@1 mean: 0.95)
The model correctly stratifies by subgroup in 95% of trials. The task requires joining two CSVs and running a groupby — operations the model handles well. We added dirty severity labels and a third subgroup to make it harder but the model normalized and grouped correctly. The failure mode (not stratifying) is documented in CausalPitfalls but gemini-3.5-flash doesn't fall for it on this specific setup.

### join-fanout (pass@1 mean: 0.96)
The model correctly avoids M:N join row inflation. It reads the instructions, identifies that customer_ids can have multiple tags, and filters by customer ID before summing rather than joining first. The fanout trap is a known pitfall in SQL but the model is trained on enough pandas best practices to avoid it.

### macro-vs-micro-f1 (pass@1 mean: 0.97)
The model correctly identifies macro F1 as the right metric for imbalanced multiclass problems and computes it accurately. We tried removing the hint about which metric to use and reformulating the task as a judgment call, but the model still chose macro F1 correctly. The model's training data includes extensive discussion of metric choice for imbalanced problems.

### class-imbalance-accuracy (pass@1 mean: 0.90)
The model correctly identifies that 97% accuracy on a 97/3 class split is misleading, computes recall on the fraud class, and sets recommend_deployment=false. The failure mode is well-documented in ML education materials and the model applies it correctly.

### multiple-comparisons (pass@1 mean: 0.89)
The model applies Bonferroni correction across 50 tests and identifies the correct 2 significant results. We split the data into 50 individual CSV files to make it harder to see all tests at once, but the model discovered and loaded all 50 files, computed p-values, and applied the correction. The model knows statistical best practices.

### timeseries-cv-leakage (pass@1 mean: 1.00)
When told to use "5-fold cross-validation," the model correctly uses TimeSeriesSplit instead of KFold for temporal data. The model recognized the temporal structure and chose the appropriate sklearn class. This is different from our passing timeseries-lookahead task, where the model fails silently by using rolling() without shift(1) — in that task the model doesn't know it's doing something wrong.

### cohort-retention (pass@1 mean: 0.89)
The model correctly parses comma-separated active_months, computes per-month retention rates, and handles cohort boundary dates correctly. The task requires straightforward CSV parsing and groupby operations that the model handles reliably.

## The pattern

All 7 cut tasks share the same characteristic: the correct answer requires applying a documented, well-known methodology that is extensively covered in the model's training data. The model has been trained on pandas documentation, sklearn guides, statistics textbooks, and data science blog posts — all of which cover these techniques explicitly.

The 7 retained tasks either exploit a gap in the model's reasoning (information validity at prediction time) or require reading domain-specific documents that the model cannot have memorized.
