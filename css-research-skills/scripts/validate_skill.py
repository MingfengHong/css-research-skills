#!/usr/bin/env python3
"""Validate the css-research-skills package with no third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_REFERENCES = {
    "references/causal_inference.md": ("group-time ATT", "Sun and Abraham"),
    "references/nlp_text_analysis.md": ("sample splitting", "construct"),
    "references/abm_simulation.md": ("shuffle_do", "ODD"),
    "references/network_analysis.md": ("Leiden", "maximum likelihood"),
    "references/reproducibility_and_ethics.md": (
        "Data-availability statement",
        "stakeholders",
    ),
    "references/packages.md": ("Version-first workflow",),
    "references/source_guide.md": ("Evidence hierarchy",),
}


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must begin with YAML frontmatter delimited by ---")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("SKILL.md frontmatter has no closing ---") from exc

    fields: dict[str, str] = {}
    i = 1
    while i < end:
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$", lines[i])
        if not match:
            i += 1
            continue
        key, raw = match.group(1), (match.group(2) or "").strip()
        if raw in {">", ">-", "|", "|-"}:
            values: list[str] = []
            i += 1
            while i < end and (not lines[i].strip() or lines[i][0].isspace()):
                values.append(lines[i].strip())
                i += 1
            fields[key] = " ".join(value for value in values if value)
            continue
        fields[key] = raw.strip('"\'')
        i += 1
    return fields, "\n".join(lines[end + 1 :])


def validate(skill_root: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    metrics: dict[str, object] = {}

    skill_root = skill_root.resolve()
    skill_md = skill_root / "SKILL.md"
    if not skill_md.is_file():
        return {
            "ok": False,
            "errors": [f"Missing required file: {skill_md}"],
            "warnings": [],
            "metrics": {},
        }

    try:
        skill_text = skill_md.read_text(encoding="utf-8")
        fields, body = parse_frontmatter(skill_text)
    except (OSError, UnicodeError, ValueError) as exc:
        return {
            "ok": False,
            "errors": [str(exc)],
            "warnings": [],
            "metrics": {},
        }

    name = fields.get("name", "")
    description = fields.get("description", "")
    compatibility = fields.get("compatibility", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append("Frontmatter name must contain only lowercase letters, numbers, and single hyphens")
    if name != skill_root.name:
        errors.append(f"Frontmatter name {name!r} does not match directory {skill_root.name!r}")
    if not 1 <= len(name) <= 64:
        errors.append(f"Frontmatter name length must be 1-64 characters; found {len(name)}")
    if not 1 <= len(description) <= 1024:
        errors.append(f"Description length must be 1-1024 characters; found {len(description)}")
    if compatibility and not 1 <= len(compatibility) <= 500:
        errors.append(f"Compatibility length must be 1-500 characters; found {len(compatibility)}")

    line_count = len(skill_text.splitlines())
    if line_count > 500:
        errors.append(f"SKILL.md exceeds the recommended 500 lines: {line_count}")
    metrics.update(
        {
            "skill_root": str(skill_root),
            "skill_lines": line_count,
            "description_characters": len(description),
        }
    )

    for rel_path, required_phrases in REQUIRED_REFERENCES.items():
        path = skill_root / rel_path
        if not path.is_file():
            errors.append(f"Missing routed reference: {rel_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in required_phrases:
            if phrase.casefold() not in text.casefold():
                errors.append(f"{rel_path} is missing required concept: {phrase}")

    relative_links = re.findall(
        r"\]\(((?:references|assets|scripts|evals)/[^)#]+)(?:#[^)]+)?\)", body
    )
    for rel_path in relative_links:
        if not (skill_root / rel_path).exists():
            errors.append(f"Broken relative link in SKILL.md: {rel_path}")

    text_files = sorted(skill_root.rglob("*.md"))
    text_files.extend(sorted(skill_root.rglob("*.json")))
    for path in text_files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError as exc:
            errors.append(f"Not valid UTF-8: {path.relative_to(skill_root)} ({exc})")
            continue
        if "\ufffd" in text:
            errors.append(f"Unicode replacement character found in {path.relative_to(skill_root)}")
        if re.search(r"(?i)(?:[A-Z]:[\\/](?:Users|Documents|Downloads)[\\/]|/home/[^/]+/)", text):
            errors.append(f"Machine-specific absolute path found in {path.relative_to(skill_root)}")

    version_sensitive = "\n".join(
        (skill_root / rel).read_text(encoding="utf-8")
        for rel in ("references/abm_simulation.md", "references/packages.md")
    )
    for pattern in (r"from\s+mesa\.time\s+import", r"RandomActivation\s*\(", r"SimultaneousActivation\s*\("):
        if re.search(pattern, version_sensitive):
            errors.append(f"Deprecated Mesa code pattern found: {pattern}")

    evals_path = skill_root / "evals" / "evals.json"
    if not evals_path.is_file():
        errors.append("Missing evals/evals.json")
    else:
        try:
            eval_data = json.loads(evals_path.read_text(encoding="utf-8"))
            evals = eval_data.get("evals", [])
            if eval_data.get("skill_name") != name:
                errors.append("evals/evals.json skill_name does not match frontmatter name")
            if not 2 <= len(evals) <= 6:
                warnings.append(f"Expected a focused initial set of 2-6 evals; found {len(evals)}")
            ids = [item.get("id") for item in evals]
            if len(ids) != len(set(ids)):
                errors.append("Eval IDs must be unique")
            for item in evals:
                eval_id = item.get("id", "?")
                for key in ("prompt", "expected_output", "files", "expectations"):
                    if key not in item:
                        errors.append(f"Eval {eval_id} is missing {key}")
                if not isinstance(item.get("expectations", []), list) or not item.get("expectations"):
                    errors.append(f"Eval {eval_id} must have at least one objective expectation")
            metrics["eval_count"] = len(evals)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid evals/evals.json: {exc}")

    trigger_path = skill_root / "evals" / "trigger_evals.json"
    if trigger_path.is_file():
        try:
            triggers = json.loads(trigger_path.read_text(encoding="utf-8"))
            if len(triggers) < 16:
                warnings.append(f"Trigger eval set is small: {len(triggers)} cases")
            for index, item in enumerate(triggers, 1):
                if not isinstance(item.get("query"), str) or not isinstance(item.get("should_trigger"), bool):
                    errors.append(f"Trigger eval {index} must contain string query and boolean should_trigger")
            metrics["trigger_eval_count"] = len(triggers)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid evals/trigger_evals.json: {exc}")

    metrics["markdown_files"] = len(list(skill_root.rglob("*.md")))
    return {"ok": not errors, "errors": errors, "warnings": warnings, "metrics": metrics}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate structure, references, UTF-8, and eval files for css-research-skills."
    )
    parser.add_argument(
        "skill_root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Skill directory (default: parent of this script directory)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return a failing exit code when warnings are present",
    )
    args = parser.parse_args()
    result = validate(args.skill_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] and (not args.strict or not result["warnings"]) else 1


if __name__ == "__main__":
    sys.exit(main())
