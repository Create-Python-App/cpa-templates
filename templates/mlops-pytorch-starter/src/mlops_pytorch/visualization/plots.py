"""Plotting functions for data/model stages — plain functions, no StepContext needed."""

from __future__ import annotations

import matplotlib
import numpy as np
from matplotlib.figure import Figure

matplotlib.use("Agg")  # headless-safe: no GUI backend required in CI or containers


def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> Figure:
    labels = [0, 1]
    matrix = np.zeros((2, 2), dtype=int)
    for t, p in zip(y_true.tolist(), y_pred.tolist()):
        if t in labels and p in labels:
            matrix[t, p] += 1
    figure = Figure(figsize=(4, 4))
    ax = figure.subplots()
    im = ax.imshow(matrix, cmap="Blues")
    figure.colorbar(im, ax=ax)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(matrix[i, j]), ha="center", va="center")
    return figure
