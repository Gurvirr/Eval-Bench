---
name: feature-validity
description: Before including a feature in a model, verify it would be available at prediction time. Post-event features cause target leakage.
---

# Feature Validity Check

A feature is valid only if it would be known at the moment the prediction is made.

## Common leaking patterns
- **Post-event flags**: chargeback_filed, dispute_raised, return_initiated (happen after the outcome)
- **Outcome-derived aggregates**: claims_in_30_days_after, support_tickets_after_cancel
- **Future data**: next_week_price, promotion_next_period

## Check
For each feature, ask: "Would I know this value when I need to make the prediction?"
If no, exclude it from the feature set.
