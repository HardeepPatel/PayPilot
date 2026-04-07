# prepare.py 
# Fixed constants, one-time data prep, and runtime utilities (evaluation). Not modified.

ZONES = [
    "top_action_bar",
    "top_first_row",
    "second_row",
    "secondary_drawer",
    "settings_menu",
    "top_right_card"
]

def run_evaluation(placements):
    """
    Mock Evaluation function:
    Scores the array of features and their assigned zones based on priority.
    """
    passed_guard = True
    
    zone_values = {
        "top_action_bar": 10,
        "top_first_row": 8,
        "top_right_card": 7,
        "second_row": 6,
        "secondary_drawer": 2,
        "settings_menu": 0
    }

    speed = 0
    priority_alignment = 0
    safety_compliance = 100
    clutter_penalty = 0
    regression_penalty = 0

    p0_count = sum(1 for p in placements if p["priority"] == "P0")
    max_p0_speed = p0_count * 10
    
    for item in placements:
        priority = item["priority"]
        zone = item["zone"]
        val = zone_values.get(zone, 0)
        
        if priority == "P0":
            speed += val
            priority_alignment += val
            # Guardrail: Never hide P0 features (they must be in top_action_bar or top_first_row)
            if zone not in ["top_action_bar", "top_first_row"]:
                passed_guard = False
                safety_compliance -= 30
        
        elif priority == "P1":
            speed += val * 0.8
            if zone in ["top_first_row", "top_right_card", "second_row"]:
                priority_alignment += 10
            else:
                priority_alignment -= 5
                
        elif priority == "P2" or priority == "P3":
            if zone in ["top_action_bar", "top_first_row"]:
                # High clutter penalty if rare stuff is at the top
                clutter_penalty += 15
            else:
                priority_alignment += 5

    norm_speed = min(100, max(0, (speed / max(1, max_p0_speed * 1.5)) * 100))
    norm_alignment = min(100, max(0, priority_alignment * 2))
    norm_discoverability = 100 - clutter_penalty
    norm_safety = max(0, safety_compliance)
    success = 100 if passed_guard else 40

    final_score = (
        0.30 * success +
        0.25 * norm_speed +
        0.20 * norm_alignment +
        0.15 * norm_discoverability +
        0.10 * norm_safety - 
        0.10 * clutter_penalty - 
        0.10 * regression_penalty
    )

    return final_score, passed_guard, success, norm_speed, norm_alignment, norm_discoverability, norm_safety, clutter_penalty
