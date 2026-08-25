---
description: Validate a startup idea through the Diamond graph — frozen contract, blind parallel research, adversarial skeptic, independent merge, human gate
argument-hint: [the idea, in a sentence or two]
allowed-tools: ["Skill", "Task", "Read", "Write", "Edit", "Glob", "Grep", "Bash", "WebSearch", "WebFetch", "AskUserQuestion"]
---

Run the Diamond graph on this idea:

$ARGUMENTS

Invoke the `idea-diamond` skill and follow it node by node. Do not answer
"should I build this?" from your own knowledge — that single-blob-of-text answer
is the failure this whole workflow exists to avoid.

Non-negotiables:

- Freeze the contract **before** looking at any evidence. Kill criteria written
  after seeing the data are not kill criteria.
- Launch the lane researchers in **one message** so they run in parallel, blind
  to each other, to the kill criteria, and to what the user hopes is true.
- Every claim carries source, date and grade. Unsourced is grade D and gets
  labelled, never hidden.
- Kill is a valid success. "Inconclusive" is an allowed and sometimes correct
  answer. Never manufacture a pursue because effort was spent.
- Stop at the human gate and let the user decide.

If no idea was supplied, ask for it in one sentence before doing anything else.
