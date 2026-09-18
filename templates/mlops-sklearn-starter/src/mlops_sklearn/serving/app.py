"""Minimal FastAPI serving endpoint — plain responses, no APIResponse envelope.

Does not implement HTTP/request tracing itself; see MLOPS_CONTRACT.md's
Observability policy for why (fastapi-opentelemetry/fastapi-mlflow-tracing
are not yet compatible with this template's `mlops-sklearn` type):
https://github.com/Create-Python-App/cpa-templates/blob/main/docs/MLOPS_CONTRACT.md
"""

from __future__ import annotations

import logging
import os
from functools import lru_cache

import numpy as np
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from sklearn.pipeline import Pipeline

from mlops_sklearn.tracking.model_registry import load_model

logger = logging.getLogger(__name__)

app = FastAPI(title="mlops-sklearn-starter serving")


class PredictRequest(BaseModel):
    # No caller-supplied model_uri: this endpoint always serves the model
    # bound by server configuration (MODEL_URI), never a URI the request
    # body names. Accepting an arbitrary URI here would let a caller point
    # model loading at attacker-controlled data — MLflow's model loaders
    # deserialize pickled/joblib objects, so loading from an untrusted
    # source is a code-execution risk, not just a data risk.
    features: list[list[float]]


class PredictResponse(BaseModel):
    predictions: list[int]
    model_uri: str


def _model_uri() -> str:
    return os.environ.get("MODEL_URI", "models:/mlops-sklearn-local@production")


@lru_cache(maxsize=8)
def _load_cached_model(model_uri: str) -> Pipeline:
    # Cached per resolved model_uri string, not loaded once at startup: a
    # lifespan/startup hook would break the missing-model test, which
    # reassigns MODEL_URI mid-session and expects the *next* request to
    # reflect it. Keying by URI string keeps that working — same URI hits
    # the cache (fixing the ~22ms/request reload cost), a different URI is
    # a fresh miss. lru_cache does not cache exceptions, so a failed load
    # is retried on the next request rather than being stuck.
    #
    # Accepted tradeoff: re-promoting a *new version under the same
    # alias/URI string* (e.g. re-running `set_registered_model_alias` for
    # "production" without changing the URI) will NOT be picked up until
    # the process restarts. That's fine for this starter template but is
    # worth knowing before relying on this cache in a long-lived deployment.
    return load_model(model_uri)


@app.post("/predict", response_model=PredictResponse)
def predict_endpoint(body: PredictRequest) -> PredictResponse:
    model_uri = _model_uri()
    try:
        model = _load_cached_model(model_uri)
    except Exception:
        # MLflow raises varied exception types (MlflowException, RestException,
        # ...) for a missing model/alias/registry entry — normalize to 404.
        # Log the real cause server-side only; never echo exception internals
        # or the resolved model URI back to the caller.
        logger.exception("failed to load model for prediction")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="model not found",
        ) from None
    try:
        features = np.asarray(body.features, dtype=float)
        if features.ndim != 2 or 0 in features.shape:
            raise ValueError("features must be a non-empty 2D matrix")
        predictions = model.predict(features)
    except Exception:
        # Malformed client input (empty/ragged/wrong-shape features) is a
        # 422, not a 404 — it must never be conflated with a missing model.
        logger.exception("invalid prediction input")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="invalid feature matrix",
        ) from None
    return PredictResponse(predictions=[int(p) for p in predictions], model_uri=model_uri)
