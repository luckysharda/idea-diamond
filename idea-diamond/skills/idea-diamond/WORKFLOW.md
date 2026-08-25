# The Diamond — graph engineering rules for this repo

This is the shared contract every graph in this repo obeys. The three runbooks
(`idea-diamond`, `code-diamond`, `content-diamond`) are the same shape pointed at
different work.

Source shape: the "Diamond" from the Startup Ideas Podcast episode on graph
engineering (planner → parallel researchers → skeptic → merge → human gate).
Rigor layer: frozen contracts, blind workers, independent judges, evidence
ledgers, honest red/yellow/green, and resumable state.

---

## 0. The one rule that makes this worth doing

**The model that writes the answer never grades the answer.**

Everything below is machinery in service of that one sentence. If you ever find a
single agent researching, concluding, and rating its own confidence, the graph
has collapsed back into a chat and the output is worth what a chat is worth.

---

## 1. The shape

```
                        ┌──────────────┐
                        │ 0. INTAKE    │  human + Claude, no research
                        └──────┬───────┘
                        ┌──────▼───────┐
                        │ 0b. CONTRACT │  frozen before any evidence exists
                        │  + AUDIT     │  fresh agent attacks the contract
                        └──────┬───────┘
                        ┌──────▼───────┐
                        │ 1. PLANNER   │  splits into angles, writes briefs
                        └──────┬───────┘        (does no research itself)
          ┌────────────────────┼────────────────────┐
    ┌─────▼─────┐        ┌─────▼─────┐        ┌─────▼─────┐
    │  LANE A   │        │  LANE B   │        │  LANE C   │   run in parallel,
    │           │        │           │        │           │   blind to each other
    └─────┬─────┘        └─────┬─────┘        └─────┬─────┘
          └────────────────────┼────────────────────┘
                        ┌──────▼───────┐
                        │ 3. SKEPTIC   │  fresh agent, paid to kill it
                        └──────┬───────┘
                        ┌──────▼───────┐
                        │ 4. MERGE     │  survivors → one page
                        └──────┬───────┘
                        ┌──────▼───────┐
                        │ 4b. REFEREE  │  optional; blind check of the verdict
                        └──────┬───────┘
                        ┌──────▼───────┐
                        │ 5. HUMAN GATE│  you decide. always.
                        └──────┬───────┘
                        ┌──────▼───────┐
                        │ 6. KNOWLEDGE │  state compounds into knowledge/
                        └──────────────┘
```

Every node writes a file. The files are the state. A context reset loses nothing.

---

## 2. Information design (who is allowed to know what)

This table is the part that actually produces quality. Violating it is how you get
five agents confidently repeating the same wrong idea.

| Node | Receives | Must never receive |
|---|---|---|
| Planner | idea, intake answers, frozen contract, `knowledge/` | — |
| Each lane worker | *neutral* idea statement, its own lane brief, evidence rules, `knowledge/` | other lanes' drafts, the kill criteria, any hint of what the human hopes is true |
| Skeptic | frozen contract, all lane reports, `knowledge/` | what the human hopes is true, any draft recommendation |
| Merge | frozen contract, lane reports, skeptic report | what the human hopes is true |
| Referee | frozen contract, evidence ledger with lane labels stripped, the recommendation | who wrote what, what the human hopes is true |
| Human gate | everything | — |

**Neutral idea statement**: strip the enthusiasm before handing the idea to a lane.
Not "my idea for finally fixing bookkeeping for Shopify sellers" but "software that
automates monthly bookkeeping for Shopify merchants doing $10k–$500k/mo".

**Lane briefs are open questions, never leading ones.**
- Bad: "Confirm that Shopify merchants hate their bookkeeper."
- Good: "How do Shopify merchants at this revenue band handle bookkeeping today,
  what does each option cost them in money and hours, and what evidence exists
  either way about how much that bothers them?"

---

## 3. Evidence rules

Every claim in every lane report carries three things: **source, date, grade.**

| Grade | Meaning |
|---|---|
| **A** | Primary. A named user's own words, a real price on a real pricing page, a filing, first-party data, an actual job post, a real transaction. |
| **B** | Credible secondary. Reputable report, competitor docs/changelog, well-sourced article, a specific forum/Reddit thread where the person is clearly the user. |
| **C** | Inference. Reasoning, analogy from an adjacent market, an estimate. Legitimate — but it must be labeled C. |
| **D** | Assumption. No source at all. Allowed only if labeled D and added to the "what we'd have to test" list. |

Rules:
- **Staleness**: every source needs a date. Older than 18 months → flag it. Older
  than 36 months in a fast-moving category → downgrade one grade.
- **No laundering**: a C claim cited by a later node stays C. Grades never rise by
  being repeated.
- **Confidence ceiling**: no node may assert high confidence in a conclusion whose
  support is only C and D. This is enforced by the skeptic.
- **Pain ≠ willingness to pay.** Complaint volume is C evidence about pain and D
  evidence about revenue, always. Only money changing hands is A evidence about
  money.
- **Numbers get shown**: any market size, CAC, or conversion figure includes the
  arithmetic and the inputs, or it is D.

---

## 4. Anti-noise rules (from the article's "the mistake")

The goal is the smallest graph that improves the work — not the most agents.

1. **Max 5 lanes.** Three is the default. A fourth or fifth needs a reason written
   in `plan.md`.
2. **Cap the output.** Each lane returns at most 10 ranked claims plus its ledger.
   A 4,000-word lane report is a lane that failed to decide what mattered.
3. **No overlap.** A lane may not answer another lane's question. If two lanes hit
   the same fact, that's fine; if a lane starts *researching* another lane's
   question, the planner scoped it wrong.
4. **Early stop.** If a kill criterion from the frozen contract is definitively
   triggered mid-run, stop the remaining lanes, write it up, and go to the gate.
   Finishing all the lanes to be thorough is fake work.
5. **Good enough is a stop condition.** If the recommendation would be the same at
   70% and at 95%, stop at 70%.
6. **Remove fake waiting.** Lanes that don't depend on each other start in the same
   message, not one after another.

---

## 5. Verdicts are honest or they're worthless

The run ends in one of four states, and **kill is a success**:

| Verdict | Means |
|---|---|
| 🟢 **Pursue** | Contract's pursue-bar cleared on A/B evidence. Next test is named. |
| 🟡 **Pause / needs evidence** | One specific unknown decides it. The run names the unknown and the cheapest way to resolve it — not "more research". |
| 🔴 **Kill** | A kill criterion fired. Write down *why*, so the next idea inherits it. |
| ⚪ **Inconclusive** | The evidence is too thin to say. Say that. Never dress it as 🟡. |

Forbidden:
- Manufacturing a 🟢 because effort was spent.
- Softening a kill criterion after seeing the evidence. The contract is frozen; if
  it was wrong, say "the contract was wrong and here is why" in the decision file —
  don't edit it silently.
- Confidence that isn't tied to evidence grade.

---

## 6. Human gates

A gate goes wherever a mistake gets expensive.

- **Light gate** (you skim, Claude proceeds): intake, plan, lane briefs.
- **Hard gate** (Claude stops and waits): the verdict, anything that spends money,
  contacts a real person, publishes publicly, deploys code, or touches production
  data or real customers.

Claude never sends an outreach message, buys a domain, posts publicly, or emails
anyone as part of a research run. It drafts; you send.

---

## 7. Resumability

`ideas/<slug>/state.json` is the source of truth for where a run is.

- Every node updates it on start (`running`) and finish (`done`).
- First action in any session, before anything else: read `state.json`, report the
  stage, resume from the first non-`done` node.
- A node's file existing but `state.json` saying `running` means that node was
  interrupted — re-run it, don't trust a partial file.

Node status values: `pending` · `running` · `done` · `blocked` · `skipped`.

---

## 8. Levels (where this repo sits)

- **Level 1** — manual lanes, one chat per lane. Slow, clear, always available.
- **Level 2** — *this repo*. Claude Code, each node writes a file, state.json for
  resume, local HTML dashboard. Paper trail + version comparison + reuse.
- **Level 3** — LangGraph (checkpoints, persistence, human-in-the-loop), AutoGen
  GraphFlow (branches/loops), n8n/Make when the graph has to touch Slack, email,
  Airtable, a CRM. Only worth it once a Level 2 graph has run several times and
  earned its automation.

Do not skip to Level 3. If the manual version produces mediocre work, automating it
produces mediocre work faster.

---

## 9. Knowledge compounds

Every run appends to `knowledge/`. That's the whole long game: the graph produces
the work *and* the context that makes the next graph smarter.

- `knowledge/customer-notes.md` — who the buyers are, what they use, what they pay
- `knowledge/competitor-db.md` — tools seen, positioning, pricing, last checked
- `knowledge/distribution-playbook.md` — channels tried/observed, what converts
- `knowledge/decision-log.md` — every verdict, one line, with the reason
- `knowledge/sources-index.md` — sources worth re-reading, with dates

Rule: append, don't rewrite. Date every entry. If a later run contradicts an older
entry, add the correction underneath it rather than deleting — the disagreement is
information.

---

## 10. Dashboard

```
python3 tools/dashboard.py <idea-slug>     # writes and opens dashboard.html
python3 tools/dashboard.py --all           # index of every run
```

View-only. Decisions happen in Claude Code, not in the dashboard.
