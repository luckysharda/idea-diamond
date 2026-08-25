#!/usr/bin/env python3
"""Local, view-only dashboard for Diamond runs.

    python3 tools/dashboard.py <slug>      build + open ideas/<slug>/dashboard.html
    python3 tools/dashboard.py --all       build + open ideas/index.html
    python3 tools/dashboard.py <slug> --no-open

No dependencies. Decisions happen in Claude Code, not here.
"""

import html
import json
import os
import re
import sys
import webbrowser
from datetime import date

# Runs from inside the installed plugin, so the script's own location is the
# plugin folder — NOT the project. Runs are always relative to where the user
# is working. Walk up from the cwd to find the folder that holds ideas/, so it
# also works from inside ideas/<slug>/.
def _find_root():
    override = os.environ.get("IDEA_DIAMOND_PROJECT")
    if override:
        return os.path.abspath(override)
    here = os.getcwd()
    probe = here
    for _ in range(6):
        if os.path.isdir(os.path.join(probe, "ideas")):
            return probe
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    return here


ROOT = _find_root()
IDEAS = os.path.join(ROOT, "ideas")

STATUS = {
    "done":    ("done",    "#1a7f37"),
    "running": ("running", "#bf6b00"),
    "pending": ("pending", "#8a8a8a"),
    "blocked": ("blocked", "#c62828"),
    "skipped": ("skipped", "#b9b9b9"),
}

VERDICT = {
    "pursue":       ("🟢 pursue", "#1a7f37"),
    "pause":        ("🟡 pause",  "#bf6b00"),
    "kill":         ("🔴 kill",   "#c62828"),
    "inconclusive": ("⚪ inconclusive", "#8a8a8a"),
}

ROWS = [
    ["intake"],
    ["contract", "contract_audit"],
    ["plan"],
    ["lane_customer", "lane_competitor", "lane_distribution",
     "lane_economics", "lane_risk"],
    ["skeptic"],
    ["merge", "referee"],
    ["gate"],
    ["knowledge"],
]

LABELS = {
    "intake": "0 · Intake",
    "contract": "0b · Contract (frozen)",
    "contract_audit": "0b · Contract audit",
    "plan": "1 · Planner",
    "lane_customer": "2 · Customer",
    "lane_competitor": "2 · Competitor",
    "lane_distribution": "2 · Distribution",
    "lane_economics": "2 · Economics",
    "lane_risk": "2 · Risk",
    "skeptic": "3 · Skeptic",
    "merge": "4 · Merge",
    "referee": "4b · Referee",
    "gate": "5 · Human gate",
    "knowledge": "6 · Knowledge",
}


# ---------------------------------------------------------------- markdown-lite

def _inline(t):
    t = html.escape(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    return t


def md(text):
    out, lines, i = [], text.split("\n"), 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("```"):
            body = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(html.escape(lines[i]))
                i += 1
            out.append("<pre><code>" + "\n".join(body) + "</code></pre>")
            i += 1
            continue

        if line.startswith("|") and i + 1 < len(lines) and re.match(
                r"^\|[\s:\-\|]+\|?\s*$", lines[i + 1]):
            def cells(row):
                return [c.strip() for c in row.strip().strip("|").split("|")]
            head = cells(line)
            i += 2
            body = []
            while i < len(lines) and lines[i].startswith("|"):
                body.append(cells(lines[i]))
                i += 1
            t = ["<table><thead><tr>"]
            t += ["<th>%s</th>" % _inline(c) for c in head]
            t.append("</tr></thead><tbody>")
            for r in body:
                t.append("<tr>" + "".join(
                    "<td>%s</td>" % _inline(c) for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lvl = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, _inline(m.group(2)), lvl))
            i += 1
            continue

        if re.match(r"^\s*(-{3,}|\*{3,})\s*$", line):
            out.append("<hr>")
            i += 1
            continue

        if re.match(r"^\s*[-*+]\s+", line) or re.match(r"^\s*\d+\.\s+", line):
            ordered = bool(re.match(r"^\s*\d+\.\s+", line))
            items = []
            while i < len(lines) and (
                    re.match(r"^\s*[-*+]\s+", lines[i])
                    or re.match(r"^\s*\d+\.\s+", lines[i])):
                items.append(_inline(
                    re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", lines[i])))
                i += 1
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (
                tag, "".join("<li>%s</li>" % x for x in items), tag))
            continue

        if line.startswith(">"):
            body = []
            while i < len(lines) and lines[i].startswith(">"):
                body.append(_inline(lines[i].lstrip("> ")))
                i += 1
            out.append("<blockquote>%s</blockquote>" % "<br>".join(body))
            continue

        if not line.strip():
            i += 1
            continue

        para = []
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#{1,6}\s|```|\||\s*[-*+]\s|\s*\d+\.\s|>)", lines[i]):
            para.append(_inline(lines[i]))
            i += 1
        if para:
            out.append("<p>%s</p>" % "<br>".join(para))
        else:
            i += 1
    return "\n".join(out)


# ------------------------------------------------------------------------- css

CSS = """
:root{--bg:#fdfaf7;--fg:#1b1917;--muted:#6f6a66;--line:#e6ddd4;--card:#fff;
--accent:#e8590c;--accent-soft:#fdece1;--code:#f4efe9}
@media (prefers-color-scheme:dark){:root{--bg:#16130f;--fg:#efe9e3;--muted:#9d948c;
--line:#332c25;--card:#1e1a16;--accent:#ff8a4c;--accent-soft:#2a1c12;--code:#231e19}}
*{box-sizing:border-box}
body{margin:0;padding:2.2rem 1.4rem 5rem;background:var(--bg);color:var(--fg);
font:15px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,sans-serif}
.wrap{max-width:1080px;margin:0 auto}
h1{font-size:1.9rem;letter-spacing:-.02em;margin:0 0 .3rem}
h2{font-size:1.15rem;margin:2.4rem 0 .8rem;letter-spacing:-.01em}
h3{font-size:1rem;margin:1.4rem 0 .5rem}
a{color:var(--accent)}
.sub{color:var(--muted);margin:0 0 1.6rem}
.bar{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0 2rem}
.pill{border:1px solid var(--line);background:var(--card);border-radius:999px;
padding:.25rem .75rem;font-size:.8rem;color:var(--muted)}
.pill b{color:var(--fg)}
.graph{border:1px solid var(--line);background:var(--card);border-radius:14px;
padding:1.3rem;overflow-x:auto}
.row{display:flex;gap:.6rem;justify-content:center;flex-wrap:wrap;margin:.35rem 0}
.node{border:1px solid var(--line);border-radius:10px;padding:.5rem .8rem;
min-width:150px;background:var(--bg);font-size:.82rem;text-align:center}
.node .lbl{font-weight:600}
.node .st{font-size:.7rem;text-transform:uppercase;letter-spacing:.07em;
margin-top:.2rem}
.node.done{border-color:#1a7f3755;background:#1a7f370f}
.node.running{border-color:#bf6b0088;background:#bf6b0014}
.node.blocked{border-color:#c6282888;background:#c6282814}
.node.skipped{opacity:.42}
.arrow{text-align:center;color:var(--muted);font-size:.85rem;line-height:1}
.verdict{display:inline-block;border-radius:10px;padding:.55rem 1rem;
font-weight:650;border:1px solid var(--line);background:var(--accent-soft)}
details{border:1px solid var(--line);border-radius:12px;background:var(--card);
margin:.6rem 0;padding:.2rem .95rem}
details[open]{padding-bottom:1rem}
summary{cursor:pointer;padding:.7rem 0;font-weight:600;list-style:none}
summary::-webkit-details-marker{display:none}
summary::before{content:"▸ ";color:var(--accent)}
details[open] summary::before{content:"▾ "}
table{border-collapse:collapse;width:100%;margin:.8rem 0;font-size:.88rem;
display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:.42rem .6rem;text-align:left;
vertical-align:top}
th{background:var(--accent-soft)}
code{background:var(--code);padding:.1rem .3rem;border-radius:4px;font-size:.87em}
pre{background:var(--code);padding:.85rem;border-radius:9px;overflow-x:auto}
pre code{background:none;padding:0}
blockquote{border-left:3px solid var(--accent);margin:.8rem 0;padding:.1rem .9rem;
color:var(--muted)}
hr{border:0;border-top:1px solid var(--line);margin:1.6rem 0}
.foot{color:var(--muted);font-size:.8rem;margin-top:3rem;border-top:1px solid
var(--line);padding-top:1rem}
"""


def page(title, body):
    return ("<!doctype html><html><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>%s</title><style>%s</style></head><body><div class='wrap'>%s"
            "<p class='foot'>View-only. Decisions happen in Claude Code, not here."
            " · rebuilt %s</p></div></body></html>"
            % (html.escape(title), CSS, body, date.today().isoformat()))


# ----------------------------------------------------------------------- build

def graph_html(nodes):
    parts = ["<div class='graph'>"]
    for ri, row in enumerate(ROWS):
        cells = []
        for key in row:
            n = nodes.get(key)
            if n is None:
                continue
            st = n.get("status", "pending")
            if st == "skipped" and key in ("lane_economics", "lane_risk",
                                           "referee", "contract_audit"):
                continue
            label, _ = STATUS.get(st, STATUS["pending"])
            note = n.get("note", "")
            cells.append(
                "<div class='node %s'><div class='lbl'>%s</div>"
                "<div class='st'>%s</div>%s</div>"
                % (st, html.escape(LABELS.get(key, key)), label,
                   ("<div class='st' style='opacity:.6'>%s</div>"
                    % html.escape(note)) if note else ""))
        if not cells:
            continue
        parts.append("<div class='row'>%s</div>" % "".join(cells))
        if ri < len(ROWS) - 1:
            parts.append("<div class='arrow'>↓</div>")
    parts.append("</div>")
    return "".join(parts)


def build_idea(slug, do_open=True):
    folder = os.path.join(IDEAS, slug)
    if not os.path.isdir(folder):
        sys.exit("no such idea folder: %s" % folder)

    sp = os.path.join(folder, "state.json")
    state = {}
    if os.path.exists(sp):
        with open(sp) as f:
            state = json.load(f)
    nodes = state.get("nodes", {})
    ev = state.get("evidence", {})

    v = (state.get("verdict") or "").lower()
    vlabel, vcolor = VERDICT.get(v, ("— not yet decided —", "#8a8a8a"))

    body = ["<h1>%s</h1>" % html.escape(state.get("slug") or slug)]
    body.append("<p class='sub'>%s</p>"
                % html.escape(state.get("one_liner", "")))
    body.append("<p><span class='verdict' style='color:%s'>%s</span></p>"
                % (vcolor, vlabel))

    pills = [
        ("stage", state.get("stage", "—")),
        ("confidence", state.get("confidence") or "—"),
        ("contract frozen", state.get("contract_frozen") or "not yet"),
        ("updated", state.get("updated") or "—"),
    ]
    ev_pills = [("evidence A", ev.get("A", 0)), ("B", ev.get("B", 0)),
                ("C", ev.get("C", 0)), ("D", ev.get("D", 0)),
                ("⚠ stale", ev.get("stale_flags", 0))]
    body.append("<div class='bar'>%s</div>" % "".join(
        "<span class='pill'>%s <b>%s</b></span>" % (html.escape(str(k)),
                                                    html.escape(str(x)))
        for k, x in pills + ev_pills))

    if state.get("early_stop"):
        body.append("<blockquote><strong>Early stop:</strong> %s</blockquote>"
                    % html.escape(str(state["early_stop"])))

    body.append("<h2>Graph</h2>")
    body.append(graph_html(nodes))

    oq = state.get("open_questions") or []
    if oq:
        body.append("<h2>Open questions</h2><ul>%s</ul>"
                    % "".join("<li>%s</li>" % html.escape(str(q)) for q in oq))

    body.append("<h2>Evidence &amp; artifacts</h2>")
    files = sorted(f for f in os.listdir(folder) if f.endswith(".md"))
    if not files:
        body.append("<p class='sub'>No node files yet.</p>")
    for fn in files:
        with open(os.path.join(folder, fn), encoding="utf-8") as f:
            content = f.read()
        opened = fn.startswith(("05", "04", "07"))
        body.append("<details%s><summary>%s</summary>%s</details>"
                    % (" open" if opened else "", html.escape(fn), md(content)))

    log = state.get("log") or []
    if log:
        body.append("<h2>Run log</h2><ul>%s</ul>"
                    % "".join("<li>%s</li>" % html.escape(str(l)) for l in log))

    out = os.path.join(folder, "dashboard.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page("Diamond · %s" % slug, "".join(body)))
    print(out)
    if do_open:
        webbrowser.open("file://" + out)
    return out


def build_index(do_open=True):
    os.makedirs(IDEAS, exist_ok=True)
    rows = []
    for slug in sorted(os.listdir(IDEAS)):
        folder = os.path.join(IDEAS, slug)
        sp = os.path.join(folder, "state.json")
        if not os.path.isdir(folder) or not os.path.exists(sp):
            continue
        with open(sp) as f:
            s = json.load(f)
        v = (s.get("verdict") or "").lower()
        vlabel, _ = VERDICT.get(v, ("—", ""))
        rows.append(
            "<tr><td><a href='%s/dashboard.html'>%s</a></td><td>%s</td>"
            "<td>%s</td><td>%s</td><td>%s</td></tr>"
            % (html.escape(slug), html.escape(slug),
               html.escape(s.get("one_liner", "")),
               html.escape(s.get("stage", "")), vlabel,
               html.escape(s.get("updated", ""))))
    body = ["<h1>Diamond runs</h1><p class='sub'>Every idea this repo has put "
            "through the graph.</p>"]
    if rows:
        body.append("<table><thead><tr><th>Idea</th><th>One-liner</th>"
                    "<th>Stage</th><th>Verdict</th><th>Updated</th></tr></thead>"
                    "<tbody>%s</tbody></table>" % "".join(rows))
    else:
        body.append("<p>No runs yet. Start one with <code>/idea-diamond</code> "
                    "in Claude Code.</p>")
    out = os.path.join(IDEAS, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page("Diamond runs", "".join(body)))
    print(out)
    if do_open:
        webbrowser.open("file://" + out)
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--no-open"]
    opening = "--no-open" not in sys.argv
    if not args or args[0] == "--all":
        build_index(opening)
    else:
        build_idea(args[0], opening)
