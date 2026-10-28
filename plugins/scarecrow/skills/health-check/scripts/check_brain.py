#!/usr/bin/env python3
"""Check a second brain: structure (setup's build check) and upkeep (health-check's scheduled visit).

Canonical source: the health-check skill (scripts/check_brain.py). The setup skill ships a
byte-identical build-check copy, enforced by the repository's tests/test_vendored_script.py. Edit this file, then
copy it over the setup copy; never edit the copy.

Usage:
  check_brain.py ROOT                 all checks (M1-M22), exit 1 on any FAIL
  check_brain.py ROOT --structure     structure only (M1-M10): what a fresh brain must pass
  check_brain.py ROOT --record-raw    record checksums of raw/ and projects/*/received/ in raw/.manifest.json
  check_brain.py ROOT --adopt         adopt mode: skip checks that assume a fresh layout
  check_brain.py ROOT --json          machine-readable results (for the agent running the visit)

Thresholds (flag, then the rules file, then the default):
  --stale-days N      verified date older than N days       (rules file "older than <N> days", default 90)
  --pending-days N    verified: pending for more than N days (default 14)
  --status-days N     status.md "Last updated" older than N  (default 30)
  --question-days N   open question added more than N ago    (default 60)
  --rules-lines N     rules file longer than N lines         (default 150)
  --today YYYY-MM-DD  pretend today is this date (testing)

Standard library only.
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import urllib.parse
from pathlib import Path

REQUIRED = [
    "AGENTS.md",
    "CLAUDE.md",
    "raw",
    "wiki/index.md",
    "wiki/log.md",
    "_system/corrections.md",
    "_system/changelog.md",
]
SPECIAL_WIKI = {"index.md", "log.md"}
LINK_RE = re.compile(r"\[[^\]]*\]\((<[^>]+>|[^)\s]+)\)")
CODE_RE = re.compile(r"^(```|~~~).*?^\1[^\n]*$|`[^`\n]+`", re.M | re.S)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
DATE_LOG_RE = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})\]\s*([\w-]+)?", re.M)
HEALTH_RE = re.compile(r"Next health check:\s*(\d{4}-\d{2}-\d{2})")
STALE_RULE_RE = re.compile(r"older than\s*<?(\d+)>?\s*days", re.I)
LAST_UPDATED_RE = re.compile(r"Last updated:\s*(\d{4}-\d{2}-\d{2})", re.I)
MANIFEST = ".manifest.json"
SKIP_DIRS = {".git", ".obsidian", ".trash", "node_modules", "__pycache__", ".smart-env"}
HUB_FIELDS = ("status", "last-updated", "decision", "feedback", "log")
HUB_STATUS_ORDER = ("active", "paused", "done", "reference",      # project, event and reference hubs
                    "draft", "testing", "stable", "deprecated")   # optional set for prompt or skill hubs
HUB_STATUS = set(HUB_STATUS_ORDER)
DECISION_RE = re.compile(r"^\d{4}-\d{2}-\d{2}:")
DEFAULTS = {"stale_days": 90, "pending_days": 14, "status_days": 30, "question_days": 60, "rules_lines": 150}

results = []


def report(check, level, msg, path=None, **data):
    results.append({"check": check, "level": level, "msg": msg, "path": path, "data": data or None})


def read(path):
    """File text as UTF-8 whatever the platform locale; undecodable bytes and a leading BOM never stop a run."""
    return path.read_text(encoding="utf-8", errors="replace").removeprefix("\ufeff")


def iso(text):
    """A YYYY-MM-DD string as a date, or None when it is not a real calendar date."""
    try:
        return dt.date.fromisoformat(text)
    except (TypeError, ValueError):
        return None


def parse_date(text):
    m = DATE_RE.search(text or "")
    return iso(m.group(0)) if m else None


def load_manifest(root):
    """Recorded checksums: {} when none are recorded yet, None when the manifest cannot be read."""
    mpath = root / "raw" / MANIFEST
    if not mpath.exists():
        return {}
    try:
        data = json.loads(read(mpath))
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def link_paths(text):
    """(as written, decoded path) for each link outside code; <...> unwrapped, %-escapes decoded, URLs and anchors dropped."""
    out = []
    for target in LINK_RE.findall(CODE_RE.sub("", text)):
        bare = target[1:-1] if target.startswith("<") else target
        if re.match(r"^[a-z]+:", bare) or bare.startswith("#"):
            continue
        clean = urllib.parse.unquote(bare.split("#")[0])
        if clean:
            out.append((target, clean))
    return out


def rel(root, p):
    return str(p.relative_to(root))


def walk_md(root):
    out = []
    for p in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            continue
        out.append(p)
    return sorted(out)


def immutable(root, p):
    parts = p.relative_to(root).parts
    return parts[:1] == ("raw",) or "received" in parts


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def raw_files(root):
    """Immutable files: everything under raw/ plus every project's received/ folder."""
    dirs = [root / "raw"] + sorted(root.glob("projects/*/received"))
    out = []
    for d in dirs:
        if d.is_dir():
            out += [p for p in d.rglob("*") if p.is_file() and p.name not in (MANIFEST, "README.md")
                    and not p.name.startswith(".")]
    return sorted(out)


def record_raw(root):
    manifest = {rel(root, p): sha256(p) for p in raw_files(root)}
    mpath = root / "raw" / MANIFEST
    old = load_manifest(root)
    if old is None:
        print(f"Refusing to record: raw/{MANIFEST} is not a readable JSON object. Restore it from version history.")
        return 1
    if old:
        changed = [k for k in old if k in manifest and old[k] != manifest[k]]
        if changed:
            print("Refusing to record: these immutable files changed since they were recorded:")
            for k in changed:
                print("  " + k)
            print("Sources are immutable. Restore them, or record the fix in _system/corrections.md.")
            return 1
    old.update(manifest)
    mpath.write_text(json.dumps(old, indent=2, sort_keys=True) + "\n")
    print(f"Recorded {len(manifest)} immutable file(s) (raw/ and projects/*/received/) in raw/{MANIFEST}")
    return 0


def frontmatter(text):
    """Top-level keys of a YAML frontmatter block, as raw strings; nested lines kept under '_lines'."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fields = {"_lines": text[3:end].splitlines()}
    for line in fields["_lines"]:
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def verified_date(fm):
    """Latest verification date. Accepts a plain date, an OKF { by, at } mapping, or an OKF list of them."""
    raw = fm.get("verified")
    if raw is None:
        return None
    if raw.strip("'\"") == "pending":
        return "pending"
    if raw:
        return parse_date(raw)
    dates, inside = [], False
    for line in fm["_lines"]:
        if re.match(r"^verified:", line):
            inside = True
            continue
        if inside:
            if line and not line[0].isspace() and not line.startswith("-"):
                break
            d = parse_date(line)
            if d:
                dates.append(d)
    return max(dates) if dates else None


def check_links(root, path, text):
    for target, clean in link_paths(text):
        if not (path.parent / clean).resolve().exists():
            report("M6", "FAIL", f"broken link in {rel(root, path)}: {target}", rel(root, path))


def table_rows(text):
    """Cells of every markdown table row that is not a header separator."""
    rows = []
    for line in text.splitlines():
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows


def section(text, heading_re):
    m = re.search(rf"^#+\s*{heading_re}.*$", text, re.M | re.I)
    if not m:
        return None
    nxt = re.search(r"^#{1,6}\s", text[m.end():], re.M)
    return text[m.end(): m.end() + nxt.start()] if nxt else text[m.end():]


# ---------------------------------------------------------------- structure checks (M1-M10)

def unquote(value):
    return (value or "").strip().strip("\"'")


def hub_header(root, hub):
    """M9: the project hub's frontmatter header (status, last-updated, decision, feedback, log)."""
    r = rel(root, hub)
    text = read(hub)
    fm = frontmatter(text)
    if fm is None:
        report("M9", "WARN", f"{r} has no header ({', '.join(HUB_FIELDS)})", r)
        return
    missing = [f for f in HUB_FIELDS if f not in fm]
    if missing:
        report("M9", "WARN", f"{r} header lacks {', '.join(missing)}", r, missing=missing)
    status = unquote(fm.get("status"))
    if status and status not in HUB_STATUS:
        report("M9", "WARN", f"{r} status '{status}' is not one of {', '.join(HUB_STATUS_ORDER)}", r)
    if "last-updated" in fm and not parse_date(fm["last-updated"]):
        report("M9", "WARN", f"{r} last-updated is not a YYYY-MM-DD date", r)
    decision = unquote(fm.get("decision"))
    if decision and not DECISION_RE.match(decision):
        report("M9", "WARN", f"{r} decision does not start with 'YYYY-MM-DD:'", r)
    if status == "paused" and not re.search(r"^## Parked\b", text, re.M):
        report("M9", "WARN", f"{r} is paused but has no '## Parked' section (why it stopped, what restarts it)", r)
    log = unquote(fm.get("log"))
    if log and not log.startswith(("#", "[[")) and not (hub.parent / log).exists():
        report("M9", "WARN", f"{r} log points at {log}, which does not exist", r)


def structure(root, args, th):
    for r in REQUIRED:
        if not (root / r).exists():
            report("M1", "FAIL", f"missing {r}", r)
    log = root / "wiki" / "log.md"
    if log.exists() and not DATE_LOG_RE.search(read(log)):
        report("M1", "WARN", "wiki/log.md has no '## [YYYY-MM-DD] ...' entries yet", "wiki/log.md")

    claude = root / "CLAUDE.md"
    if claude.exists() and not re.search(r"^@AGENTS\.md\s*$", read(claude), re.M):
        report("M2", "FAIL", "CLAUDE.md has no '@AGENTS.md' line, so Claude Code will not load the rules", "CLAUDE.md")

    agents = root / "AGENTS.md"
    if agents.exists():
        text = read(agents)
        m = HEALTH_RE.search(text)
        if not m:
            report("M3", "FAIL", "AGENTS.md has no 'Next health check: YYYY-MM-DD' line", "AGENTS.md")
        elif not iso(m.group(1)):
            report("M3", "FAIL", f"AGENTS.md 'Next health check: {m.group(1)}' is not a real date", "AGENTS.md")
        if "raw/" not in text:
            report("M3", "WARN", "AGENTS.md never mentions raw/; the immutability rule may be missing", "AGENTS.md")
        check_links(root, agents, text)
        lines = text.count("\n") + 1
        if lines > th["rules_lines"]:
            report("M10", "WARN", f"AGENTS.md is {lines} lines (limit {th['rules_lines']}); it loads every session",
                   "AGENTS.md", lines=lines, limit=th["rules_lines"])

    wiki = root / "wiki"
    index_text = read(wiki / "index.md") if (wiki / "index.md").exists() else ""
    listed = {(wiki / clean).resolve() for _, clean in link_paths(index_text)}
    listed_stems = {Path(n.strip()).stem.lower() for n in WIKILINK_RE.findall(CODE_RE.sub("", index_text))}
    if wiki.is_dir():
        for page in sorted(wiki.rglob("*.md")):
            rw = str(page.relative_to(wiki))
            if rw in SPECIAL_WIKI:
                continue
            text = read(page)
            fm = frontmatter(text)
            path = f"wiki/{rw}"
            if fm is None:
                report("M4", "FAIL", f"{path} has no frontmatter", path)
            else:
                if not fm.get("type"):
                    report("M4", "FAIL", f"{path} frontmatter has no type", path)
                if "verified" not in fm:
                    report("M4", "WARN", f"{path} frontmatter has no verified date", path)
                elif args.structure and verified_date(fm) == "pending":
                    report("M4", "WARN", f"{path} is verified: pending (owner has not confirmed takeaways)", path)
                if "sources" not in fm:
                    report("M4", "WARN", f"{path} frontmatter has no sources", path)
            if page.resolve() not in listed and page.stem.lower() not in listed_stems \
                    and not re.search(rf"(?<![\w/-]){re.escape(rw)}(?![\w-])", index_text):
                report("M5", "FAIL", f"{path} is not listed in wiki/index.md", path)
            check_links(root, page, text)
        if index_text:
            check_links(root, wiki / "index.md", index_text)

    files = raw_files(root)
    manifest = load_manifest(root)
    if manifest is None:
        report("M7", "FAIL", f"raw/{MANIFEST} is not a readable JSON object; restore it from version history",
               f"raw/{MANIFEST}")
        manifest = {}
    for p in files:
        r = rel(root, p)
        if r not in manifest:
            report("M7", "WARN", f"{r} not recorded; run with --record-raw after ingest", r)
        elif manifest[r] != sha256(p):
            report("M7", "FAIL", f"{r} changed after it landed; sources and received files are immutable", r)
    for r in manifest:
        if not (root / r).exists():
            report("M7", "FAIL", f"{r} is in the manifest but missing", r)

    if not (root / "open-questions.md").exists():
        report("M8", "WARN", "no open-questions.md; unknown facts have nowhere to go but guesses", "open-questions.md")

    projects = root / "projects"
    if projects.is_dir() and not args.adopt:
        for proj in sorted(p for p in projects.iterdir() if p.is_dir()):
            for need in ("_index.md", "status.md"):
                if not (proj / need).exists():
                    report("M9", "FAIL", f"projects/{proj.name}/ has no {need}", f"projects/{proj.name}/")
            if (proj / "_index.md").exists():
                hub_header(root, proj / "_index.md")
            for f in proj.rglob("*.md"):
                check_links(root, f, read(f))
    elif not projects.exists() and not args.adopt:
        report("M9", "WARN", "no projects/ folder; work has nowhere to live beside its context", "projects/")


# ---------------------------------------------------------------- upkeep checks (M11-M22)

def overdue(root, today):
    agents = root / "AGENTS.md"
    m = HEALTH_RE.search(read(agents)) if agents.exists() else None
    if not m:
        return
    due = iso(m.group(1))
    if not due:
        return  # M3 reports the bad date
    if today > due:
        report("M11", "WARN", f"health check overdue since {due} ({(today - due).days} days)", "AGENTS.md",
               due=str(due), days_overdue=(today - due).days)
    else:
        report("M11", "INFO", f"health check due {due}; running early is fine", "AGENTS.md", due=str(due))


def ingest_dates(root):
    """Earliest log date that names each page (for pending age)."""
    out = {}
    log = root / "wiki" / "log.md"
    if not log.exists():
        return out
    entries = re.split(r"^(?=## \[)", read(log), flags=re.M)
    for e in entries:
        m = DATE_LOG_RE.match(e)
        if not m:
            continue
        d = iso(m.group(1))
        if not d:
            continue
        for name in re.findall(r"[\w./-]+\.md", e):
            stem = Path(name).stem
            out[stem] = min(out.get(stem, d), d)
    return out


def freshness(root, today, th):
    wiki = root / "wiki"
    if not wiki.is_dir():
        return
    first_seen = ingest_dates(root)
    pending_total = 0
    for page in sorted(wiki.rglob("*.md")):
        rw = str(page.relative_to(wiki))
        if rw in SPECIAL_WIKI:
            continue
        fm = frontmatter(read(page))
        if not fm:
            continue
        path = f"wiki/{rw}"
        v = verified_date(fm)
        stale_after = parse_date(fm.get("stale_after", ""))
        if v == "pending":
            pending_total += 1
            since = first_seen.get(page.stem) or dt.date.fromtimestamp(page.stat().st_mtime)
            age = (today - since).days
            level = "WARN" if age > th["pending_days"] else "INFO"
            report("M13", level, f"{path} verified: pending for {age} days (limit {th['pending_days']})", path,
                   pending_since=str(since), age_days=age)
            continue
        if stale_after and today >= stale_after:
            report("M12", "WARN", f"{path} is past its stale_after date {stale_after}", path,
                   verified=str(v) if v else None, stale_after=str(stale_after))
        elif v and not stale_after and (today - v).days > th["stale_days"]:
            report("M12", "WARN", f"{path} verified {v} ({(today - v).days} days ago; limit {th['stale_days']})",
                   path, verified=str(v), age_days=(today - v).days)


def link_targets(root, src, text):
    """Files a note links to, by markdown link or [[wikilink]] (wikilinks resolved by filename stem)."""
    out = set()
    for _, clean in link_paths(text):
        out.add((src.parent / clean).resolve())
    for name in WIKILINK_RE.findall(CODE_RE.sub("", text)):
        out.add(("stem", Path(name.strip()).stem.lower()))
    return out


def orphans(root):
    wiki = root / "wiki"
    if not wiki.is_dir():
        return
    # Capsule pattern pages (*patterns.md) are fed by capsules, not linked from synthesis, so they are exempt.
    pages = [p for p in wiki.rglob("*.md") if str(p.relative_to(wiki)) not in SPECIAL_WIKI
             and not p.name.endswith("patterns.md")]
    inbound = {p.resolve(): 0 for p in pages}
    by_stem = {p.stem.lower(): p.resolve() for p in pages}
    for src in walk_md(root):
        if immutable(root, src) or src.parent == wiki and src.name in SPECIAL_WIKI:
            continue
        for t in link_targets(root, src, read(src)):
            target = by_stem.get(t[1]) if isinstance(t, tuple) else t
            if target in inbound and target != src.resolve():
                inbound[target] += 1
    for p, n in sorted(inbound.items()):
        if n == 0:
            r = rel(root, p)
            report("M14", "WARN", f"{r} has no inbound links besides the index", r)


def status_age(root, today, th):
    projects = root / "projects"
    if not projects.is_dir():
        return
    for proj in sorted(p for p in projects.iterdir() if p.is_dir()):
        s = proj / "status.md"
        if not s.exists():
            continue
        path = f"projects/{proj.name}/status.md"
        m = LAST_UPDATED_RE.search(read(s))
        if not m:
            report("M15", "WARN", f"{path} has no 'Last updated: YYYY-MM-DD' line", path)
            continue
        last = iso(m.group(1))
        if not last:
            report("M15", "WARN", f"{path} 'Last updated: {m.group(1)}' is not a real date", path)
            continue
        # A file counts as newer only when it changed on a later day than status.md itself was last written.
        # Clones, syncs, and copies rewrite every mtime at once, so they never flag the whole project.
        since = max(last, dt.date.fromtimestamp(s.stat().st_mtime))
        newer = [rel(root, f) for f in proj.rglob("*") if f.is_file() and f != s and not f.name.startswith(".")
                 and dt.date.fromtimestamp(f.stat().st_mtime) > since]
        age = (today - last).days
        if age > th["status_days"] or newer:
            why = f"last updated {last} ({age} days; limit {th['status_days']})"
            if newer:
                why += f"; {len(newer)} file(s) in the project changed after that"
            report("M15", "WARN", f"{path} {why}", path, last_updated=str(last), age_days=age, newer_files=newer)


def hub_lag(root):
    """M22: a hub header confirmed before its project's status.md last changed."""
    projects = root / "projects"
    if not projects.is_dir():
        return
    for proj in sorted(p for p in projects.iterdir() if p.is_dir()):
        hub, s = proj / "_index.md", proj / "status.md"
        if not (hub.exists() and s.exists()):
            continue
        fm = frontmatter(read(hub)) or {}
        confirmed = parse_date(fm.get("last-updated"))
        m = LAST_UPDATED_RE.search(read(s))
        if not (confirmed and m):
            continue
        updated = iso(m.group(1))
        if updated and updated > confirmed:
            path = f"projects/{proj.name}/_index.md"
            report("M22", "WARN", f"{path} header confirmed {confirmed}, but status.md was updated {updated}; "
                   "check whether decision and feedback still hold, then bump last-updated", path,
                   header_date=str(confirmed), status_date=str(updated))


def open_questions(root, today, th):
    oq = root / "open-questions.md"
    if not oq.exists():
        return
    for cells in table_rows(read(oq)):
        d = parse_date(cells[0]) if cells else None
        if not d:
            continue
        age = (today - d).days
        if age > th["question_days"]:
            q = cells[2] if len(cells) > 2 else " | ".join(cells[1:])
            report("M16", "WARN", f"open question added {d} ({age} days): {q}", "open-questions.md",
                   added=str(d), age_days=age, row=cells)


def folder_drift(root, adopt):
    agents = root / "AGENTS.md"
    if not agents.exists():
        return
    text = read(agents)
    body = section(text, r"(folder map|folders|layout|structure)")
    if body is None:
        report("M17", "INFO", "AGENTS.md has no folder map section; drift check skipped", "AGENTS.md")
        return
    mapped = set()
    for cells in table_rows(body):
        for path in re.findall(r"`([^`]+)`", cells[0] if cells else ""):
            mapped.add(path.strip().rstrip("/"))
    top_mapped = {p.split("/")[0] for p in mapped}
    real_top = {p.name for p in root.iterdir() if p.is_dir() and p.name not in SKIP_DIRS
                and not p.name.startswith(".")}
    for name in sorted(real_top - top_mapped):
        report("M17", "WARN", f"folder {name}/ exists but is not in the AGENTS.md folder map", f"{name}/")
    for p in sorted(mapped):
        if "<" in p or "*" in p or "." in Path(p).name:
            continue
        if not (root / p).exists():
            report("M17", "WARN", f"folder map lists {p}/ but it does not exist", f"{p}/")
    # One level down: when the map names concrete children of a folder (projects/acme/), every real child needs a row.
    parents = {}
    for p in mapped:
        parts = p.split("/")
        if len(parts) == 2:
            parents.setdefault(parts[0], set()).add(parts[1])
    for parent, kids in sorted(parents.items()):
        if any("<" in k or "*" in k for k in kids) or not (root / parent).is_dir():
            continue
        real = {c.name for c in (root / parent).iterdir() if c.is_dir() and not c.name.startswith(".")}
        for name in sorted(real - kids):
            report("M17", "WARN", f"{parent}/{name}/ exists but has no row in the folder map", f"{parent}/{name}/")


def corrections_file(root, override):
    if override:
        return root / override
    for c in ("_system/corrections.md", "_system/errata.md"):
        if (root / c).exists():
            return root / c
    return None


def corrections_prefilter(root, override):
    cfile = corrections_file(root, override)
    if not cfile:
        return
    rows = table_rows(read(cfile))
    wrongs = []
    for cells in rows[1:] if rows and not parse_date(rows[0][0]) else rows:
        if len(cells) < 3 or not cells[1] or cells[1].startswith("<"):
            continue
        wrongs.append(cells[1].strip("`\"' "))
    if not wrongs:
        return
    targets = [p for p in walk_md(root) if not immutable(root, p) and p.parts[len(root.parts)] != "_system"]
    for w in wrongs:
        if len(w) < 4:
            continue
        needle = w.lower()
        for p in targets:
            for i, line in enumerate(read(p).splitlines(), 1):
                if needle in line.lower():
                    r = rel(root, p)
                    report("M18", "WARN", f"{r}:{i} contains a known-wrong statement: {w}", r, line=i, wrong=w)


def uncompiled(root):
    """Sources in raw/ that no wiki page lists in its sources and the log never names: landed, never ingested."""
    raw = root / "raw"
    wiki = root / "wiki"
    if not raw.is_dir():
        return
    cited = ""
    if wiki.is_dir():
        for page in wiki.rglob("*.md"):
            if page.name == "log.md":
                cited += read(page)
                continue
            fm = frontmatter(read(page))
            if fm:
                cited += "\n".join(fm["_lines"])
    for p in sorted(raw.rglob("*")):
        if not p.is_file() or p.name in (MANIFEST, "README.md") or p.name.startswith("."):
            continue
        if p.name not in cited:
            r = rel(root, p)
            report("M20", "WARN", f"{r} is not cited by any wiki page and not in the log; it may never have been ingested", r)


def capsules(root):
    for p in walk_md(root):
        if not p.name.endswith("-capsule.md") or immutable(root, p):
            continue
        r = rel(root, p)
        text = read(p)
        body = section(text, r"revision triggers")
        fm = frontmatter(text) or {}
        written = parse_date(fm.get("date", "")) or parse_date(p.name)
        if body is None:
            report("M19", "WARN", f"{r} has no 'Revision triggers' section", r)
            continue
        triggers = [re.sub(r"^[-*]\s+|^\d+\.\s+", "", ln.strip()) for ln in body.splitlines()
                    if re.match(r"^\s*([-*]|\d+\.)\s+", ln)]
        report("M19", "INFO", f"{r}: {len(triggers)} revision trigger(s)", r,
               written=str(written) if written else None, triggers=triggers)


SECRET_SHAPES = [
    ("AWS access key id", r"(?<!AWSAccessKeyId=)\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("GitHub token", r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b|\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    ("API key (sk-)", r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{24,}"),
    ("Slack token", r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    ("Stripe live key", r"\b[rs]k_live_[A-Za-z0-9]{20,}"),
    ("Google API key", r"\bAIza[0-9A-Za-z_-]{35}\b"),
    ("private key", r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----"),
    ("JWT", r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
]
SECRET_RES = [(kind, re.compile(rx)) for kind, rx in SECRET_SHAPES]
SECRET_SUFFIXES = {".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".env", ".toml", ".ini", ".cfg"}


def secrets(root):
    """Known key shapes in text files. Reports a fingerprint (kind, first 4 characters, length), never the value."""
    for p in sorted(root.rglob("*")):
        if not p.is_file() or any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            continue
        if p.suffix.lower() not in SECRET_SUFFIXES and not p.name.startswith(".env"):
            continue
        try:
            if p.stat().st_size > 2_000_000:
                continue
            lines = read(p).splitlines()
        except OSError:
            continue
        r = rel(root, p)
        for n, line in enumerate(lines, 1):
            for kind, rx in SECRET_RES:
                for m in rx.finditer(line):
                    v = m.group(0)
                    report("M21", "WARN", f"{r}:{n} holds a secret-shaped value: {kind} ({v[:4]}..., {len(v)} chars)",
                           r, line=n, kind=kind)


# ---------------------------------------------------------------- main

def thresholds(root, args):
    th = dict(DEFAULTS)
    agents = root / "AGENTS.md"
    if agents.exists():
        body = section(read(agents), r"health check") or ""
        m = STALE_RULE_RE.search(body)
        if m:
            th["stale_days"] = int(m.group(1))
    for k in DEFAULTS:
        v = getattr(args, k)
        if v is not None:
            th[k] = v
    return th


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--record-raw", action="store_true")
    ap.add_argument("--adopt", action="store_true")
    ap.add_argument("--structure", action="store_true", help="structure checks only (M1-M10)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--corrections", help="corrections register path relative to ROOT")
    ap.add_argument("--today")
    for k in DEFAULTS:
        ap.add_argument("--" + k.replace("_", "-"), dest=k, type=int)
    args = ap.parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"FAIL  {root} is not a folder")
        return 1
    if args.record_raw:
        return record_raw(root)
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    th = thresholds(root, args)

    structure(root, args, th)
    if not args.structure:
        overdue(root, today)
        freshness(root, today, th)
        orphans(root)
        status_age(root, today, th)
        hub_lag(root)
        open_questions(root, today, th)
        folder_drift(root, args.adopt)
        corrections_prefilter(root, args.corrections)
        capsules(root)
        uncompiled(root)
        secrets(root)

    fails = sum(r["level"] == "FAIL" for r in results)
    warns = sum(r["level"] == "WARN" for r in results)
    if args.json:
        print(json.dumps({"root": str(root), "today": str(today),
                          "mode": "structure" if args.structure else "full", "adopt": args.adopt,
                          "thresholds": th, "summary": {"fail": fails, "warn": warns}, "results": results},
                         indent=2))
    else:
        order = {"FAIL": 0, "WARN": 1, "INFO": 2}
        for r in sorted(results, key=lambda r: (order[r["level"]], int(r["check"][1:]))):
            print(f"{r['level']:<5} [{r['check']}] {r['msg']}")
        print(f"\n{'PASS' if not fails else 'FAIL'}: {fails} fail, {warns} warn")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
