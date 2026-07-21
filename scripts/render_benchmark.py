#!/usr/bin/env python3
"""Render the reviewed comprehensive benchmark as a README-ready PNG.

The renderer intentionally depends only on Pillow. Bars start at a true zero
baseline, carry direct value labels, and use both color and texture so the
three conditions remain distinguishable in grayscale.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


INK = "#20251E"
MUTED = "#626A5D"
GRID = "#DDE1D8"
PAPER = "#FCFCF9"
FRAME = "#9CA496"
FONT_REGULAR = Path("C:/Windows/Fonts/georgia.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/georgiab.ttf")
DIMENSION_LABELS = {
    "research_framing": "Research\nframing",
    "method_fit": "Method\nfit",
    "implementation": "Implemen-\ntation",
    "diagnostics": "Diagnostics",
    "reproducibility": "Reproduc-\nibility",
    "responsible_claims": "Responsible\nclaims",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("benchmarks/benchmark-results.json"),
        help="Reviewed aggregate JSON",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("assets/benchmark-comparison.png"),
        help="PNG output path",
    )
    return parser.parse_args()


def load_results(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if len(data.get("conditions", [])) != 3:
        raise ValueError("Expected exactly three benchmark conditions")
    if not data.get("tasks") or not data.get("dimensions"):
        raise ValueError("Tasks and dimensions are required")
    condition_ids = {condition["id"] for condition in data["conditions"]}
    for collection in (data["tasks"], data["dimensions"]):
        for item in collection:
            if set(item["results"]) != condition_ids:
                raise ValueError(f"Condition mismatch in {item.get('name', item.get('id'))}")
            for result in item["results"].values():
                if not 0 <= result["pass_rate"] <= 100:
                    raise ValueError("Pass rates must be in 0..100")
    return data


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold else FONT_REGULAR
    if not path.exists():
        raise FileNotFoundError(f"Required font not found: {path}")
    return ImageFont.truetype(str(path), size=size)


def centered_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    *,
    typeface: ImageFont.FreeTypeFont,
    fill: str,
    spacing: int = 4,
) -> None:
    box = draw.multiline_textbbox((0, 0), text, font=typeface, spacing=spacing, align="center")
    width = box[2] - box[0]
    height = box[3] - box[1]
    draw.multiline_text(
        (xy[0] - width / 2, xy[1] - height / 2 - box[1]),
        text,
        font=typeface,
        fill=fill,
        spacing=spacing,
        align="center",
    )


def textured_bar(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    *,
    fill: str,
    edge: str,
    hatch: str,
) -> None:
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=fill, outline=edge, width=2)
    if hatch == "..":
        for y in range(y0 + 8, y1, 13):
            offset = 6 if ((y - y0) // 13) % 2 else 0
            for x in range(x0 + 7 + offset, x1, 13):
                draw.ellipse((x - 1, y - 1, x + 1, y + 1), fill=edge)
    elif hatch == "//":
        step = 15
        for start in range(x0 - (y1 - y0), x1, step):
            points = []
            for x, y in ((start, y1), (start + (y1 - y0), y0)):
                points.append((max(x0, min(x1, x)), max(y0, min(y1, y))))
            # Clip the diagonal analytically to the rectangle.
            line_x0 = max(x0, start)
            line_y0 = y1 - (line_x0 - start)
            line_x1 = min(x1, start + (y1 - y0))
            line_y1 = y1 - (line_x1 - start)
            if line_x0 <= line_x1 and y0 <= line_y0 <= y1 and y0 <= line_y1 <= y1:
                draw.line((line_x0, line_y0, line_x1, line_y1), fill=edge, width=1)
        draw.rectangle(box, outline=edge, width=2)


def draw_panel(
    draw: ImageDraw.ImageDraw,
    *,
    box: tuple[int, int, int, int],
    title: str,
    labels: list[str],
    rates: dict[str, list[float]],
    conditions: list[dict],
    show_y_labels: bool,
) -> None:
    left, top, right, bottom = box
    plot_top = top + 54
    plot_bottom = bottom - 105
    plot_left = left + (70 if show_y_labels else 25)
    plot_right = right - 20
    plot_height = plot_bottom - plot_top

    draw.text((left, top), title, font=font(26, bold=True), fill=INK)
    for tick in range(0, 101, 20):
        y = round(plot_bottom - (tick / 100) * plot_height)
        draw.line((plot_left, y, plot_right, y), fill=GRID, width=2)
        if show_y_labels:
            tick_text = str(tick)
            tick_box = draw.textbbox((0, 0), tick_text, font=font(17))
            draw.text((plot_left - 15 - (tick_box[2] - tick_box[0]), y - 10), tick_text, font=font(17), fill=MUTED)

    draw.rectangle((plot_left, plot_top, plot_right, plot_bottom), outline=FRAME, width=2)
    group_width = (plot_right - plot_left) / len(labels)
    bar_width = min(29, int(group_width * 0.22))
    gap = max(3, int(bar_width * 0.13))
    cluster_width = 3 * bar_width + 2 * gap

    for group_index, label in enumerate(labels):
        center = plot_left + group_width * (group_index + 0.5)
        cluster_left = center - cluster_width / 2
        prior_values: list[float] = []
        for condition_index, condition in enumerate(conditions):
            value = rates[condition["id"]][group_index]
            x0 = round(cluster_left + condition_index * (bar_width + gap))
            x1 = x0 + bar_width
            # Reserve ten percentage points of headroom for direct labels.
            y0 = round(plot_bottom - (value / 110) * plot_height)
            textured_bar(
                draw,
                (x0, y0, x1, plot_bottom),
                fill=condition["color"],
                edge=condition["edge_color"],
                hatch=condition.get("hatch", ""),
            )
            label_font = font(15, bold=value >= 99.9)
            value_text = f"{value:.1f}"
            value_box = draw.textbbox((0, 0), value_text, font=label_font)
            collision_level = sum(abs(value - prior) < 4 for prior in prior_values)
            draw.text(
                (
                    x0 + bar_width / 2 - (value_box[2] - value_box[0]) / 2,
                    y0 - 25 - collision_level * 19,
                ),
                value_text,
                font=label_font,
                fill=INK,
            )
            prior_values.append(value)
        centered_text(
            draw,
            (center, plot_bottom + 55),
            label,
            typeface=font(16, bold=True),
            fill=INK,
            spacing=1,
        )

    if show_y_labels:
        axis_label = "Rubric checks passed (%)"
        axis_font = font(19)
        layer = Image.new("RGBA", (plot_height + 80, 44), (0, 0, 0, 0))
        layer_draw = ImageDraw.Draw(layer)
        centered_text(
            layer_draw,
            (layer.width / 2, layer.height / 2),
            axis_label,
            typeface=axis_font,
            fill=INK,
        )
        rotated = layer.rotate(90, expand=True)
        draw._image.paste(rotated, (left - 9, plot_top + (plot_height - rotated.height) // 2), rotated)


def render(data: dict, output: Path) -> Path:
    canvas = Image.new("RGB", (2600, 1300), PAPER)
    draw = ImageDraw.Draw(canvas)

    draw.text((115, 70), "CSS RESEARCH SKILLS", font=font(28, bold=True), fill=INK)
    date_box = draw.textbbox((0, 0), data["benchmark_date"], font=font(21))
    draw.text((2485 - (date_box[2] - date_box[0]), 77), data["benchmark_date"], font=font(21), fill=MUTED)
    draw.line((115, 120, 2485, 120), fill=INK, width=4)

    centered_text(
        draw,
        (1300, 190),
        "Comprehensive benchmark across skill versions",
        typeface=font(48, bold=True),
        fill=INK,
    )
    centered_text(
        draw,
        (1300, 250),
        "8 research tasks · 6 dimensions · 48 checks per condition",
        typeface=font(23),
        fill=MUTED,
    )

    conditions = data["conditions"]
    legend_y = 318
    legend_width = 760
    legend_left = 1300 - legend_width / 2
    draw.rectangle((legend_left, legend_y - 25, legend_left + legend_width, legend_y + 35), outline=FRAME, width=2)
    for index, condition in enumerate(conditions):
        item_x = legend_left + 35 + index * 250
        textured_bar(
            draw,
            (round(item_x), legend_y - 10, round(item_x + 50), legend_y + 10),
            fill=condition["color"],
            edge=condition["edge_color"],
            hatch=condition.get("hatch", ""),
        )
        draw.text((item_x + 64, legend_y - 14), condition["label"], font=font(18, bold=True), fill=INK)

    task_labels = [task["label"].replace("→", "to") for task in data["tasks"]]
    task_rates = {
        condition["id"]: [task["results"][condition["id"]]["pass_rate"] for task in data["tasks"]]
        for condition in conditions
    }
    draw_panel(
        draw,
        box=(115, 390, 1460, 1080),
        title="Task-level coverage",
        labels=task_labels,
        rates=task_rates,
        conditions=conditions,
        show_y_labels=True,
    )

    dimension_labels = [DIMENSION_LABELS[dimension["id"]] for dimension in data["dimensions"]] + ["Overall"]
    dimension_rates = {
        condition["id"]: [
            dimension["results"][condition["id"]]["pass_rate"] for dimension in data["dimensions"]
        ]
        + [condition["overall_pass_rate"]]
        for condition in conditions
    }
    draw_panel(
        draw,
        box=(1505, 390, 2485, 1080),
        title="Cross-task dimensions and overall",
        labels=dimension_labels,
        rates=dimension_rates,
        conditions=conditions,
        show_y_labels=False,
    )

    draw.text(
        (115, 1163),
        "Figure 1. Benchmark comparison across eight computational social-science tasks and six dimensions.",
        font=font(21),
        fill=INK,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, format="PNG", optimize=True)
    return output


def main() -> int:
    args = parse_args()
    results = load_results(args.input)
    output = render(results, args.output)
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
