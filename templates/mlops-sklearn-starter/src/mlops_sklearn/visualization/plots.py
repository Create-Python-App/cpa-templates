"""Plotting functions for data/model stages — plain functions, no StepContext needed."""

from __future__ import annotations

import matplotlib
import numpy as np
from matplotlib.figure import Figure
from sklearn.metrics import ConfusionMatrixDisplay

matplotlib.use("Agg")  # headless-safe: no GUI backend required in CI or containers


def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> Figure:
    display = ConfusionMatrixDisplay.from_predictions(y_true, y_pred)
    return display.figure_
