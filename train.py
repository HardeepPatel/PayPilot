# train.py
# The single file the agent edits. Contains the layout spec logic mapping features to zones.

from prepare import run_evaluation

# Layout Spec
placements = [
    {"feature": "Refund queue", "priority": "P0", "zone": "secondary_drawer"},
    {"feature": "Failed payments", "priority": "P0", "zone": "settings_menu"},
    {"feature": "Payout status", "priority": "P0", "zone": "second_row"},
    {"feature": "Merchant health", "priority": "P1", "zone": "top_right_card"},
    {"feature": "Settlement summary", "priority": "P1", "zone": "secondary_drawer"},
    {"feature": "Exports", "priority": "P2", "zone": "top_action_bar"}
]

if __name__ == "__main__":
    score, passed_guard, succ, spd, align, disc, safe, clut = run_evaluation(placements)
    
    # Strictly output to stdout so launch.py can parse it
    print(f"final_score: {score:.4f}")
    print(f"guard_passed: {passed_guard}")
    print(f"success: {succ:.4f}, speed: {spd:.4f}, alignment: {align:.4f}")
    print(f"safety: {safe:.4f}, clutter: {clut:.4f}, discoverability: {disc:.4f}")
