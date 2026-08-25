---
name: idea-diamond
description: Validate a startup idea with the Diamond graph — a decision contract frozen before any evidence exists, parallel blind researchers (customer / competitor / distribution / economics / risk), an adversarial skeptic, an independent merge, and a human gate. Use when someone says "should I build X", shares a new idea, asks whether an idea is worth testing, or wants market, customer, competitor or go-to-market research. Produces a one-page pursue / pause / kill recommendation with a graded evidence trail in ideas/<slug>/.
---

# Idea Diamond

Read `${CLAUDE_PLUGIN_ROOT}/skills/idea-diamond/WORKFLOW.md` first. It holds the
shared rules this runbook assumes: information design, evidence grades A–D,
anti-noise limits, verdict honesty, gates, resumability.

**The one rule everything else serves:** the model that writes the answer never
grades the answer.

**Final output, one sentence:** a one-page recommendation on whether this idea is
worth testing — the wedge, the first customer, the riskiest assumption, the
7-day test, and what would change our mind, every claim sourced and graded.

Work in the user's current directory. Templates live at
`${CLAUDE_PLUGIN_ROOT}/skills/idea-diamond/templates/`.

---

## Node 0 — Intake (you + the human, no research)

Create `ideas/<slug>/`, copy `templates/state.json` into it, fill the header.

Ask in ONE `AskUserQuestion` round where options fit, plain questions otherwise.
Do not research yet. Do not react to the idea yet.

1. The idea in one sentence — what it does, for whom.
2. Who *exactly* is the first customer? Push for a segment they could name 20
   real examples of. "Small businesses" is not an answer.
3. What do they do today instead? The real competitor is usually a spreadsheet,
   an intern, or nothing.
4. Why you, why now?
5. What are they willing to spend — weeks, dollars, side project or main thing?
6. What would make them walk away? Get the instinct on record *before* evidence.

Write `00-intake.md`. If the user has asked you not to stop, record the answers
you would have asked for as **ASSUMED (grade D)**, flag each one loudly, and
carry on — never silently invent them.

## Node 0b — Contract, then FROZEN

Write `01-contract.md` from `templates/contract.md`: the decision and its
options; 4–6 falsifiable must-be-true claims; the pursue bar with grades; kill
criteria in numbers; constraints; what would change our mind either way.

Then dispatch **`diamond-contract-auditor`** with the contract and the intake.
Apply its mandatory changes, mark the contract **FROZEN <date>**, and stop
editing it. If evidence later shows the contract was wrong, that is a finding
for `07-decision.md`, not a silent edit.

## Node 1 — Planner

Dispatch **`diamond-planner`** with the neutral idea statement, the segment, the
status quo, the constraints, and one line on the decision at stake. Do **not**
give it the kill criteria. Save `02-plan.md`. Show the lane list to the user —
one line each — and proceed unless redirected.

## Node 2 — Lanes, parallel and blind

Dispatch one **`diamond-researcher`** per lane, **all in a single message** so
they run concurrently. Each gets only: the neutral idea statement, its own brief
from the plan, and its unknown-unknowns instruction. Never the kill criteria,
never another lane's output, never a hint of what the user hopes.

Each writes `03-<lane>.md` using `templates/lane-report.md`.

**Early stop:** if a lane definitively fires a kill criterion, stop the remaining
lanes, note it in `state.json`, and go to node 4. Finishing the rest for
completeness is fake work. If lanes are already in flight, let them finish rather
than discarding spent effort — and say which you did.

## Node 3 — Skeptic

Dispatch **`diamond-skeptic`** with the frozen contract and every lane report.
Writes `04-skeptic.md`. For a high-stakes call, dispatch a second one in the same
message with the opposite lens: steelman the incumbent's response and the case
that the timing is wrong.

If the skeptic identifies a disputed fact that moves a criterion, resolve it
yourself with a live source before the merge, and write the adjudication to
`04-factcheck.md`. One page load can be worth more than another lane.

## Node 4 — Merge

Dispatch **`diamond-merge`** with the contract, the lane reports, the skeptic,
and any factcheck. Writes `05-recommendation.md`.

**Split-verdict check**, for a decision that commits real money or months: run
two merge agents independently on identical evidence, in the same message. If
they disagree on pursue versus kill, **that disagreement is the finding** — drop
to 🟡 and name the unknown that splits them.

## Node 4b — Referee (expensive decisions)

Dispatch **`diamond-referee`** with the contract, the evidence, and the
recommendation. Do **not** tell it whether anyone agreed. Writes `06-referee.md`.

## Node 5 — Human gate (hard stop)

Refresh the dashboard, then present, in this order: the verdict and its
confidence; the three pieces of evidence that decided it; the strongest argument
against; the 7-day test with its pass and fail lines stated up front; and the
options — **pursue · pause · kill · one more targeted lane** (which must name a
specific question, never "research more").

Then wait. Do not decide for the user, do not lobby, and do not soften a kill to
be encouraging. Record their call in `07-decision.md` and set `state.json` to
`closed`.

## Node 6 — Knowledge (always, especially on a kill)

Append, dated, never overwriting, to `knowledge/`: `decision-log.md`,
`customer-notes.md`, `competitor-db.md`, `distribution-playbook.md`,
`sources-index.md`. A kill that produces good notes makes the next three ideas
faster. That is the compounding.

## Dashboard

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/dashboard.py" <slug>     # this run
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/dashboard.py" --all      # every run
```

View-only by design. Refresh it after the lanes, after the merge, and at the
gate. Update `state.json` at the start and end of every node.
