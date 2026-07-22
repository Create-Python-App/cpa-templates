from pathlib import Path

from mlops_sklearn.serving.predict import load_features


def test_load_features_fixture() -> None:
    arr = load_features(Path("tests/fixtures/sample_predict.csv"))
    assert arr.shape[0] == 2
    assert arr.shape[1] == 8
