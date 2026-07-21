#!/usr/bin/env python3
"""Aggregate blinded comprehensive-benchmark grades into reviewed community data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CONDITIONS = {
    "no_skill": {
        "label": "No Skill",
        "version": None,
        "color": "#E4E2DA",
        "edge_color": "#8E8D87",
        "hatch": "..",
    },
    "v1_0_0": {
        "label": "Skill 1.0.0",
        "version": "1.0.0",
        "color": "#C6D0B4",
        "edge_color": "#7A8B64",
        "hatch": "//",
    },
    "v2_0_0": {
        "label": "Skill 2.0.0",
        "version": "2.0.0",
        "color": "#7A8B64",
        "edge_color": "#3E4935",
        "hatch": "",
    },
}

TASK_LABELS = {
    "staggered-adoption-did": "Staggered\nDiD",
    "cross-language-iv-audit": "Cross-language\nIV",
    "multilingual-text-causal-measurement": "Text → causal\nmeasurement",
    "imbalanced-text-classification-audit": "Text\nclassification",
    "large-spatial-abm": "Spatial\nABM",
    "large-bipartite-network": "Bipartite\nnetwork",
    "valued-ergm-with-missing-dyads": "Valued\nERGM",
    "restricted-data-replication-package": "Replication\npackage",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evals", type=Path, default=Path("benchmarks/comprehensive-evals.json"))
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path("css-research-skills-workspace/iteration-3"),
    )
    parser.add_argument("--output", type=Path, default=Path("benchmarks/benchmark-results.json"))
    parser.add_argument("--markdown", type=Path, default=Path("benchmarks/benchmark-results.md"))
    return parser.parse_args()


def rate(passed: int, total: int) -> float:
    return round(100 * passed / total, 1) if total else 0.0


def main() -> int:
    args = parse_args()
    eval_data = json.loads(args.evals.read_text(encoding="utf-8"))
    mapping_data = json.loads((args.workspace / "private-mapping.json").read_text(encoding="utf-8"))
    mappings = mapping_data["mapping"]

    totals = {condition: {"passed": 0, "total": 0} for condition in CONDITIONS}
    dimension_totals = {
        dimension["id"]: {
            condition: {"passed": 0, "total": 0} for condition in CONDITIONS
        }
        for dimension in eval_data["dimensions"]
    }
    task_results = []

    for evaluation in eval_data["evals"]:
        eval_id = str(evaluation["id"])
        candidate_to_condition = mappings[eval_id]
        expected_texts = [item["text"] for item in evaluation["expectations"]]
        dimensions = [item["dimension"] for item in evaluation["expectations"]]
        results = {}

        for candidate, condition in candidate_to_condition.items():
            grading_path = (
                args.workspace
                / "blind"
                / f"eval-{eval_id}"
                / candidate
                / "run-1"
                / "grading.json"
            )
            grading = json.loads(grading_path.read_text(encoding="utf-8"))
            graded = grading["expectations"]
            if [item["text"] for item in graded] != expected_texts:
                raise ValueError(f"Expectation mismatch in {grading_path}")
            passed = sum(bool(item["passed"]) for item in graded)
            total = len(graded)
            results[condition] = {"passed": passed, "total": total, "pass_rate": rate(passed, total)}
            totals[condition]["passed"] += passed
            totals[condition]["total"] += total
            for dimension, item in zip(dimensions, graded):
                dimension_totals[dimension][condition]["passed"] += int(bool(item["passed"]))
                dimension_totals[dimension][condition]["total"] += 1

        task_results.append(
            {
                "id": evaluation["id"],
                "name": evaluation["name"],
                "label": TASK_LABELS[evaluation["name"]],
                "domain": evaluation["domain"],
                "checks": len(evaluation["expectations"]),
                "results": results,
            }
        )

    dimensions_output = []
    for dimension in eval_data["dimensions"]:
        results = {}
        for condition in CONDITIONS:
            values = dimension_totals[dimension["id"]][condition]
            results[condition] = {
                **values,
                "pass_rate": rate(values["passed"], values["total"]),
            }
        dimensions_output.append({**dimension, "results": results})

    conditions_output = []
    for condition, presentation in CONDITIONS.items():
        values = totals[condition]
        conditions_output.append(
            {
                "id": condition,
                **presentation,
                "overall_passed": values["passed"],
                "overall_total": values["total"],
                "overall_pass_rate": rate(values["passed"], values["total"]),
            }
        )

    output = {
        "benchmark_id": eval_data["benchmark_id"],
        "benchmark_date": "July 21, 2026",
        "skill": "css-research-skills",
        "method": {
            "tasks": len(task_results),
            "dimensions": len(dimensions_output),
            "checks_per_task": 6,
            "total_checks_per_condition": len(task_results) * 6,
            "runs_per_condition_task": 1,
            "conditions_executed_concurrently": True,
            "grading": "Candidate labels were rotated by task; two independent graders applied the same frozen binary rubric without access to the version mapping.",
            "timing_and_token_comparison": "excluded because exact telemetry was unavailable",
            "status": "pilot",
        },
        "conditions": conditions_output,
        "tasks": task_results,
        "dimensions": dimensions_output,
        "provenance": {
            "prompts": "benchmarks/comprehensive-prompts.json",
            "eval_definition": "benchmarks/comprehensive-evals.json",
            "raw_runs": "css-research-skills-workspace/iteration-3/raw",
            "blinded_grades": "css-research-skills-workspace/iteration-3/blind",
            "figure_script": "scripts/render_benchmark.py",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    headers = ["Condition", *[task["label"].replace("\n", " ") for task in task_results], "Overall"]
    rows = []
    for condition in conditions_output:
        row = [condition["label"]]
        for task in task_results:
            result = task["results"][condition["id"]]
            row.append(f"{result['passed']}/{result['total']}")
        row.append(
            f"{condition['overall_passed']}/{condition['overall_total']} "
            f"({condition['overall_pass_rate']:.1f}%)"
        )
        rows.append(row)
    lines = [
        "# Comprehensive benchmark results",
        "",
        "Pilot: eight tasks, six frozen dimensions per task, one run per condition/task.",
        "",
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---", *(["---:"] * (len(headers) - 1))]) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    lines.extend(
        [
            "",
            "> Single-run pilot values are coverage estimates, not uncertainty intervals. "
            "Timing and token comparisons are excluded.",
        ]
    )
    args.markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"Wrote {args.markdown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
