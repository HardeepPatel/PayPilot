# PayPilot Layout Engine
### Autoresearch UI Agent for Payment Dashboards

Inspired by Andrej Karpathy’s original [autoresearch](https://github.com/karpathy/autoresearch) and extended using ideas from Langfuse’s [autoresearch writeup](https://langfuse.com/blog/2026-03-24-optimizing-ai-skill-with-autoresearch), this project applies the autoresearch loop to a new domain:

> **UI layout optimization for complex payment dashboards**

Instead of optimizing model training (`val_bpb`), this system optimizes **where features are placed on a dashboard**.

---

## 🧠 Core Idea

Payment dashboards are dense and operationally critical. They contain features like:

- Refunds  
- Payouts  
- Failed payments  
- Disputes  
- Risk alerts  
- Settlements  
- Analytics and exports  

The real problem is:

> **Where should each feature be placed so users can act faster, with fewer clicks, and without missing critical actions?**

This system solves that using an **autoresearch loop**:

- Propose a layout  
- Evaluate it using UI metrics  
- Enforce safety constraints  
- Keep only improvements  
- Repeat  

---

## 🔄 Autoresearch Loop (UI Version)

```mermaid
graph TD
    A[Baseline Layout train.py] --> B[Proposer Agent]
    B -->|Modify layout| C[train.py]
    
    C --> D{Evaluator prepare.py}
    D -->|Compute Score| E[Score]
    
    E --> F{Guardrails}
    
    F -->|Fail| G[Reject & Revert]
    F -->|Pass| H{Better Score?}
    
    H -->|Yes| I[Keep Change]
    H -->|No| J[Discard Change]
    
    I --> B
    J --> B
    G --> B
```

---

## 🏗️ Architecture (1:1 with Original Autoresearch)

To stay faithful to the original design, we preserve the same file structure and philosophy:

### 1. `prepare.py`
- Fixed evaluation harness  
- Computes UI score  
- Enforces safety guardrails  
- **Never modified by the agent**

---

### 2. `train.py`
- **The only file the agent edits**  
- Represents the dashboard layout  
- Maps features → UI zones  

👉 Equivalent to modifying model architecture in the original autoresearch

---

### 3. `program.md`
- Instruction file for the agent  
- Defines UI rules:
  - P0 features must be visible  
  - Minimize clicks for critical workflows  
  - Avoid cluttering the primary screen  

---

### 4. `launch.py`
- Supervisor loop  
- Runs the full cycle:
  - Triggers edits  
  - Executes evaluation  
  - Compares scores  
  - Accepts or reverts changes  
- Logs all runs to `result.csv`

---

### 📁 Project Structure

```
.
├── prepare.py      # evaluator (never edited)
├── train.py        # layout definition (agent edits this)
├── program.md      # agent instructions
├── launch.py       # optimization loop
├── result.csv      # iteration logs
```

---

## 📊 Evaluation Metrics

Instead of `$val_bpb`, the target function maximizes a **UI layout score** based on concrete UX parameters:

- **Task Success**  
  Ensures critical workflows (refunds, payouts, disputes) are always completable.  
  Guaranteed only if safety guardrails pass.

- **Speed**  
  Measures how quickly users can access critical features.  
  Rewards placing `P0` elements (Refunds, Failed Payments, Payout Status) in top zones.

- **Priority Alignment**  
  Rewards correct placement of features:
  - `P0` → top row / action bar  
  - `P1` → first screen  
  - Penalizes hidden or misplaced items  

- **Discoverability (Clutter Penalty)**  
  Penalizes overcrowded primary UI.  
  Strongly penalizes placing `P3` (rare/admin tools) in top-level zones.

- **Safety** (**Hard Guardrail**)  
  Failing to expose `P0` features correctly **invalidates the run immediately** (`REJECT_UNSAFE`).

---

## 📊 Evaluation Function

```
score =
  0.30 * task_success
+ 0.25 * speed
+ 0.20 * priority_alignment
- 0.10 * clutter_penalty
```

---

## 🚨 Guardrails (Critical for Payments)

This system enforces strict safety rules:

- P0 features must always be visible  
- Refunds, payouts, and disputes cannot be hidden  
- Critical actions must be reachable quickly  
- No layout can reduce operational visibility  

If violated → layout is **immediately rejected**

---

## ▶️ Run the System

```bash
python launch.py
```

---

## 📊 Output

- `train.py` → best layout found  
- `result.csv` → full optimization history  

---

## 🖼️ UI Optimization Outcome

Running `launch.py` creates a continuous optimization loop that:

- Explores multiple layout variations  
- Rejects unsafe configurations  
- Retains only layouts that improve UX score  
- Converges toward an optimal, safe dashboard structure  

The final result represents a **high-quality layout configuration** that satisfies both usability and payment safety constraints.

![Optimized Dashboard Layout](mockup.png)

*Example outcome: `Refund Queue` and `Payout Status` are placed in top-level zones (`top_first_row`, `top_action_bar`), ensuring maximum visibility and fast access for critical workflows.*

---

## 🧬 Why This Matters

UI design is usually subjective.

This project makes it:

> **measurable, testable, and optimizable**

It connects:
- LLM agents  
- UI/UX design  
- Fintech dashboards  
- Continuous optimization loops  

---

## 🧠 Mental Model

| Layer | Role |
|------|------|
| PayPilot | Displays financial data |
| PayPilot Layout Engine | Decides feature placement |

---

## 📌 Summary

**PayPilot Layout Engine** applies autoresearch to UI systems.

> Instead of training models, it trains **dashboard layouts**.

It continuously improves feature placement based on usability, priority, and safety constraints.
