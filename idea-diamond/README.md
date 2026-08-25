# idea-diamond

Validate a startup idea the way a careful team would: split the work into jobs,
run the jobs that don't depend on each other at the same time, and **never let
the model that writes the answer be the model that grades it**.

## The problem it solves

Ask a chat "should I build this?" and you get a confident answer in seconds —
market size, competitors, a go-to-market plan. Slow down and look at what
happened: one model, in one pass, decided what mattered, researched it,
interpreted its own evidence, wrote the recommendation, and then graded its own
confidence. That is a lot of trust in one blob of text, and people spend years of
their life on it.

## Install

```
/plugin marketplace add /path/to/startupresearch/plugins
/plugin install idea-diamond@startupresearch
```

## Use

```
/idea-diamond an AI bookkeeping product for Shopify merchants
```

Or just describe an idea — the skill's description routes it.

## The graph

```
INTAKE ─► CONTRACT (frozen) ─► PLANNER ─┬─► customer ────┐
             + audit                    ├─► competitor ──┤  parallel,
                                        ├─► distribution ┤  blind to
                                        ├─► economics    ┤  each other
                                        └─► risk ────────┘
                                                         ▼
                                    SKEPTIC ─► MERGE ─► REFEREE ─► HUMAN GATE
```

Every node writes a file into `ideas/<slug>/`, so a context reset loses nothing
and you can read exactly how the answer was reached.

## What makes it different from asking nicely

**The contract is frozen before any evidence exists.** Kill criteria written
after seeing the data are not kill criteria. An independent auditor attacks the
contract first — in practice it routinely finds criteria that could never fire,
because they demand evidence nobody ever publishes.

**Lane workers run blind.** They get a *neutral* statement of the idea with the
enthusiasm stripped out, their own brief, and nothing else. Never the kill
thresholds, never another lane's draft, never a hint of what you hope is true.
Otherwise you get five agents agreeing with each other loudly.

**Every claim carries source, date and grade.** A = a real user's words or a real
price. B = credible secondary. C = inference, show the arithmetic. D =
assumption, labelled. Grades never rise by being repeated, and pain is never
evidence about money.

**The skeptic attacks the researchers, not the idea.** Grade inflation, stale
sources, popularity read as revenue, arithmetic measured at the wrong operating
point, and contradictions between lanes that no single lane could see.

**Kill is a success.** A clean 🔴 with a precise reason is worth more than a
manufactured 🟢, and it makes the next three ideas faster.

## What ships

| | |
|---|---|
| `/idea-diamond` | the command |
| `idea-diamond` skill | the runbook, node by node |
| 6 agents | contract auditor · planner · researcher · skeptic · merge · referee |
| templates | contract, plan, lane report, skeptic, recommendation, decision, state |
| `scripts/dashboard.py` | a local, view-only HTML dashboard of any run |

Decisions happen in Claude Code, not in the dashboard. The graph makes the
decision better informed. You still make it.

## Credit

The Diamond shape comes from the Startup Ideas Podcast episode on graph
engineering. The rigour layer — frozen contracts, blind workers, independent
judges, graded evidence, honest verdicts — was added in practice.

MIT.
