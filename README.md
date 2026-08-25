# idea-diamond

A Claude Code plugin marketplace holding **idea-diamond** — validate a startup
idea with a graph of agents instead of one confident paragraph.

## Install

```
/plugin marketplace add luckysharda/idea-diamond
/plugin install idea-diamond@startupresearch
```

Then:

```
/idea-diamond an AI bookkeeping product for Shopify merchants
```

## Why

Ask a chat "should I build this?" and one model, in one pass, decides what
matters, researches it, interprets its own evidence, writes the recommendation,
and grades its own confidence. That is a lot of trust in one blob of text.

This plugin splits that into jobs, runs the independent ones in parallel, and
makes sure **the model that writes the answer is never the model that grades it**.

Full detail: [`idea-diamond/README.md`](./idea-diamond/README.md)

## What's in here

```
.claude-plugin/marketplace.json    the marketplace
idea-diamond/                      the plugin
  .claude-plugin/plugin.json
  commands/idea-diamond.md
  skills/idea-diamond/            runbook, shared rules, 7 templates
  agents/                         6 agents: auditor, planner, researcher,
                                  skeptic, merge, referee
  scripts/dashboard.py            local, view-only run dashboard
```

MIT.
