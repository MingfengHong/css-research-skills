#!/usr/bin/env python3
"""Create label-blind grading inputs for the comprehensive benchmark."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


MAPPINGS = (
    {"candidate-A": "v2_0_0", "candidate-B": "no_skill", "candidate-C": "v1_0_0"},
    {"candidate-A": "v1_0_0", "candidate-B": "v2_0_0", "candidate-C": "no_skill"},
    {"candidate-A": "no_skill", "candidate-B": "v1_0_0", "candidate-C": "v2_0_0"},
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evals", type=Path, default=Path("benchmarks/comprehensive-evals.json"))
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path("css-research-skills-workspace/iteration-3"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = json.loads(args.evals.read_text(encoding="utf-8"))
    raw_root = args.workspace / "raw"
    blind_root = args.workspace / "blind"
    mapping_output: dict[str, dict[str, str]] = {}

    for index, evaluation in enumerate(data["evals"]):
        eval_id = int(evaluation["id"])
        eval_dir = blind_root / f"eval-{eval_id}"
        eval_dir.mkdir(parents=True, exist_ok=True)
        metadata = {
            "eval_id": eval_id,
            "eval_name": evaluation["name"],
            "domain": evaluation["domain"],
            "prompt": evaluation["prompt"],
            "expectations": evaluation["expectations"],
        }
        (eval_dir / "eval_metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        mapping = MAPPINGS[index % len(MAPPINGS)]
        mapping_output[str(eval_id)] = mapping
        for candidate, condition in mapping.items():
            source = raw_root / f"eval-{eval_id}" / condition / "response.md"
            if not source.is_file():
                raise FileNotFoundError(source)
            run_dir = eval_dir / candidate / "run-1"
            output_dir = run_dir / "outputs"
            output_dir.mkdir(parents=True, exist_ok=True)
            target = output_dir / "response.md"
            shutil.copyfile(source, target)
            response = target.read_text(encoding="utf-8")
            transcript = f"# Prompt\n\n{evaluation['prompt']}\n\n# Final response\n\n{response}"
            (run_dir / "transcript.md").write_text(transcript, encoding="utf-8")
            metrics = {
                "total_tool_calls": 0,
                "total_steps": 1,
                "errors_encountered": 0,
                "output_chars": len(response),
                "transcript_chars": len(transcript),
            }
            (output_dir / "metrics.json").write_text(
                json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            (run_dir / "timing.json").write_text(
                json.dumps(
                    {
                        "total_tokens": 0,
                        "total_duration_seconds": 0,
                        "note": "Exact telemetry unavailable; excluded from the benchmark.",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

    private_mapping = {
        "benchmark_id": data["benchmark_id"],
        "warning": "Do not expose this mapping to graders before grading is complete.",
        "mapping": mapping_output,
    }
    (args.workspace / "private-mapping.json").write_text(
        json.dumps(private_mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Prepared {len(data['evals'])} blinded evaluations in {blind_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
