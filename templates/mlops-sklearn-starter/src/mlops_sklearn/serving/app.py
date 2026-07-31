"""Minimal FastAPI serving endpoint — plain responses, no APIResponse envelope.

Does not implement HTTP/request tracing itself; see docs/MLOPS_CONTRACT.md's
Observability policy for why (fastapi-opentelemetry/fastapi-mlflow-tracing
are not yet compatible with this template's `mlops-sklearn` type).
"""

from __future__ import annotations

import logging
import os

import numpy as np
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from mlops_sklearn.serving.predict import predict

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


@app.post("/predict", response_model=PredictResponse)
def predict_endpoint(body: PredictRequest) -> PredictResponse:
    model_uri = _model_uri()
    try:
        predictions = predict(model_uri, np.array(body.features))
    except Exception:
        # MLflow raises varied exception types (MlflowException, RestException,
        # ...) for a missing model/alias/registry entry — normalize to 404.
        # Log the real cause server-side only; never echo exception internals
        # or the resolved model URI back to the caller.
        logger.exception("failed to load or run model for prediction")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="model not found",
        ) from None
    return PredictResponse(predictions=[int(p) for p in predictions], model_uri=model_uri)
