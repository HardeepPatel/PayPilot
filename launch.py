# launch.py
# The supervisor process. It simulates pointing the LLM to program.md and having it edit train.py.

import os
import subprocess
import copy
import random
import csv
import re
from prepare import ZONES

RESULT_FILE = "result.csv"
TRAIN_FILE = "train.py"
MAX_ROUNDS = 100

def parse_score(output):
    """Parse final_score and guard_passed from train.py stdout"""
    score_match = re.search(r"final_score:\s*([\d\.]+)", output)
    guard_match = re.search(r"guard_passed:\s*(True|False)", output)
    if not score_match:
        return 0.0, False
    
    score = float(score_match.group(1))
    guard_passed = guard_match.group(1) == "True"
    return score, guard_passed

def simulate_llm_editing_train_py():
    """
    Simulates the LLM receiving program.md and editing train.py.
    Reads train.py, changes the 'zone' assignment string, and writes back.
    """
    with open(TRAIN_FILE, 'r') as f:
        content = f.read()

    # Find all current zone assignments
    matches = list(re.finditer(r'"zone":\s*"([^"]+)"', content))
    if not matches:
        return content

    # Simulate random LLM edits: we tweak one or two zones
    # Bias: if priority is P0, move to a top zone (reading program.md rule)
    new_content = copy.copy(content)
    
    for _ in range(random.randint(1, 2)):
        idx = random.randint(0, len(matches) - 1)
        match = matches[idx]
        
        # Super basic heuristic check via regex back-look
        preceding_text = content[max(0, match.start()-50):match.start()]
        
        new_zone = ""
        if '"P0"' in preceding_text and random.random() < 0.8:
            new_zone = random.choice(["top_action_bar", "top_first_row"])
        else:
            new_zone = random.choice(ZONES)
            
        new_content = new_content[:match.start()] + f'"zone": "{new_zone}"' + new_content[match.end():]
        # Refresh matches for string shifts
        matches = list(re.finditer(r'"zone":\s*"([^"]+)"', new_content))

    return new_content

def run_train_py():
    result = subprocess.run(["python", TRAIN_FILE], capture_output=True, text=True)
    return parse_score(result.stdout)

def save_train_py(content):
    with open(TRAIN_FILE, 'w') as f:
        f.write(content)

def read_train_py():
    with open(TRAIN_FILE, 'r') as f:
        return f.read()

def run_launch():
    print("🚀 AutoResearch active: Reading program.md and optimizing train.py...")
    
    if not os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, 'w', newline='') as f:
            f.write("Iteration,Score,Guard_Passed,Action\n")

    best_score, best_guard = run_train_py()
    print(f"📊 Baseline Score: {best_score:.4f} (Guard: {best_guard})")
    
    with open(RESULT_FILE, 'a', newline='') as f:
        f.write(f"0,{best_score:.4f},{best_guard},BASELINE\n")

    current_code = read_train_py()
    no_improve_count = 0

    for i in range(1, MAX_ROUNDS + 1):
        print(f"\n--- Iteration {i} ---")
        
        candidate_code = simulate_llm_editing_train_py()
        save_train_py(candidate_code)
        
        score, passed_guard = run_train_py()
        action = "DISCARD"
        
        if score > best_score:
            print(f"✅ train.py improved! Score: {best_score:.4f} -> {score:.4f}")
            if passed_guard:
                print("🛡️ Guardrails passed. Keeping train.py changes.")
                best_score = score
                current_code = candidate_code
                action = "KEEP"
                no_improve_count = 0
            else:
                print("❌ Failed safety guards. Reverting train.py.")
                save_train_py(current_code)
                action = "REJECT_UNSAFE"
        else:
            print(f"📉 Score decreased ({score:.4f}). Reverting train.py.")
            save_train_py(current_code)
            action = "DISCARD"
            no_improve_count += 1
            
        with open(RESULT_FILE, 'a', newline='') as f:
            f.write(f"{i},{score:.4f},{passed_guard},{action}\n")
            
        if no_improve_count >= 15:
            print("\n🛑 Stopping limit reached (15 rounds no improvement).")
            break

    print(f"\n🏆 Autoresearch complete. Best Layout Score: {best_score:.4f}")

if __name__ == "__main__":
    run_launch()
