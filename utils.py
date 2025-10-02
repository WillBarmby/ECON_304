"""Utility helpers for reusable goods market visualisations."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np

__all__ = [
    "GoodsMarketLineSpec",
    "GuideSpec",
    "PointSpec",
    "ArrowSpec",
    "TextSpec",
    "default_goods_market_elements",
    "plot_goods_market_diagram",
]

Pair = Tuple[float, float]


@dataclass(frozen=True)
class GoodsMarketLineSpec:
    """Configuration for an aggregate expenditure schedule."""

    shift: float = 0.0
    label: Optional[str] = None
    label_xy: Optional[Pair] = None
    plot_kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GuideSpec:
    """Description of a guide line drawn in data coordinates."""

    orientation: str
    value: float
    start: float
    end: float
    text: Optional[str] = None
    text_xy: Optional[Pair] = None
    text_kwargs: Dict[str, Any] = field(default_factory=dict)
    line_kwargs: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:  # type: ignore[override]
        if self.orientation not in {"vertical", "horizontal"}:
            raise ValueError("orientation must be 'vertical' or 'horizontal'")


@dataclass(frozen=True)
class PointSpec:
    """Marker configuration for a point of interest."""

    xy: Pair
    label: Optional[str] = None
    label_xy: Optional[Pair] = None
    label_kwargs: Dict[str, Any] = field(default_factory=dict)
    plot_kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ArrowSpec:
    """Arrow connecting two points, optionally with an adjacent label."""

    xy: Pair
    xytext: Pair
    arrow_kwargs: Dict[str, Any] = field(default_factory=dict)
    label: Optional[str] = None
    label_xy: Optional[Pair] = None
    label_kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TextSpec:
    """Free-form text placement."""

    xy: Pair
    text: str
    text_kwargs: Dict[str, Any] = field(default_factory=dict)


def _normalise(value: float, limits: Pair) -> float:
    lower, upper = limits
    if upper == lower:
        raise ValueError("Axis limits must span a non-zero range")
    return (value - lower) / (upper - lower)


def _draw_guide(ax: plt.Axes, spec: GuideSpec, x_limits: Pair, y_limits: Pair) -> None:
    default_kwargs = {"color": "black", "linewidth": 0.5, "ls": "--"}
    line_kwargs = {**default_kwargs, **spec.line_kwargs}

    if spec.orientation == "vertical":
        ymin = _normalise(spec.start, y_limits)
        ymax = _normalise(spec.end, y_limits)
        ax.axvline(spec.value, ymin=ymin, ymax=ymax, **line_kwargs)
    else:
        xmin = _normalise(spec.start, x_limits)
        xmax = _normalise(spec.end, x_limits)
        ax.axhline(spec.value, xmin=xmin, xmax=xmax, **line_kwargs)

    if spec.text and spec.text_xy:
        text_kwargs = {"fontsize": 12, **spec.text_kwargs}
        ax.text(*spec.text_xy, spec.text, **text_kwargs)


def default_goods_market_elements() -> Dict[str, Sequence[Any]]:
    """Return the configuration that reproduces the lecture diagram."""

    lines = (
        GoodsMarketLineSpec(shift=0.0, label=r"$ZZ(G_1)$", label_xy=(25, 18)),
        GoodsMarketLineSpec(shift=-8.8, label=r"$ZZ(G_0)$", label_xy=(25, 9)),
    )

    guides = (
        GuideSpec("vertical", value=18, start=0, end=18),
        GuideSpec("horizontal", value=18, start=0, end=18),
        GuideSpec("vertical", value=5, start=0, end=5),
        GuideSpec("horizontal", value=5, start=0, end=5),
        GuideSpec("horizontal", value=13.7, start=0, end=5),
        GuideSpec("vertical", value=10, start=0, end=15.5),
        GuideSpec("horizontal", value=15.5, start=0, end=10),
    )

    points = (
        PointSpec(xy=(18, 18)),
        PointSpec(xy=(5, 5)),
        PointSpec(xy=(5, 13.7)),
        PointSpec(xy=(10, 15.5)),
    )

    arrows = (
        ArrowSpec(
            xy=(5, 5.5),
            xytext=(5, 13.1),
            arrow_kwargs={"arrowstyle": "<->", "lw": 1.5},
            label="Shortage",
            label_xy=(5.5, 9.5),
            label_kwargs={"fontsize": 10, "verticalalignment": "center"},
        ),
        ArrowSpec(xy=(5.3, 2), xytext=(9.7, 2), arrow_kwargs={"arrowstyle": "<-", "lw": 1.5}),
        ArrowSpec(xy=(10.3, 2), xytext=(17.7, 2), arrow_kwargs={"arrowstyle": "<-", "lw": 1.5}),
        ArrowSpec(
            xy=(10, 10.3),
            xytext=(10, 15),
            arrow_kwargs={"arrowstyle": "<->", "lw": 1.5},
            label="Shortage",
            label_xy=(10.5, 12.5),
            label_kwargs={"fontsize": 10, "verticalalignment": "center"},
        ),
        ArrowSpec(xy=(23, 11.5), xytext=(23, 19), arrow_kwargs={"arrowstyle": "<-", "lw": 3}),
    )

    texts = (
        TextSpec(
            xy=(18, -1),
            text="Y*",
            text_kwargs={"fontsize": 12, "verticalalignment": "top", "horizontalalignment": "center"},
        ),
        TextSpec(
            xy=(-1, 19),
            text="Z*",
            text_kwargs={"fontsize": 12, "verticalalignment": "top", "horizontalalignment": "center"},
        ),
        TextSpec(
            xy=(5, -1),
            text=r"$Y_0$",
            text_kwargs={"fontsize": 12, "verticalalignment": "top", "horizontalalignment": "center"},
        ),
        TextSpec(
            xy=(-0.5, 5),
            text=r"$Y_0$",
            text_kwargs={"fontsize": 12, "verticalalignment": "center", "horizontalalignment": "right"},
        ),
        TextSpec(
            xy=(-0.5, 13.7),
            text=r"$Z_1$",
            text_kwargs={"fontsize": 12, "verticalalignment": "center", "horizontalalignment": "right"},
        ),
        TextSpec(
            xy=(10, -1),
            text=r"$Y_1$",
            text_kwargs={"fontsize": 12, "verticalalignment": "top", "horizontalalignment": "center"},
        ),
        TextSpec(
            xy=(-0.5, 17),
            text=r"$Z_2$",
            text_kwargs={"fontsize": 12, "verticalalignment": "top", "horizontalalignment": "right"},
        ),
    )

    diagonal_label = TextSpec(xy=(25, 23), text="Y=Z")

    return {
        "line_specs": lines,
        "guides": guides,
        "points": points,
        "arrows": arrows,
        "texts": texts,
        "diagonal_label": diagonal_label,
    }


def plot_goods_market_diagram(
    intercept: float = 12.0,
    slope: float = 1 / 3,
    x_domain: Pair = (0, 40),
    num_points: int = 200,
    line_specs: Optional[Sequence[GoodsMarketLineSpec]] = None,
    guides: Optional[Sequence[GuideSpec]] = None,
    points: Optional[Sequence[PointSpec]] = None,
    arrows: Optional[Sequence[ArrowSpec]] = None,
    texts: Optional[Sequence[TextSpec]] = None,
    diagonal_line: bool = True,
    diagonal_kwargs: Optional[Dict[str, Any]] = None,
    diagonal_label: Optional[TextSpec] = None,
    figsize: Pair = (6.5, 3.5),
    ax: Optional[plt.Axes] = None,
    x_limits: Pair = (0, 30),
    y_limits: Pair = (0, 30),
    xlabel: str = "Output, Y",
    ylabel: str = "Agg. Exp., Z",
    xlabel_kwargs: Optional[Dict[str, Any]] = None,
    ylabel_kwargs: Optional[Dict[str, Any]] = None,
    title: str = "Goods Market",
    title_kwargs: Optional[Dict[str, Any]] = None,
    grid: bool = True,
    remove_ticks: bool = True,
    horizontal_zero: bool = True,
) -> Tuple[plt.Figure, plt.Axes]:
    """Plot a goods market diagram with highly customisable components."""

    if num_points < 2:
        raise ValueError("num_points must be at least 2")

    defaults = default_goods_market_elements()
    if line_specs is None:
        line_specs = defaults["line_specs"]
    if guides is None:
        guides = defaults["guides"]
    if points is None:
        points = defaults["points"]
    if arrows is None:
        arrows = defaults["arrows"]
    if texts is None:
        texts = defaults["texts"]
    if diagonal_label is None and diagonal_line:
        diagonal_label = defaults["diagonal_label"]

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    x = np.linspace(*x_domain, num_points)
    base_line = intercept + slope * x

    for spec in line_specs:
        line_kwargs = {"linewidth": 2.0, **spec.plot_kwargs}
        y_vals = base_line + spec.shift
        ax.plot(x, y_vals, **line_kwargs)
        if spec.label and spec.label_xy:
            ax.text(*spec.label_xy, spec.label, color=line_kwargs.get("color", "black"))

    if diagonal_line:
        diag_kwargs = {"color": "red", "linewidth": 0.5, "ls": "--"}
        if diagonal_kwargs:
            diag_kwargs.update(diagonal_kwargs)
        ax.plot(x, x, **diag_kwargs)
        if diagonal_label:
            label_kwargs = {"color": diag_kwargs.get("color", "black")}
            label_kwargs.update(diagonal_label.text_kwargs)
            ax.text(*diagonal_label.xy, diagonal_label.text, **label_kwargs)

    ax.set_xlim(*x_limits)
    ax.set_ylim(*y_limits)

    if horizontal_zero:
        ax.axhline(0, color="black", linewidth=0.5, ls="--")

    for guide in guides:
        _draw_guide(ax, guide, x_limits, y_limits)

    for point in points:
        plot_kwargs = {"marker": "o", "color": "black"}
        plot_kwargs.update(point.plot_kwargs)
        ax.plot(*point.xy, **plot_kwargs)
        if point.label and point.label_xy:
            label_kwargs = {"fontsize": 12, **point.label_kwargs}
            ax.text(*point.label_xy, point.label, **label_kwargs)

    for arrow in arrows:
        arrow_kwargs = {"arrowstyle": "->", "lw": 1.5}
        arrow_kwargs.update(arrow.arrow_kwargs)
        ax.annotate("", xy=arrow.xy, xytext=arrow.xytext, arrowprops=arrow_kwargs)
        if arrow.label and arrow.label_xy:
            label_kwargs = {"fontsize": 10, **arrow.label_kwargs}
            ax.text(*arrow.label_xy, arrow.label, **label_kwargs)

    for text in texts:
        ax.text(*text.xy, text.text, **text.text_kwargs)

    xlabel_kwargs = {"loc": "right", **(xlabel_kwargs or {})}
    ylabel_kwargs = {"loc": "top", **(ylabel_kwargs or {})}
    title_kwargs = {**(title_kwargs or {})}

    ax.set_xlabel(xlabel, **xlabel_kwargs)
    ax.set_ylabel(ylabel, **ylabel_kwargs)
    ax.set_title(title, **title_kwargs)

    if grid:
        ax.grid(True)
    if remove_ticks:
        ax.set_xticks([])
        ax.set_yticks([])

    return fig, ax
