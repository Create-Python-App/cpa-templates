"""Minimal FastAPI serving endpoint — plain responses, no APIResponse envelope.

Does not implement HTTP/request tracing itself; see docs/MLOPS_CONTRACT.md's
Observability policy for why (fastapi-opentelemetry/fastapi-mlflow-tracing
are not yet compatible with this template's `mlops-sklearn` type).
"""

from __future__ import annotations

import os

import numpy as np
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from mlops_sklearn.serving.predict import predict

app = FastAPI(title="mlops-sklearn-starter serving")


class PredictRequest(BaseModel):
    features: list[list[float]]
    model_uri: str | None = None


class PredictResponse(BaseModel):
    predictions: list[int]
    model_uri: str


def _default_model_uri() -> str:
    return os.environ.get("MODEL_URI", "models:/mlops-sklearn-local@production")


@app.post("/predict", response_model=PredictResponse)
def predict_endpoint(body: PredictRequest) -> PredictResponse:
    model_uri = body.model_uri or _default_model_uri()
    try:
        predictions = predict(model_uri, np.array(body.features))
    except Exception as exc:
        # MLflow raises varied exception types (MlflowException, RestException,
        # ...) for a missing model/alias/registry entry — normalize to 404.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"could not load model at {model_uri!r}: {exc}",
        ) from exc
    return PredictResponse(predictions=[int(p) for p in predictions], model_uri=model_uri)
