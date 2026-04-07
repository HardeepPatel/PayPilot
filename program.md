# Agent Instructions

You are optimizing a payment dashboard layout. Your goal is to maximize `final_score` and ensure `guard_passed` is True.

This dashboard displays dynamic features for Payment Ops. You modify `train.py` by changing the `zone` assignments in the `placements` list to improve the score. 

## Target Function
The `final_score` represents usability, derived from: `0.30*success + 0.25*speed + 0.20*alignment + 0.15*discoverability + 0.10*safety - clutter - regression`.

## Rules
1. **Critical Guardrail**: P0 items (Refund queue, Failed payments, Payout status) MUST be in `"top_action_bar"` or `"top_first_row"`. Breaking this results in `guard_passed: False` and a massive safety penalty.
2. P1 items (Merchant health, Settlement summary) should be highly visible (e.g. `"second_row"` or `"top_right_card"`).
3. P2/P3 items (Exports, Admin) should be tucked away to reduce clutter (e.g. `"secondary_drawer"` or `"settings_menu"`).

## Valid ZONES
You may ONLY use these zones:
"top_action_bar", "top_first_row", "second_row", "secondary_drawer", "settings_menu", "top_right_card"

## Your Execution Loop
1. Read `train.py`.
2. Propose a new valid layout by altering `zone` definitions in the file.
3. Run `python train.py` and read the `final_score`.
4. If it improves, keep the new file. If not, revert.
