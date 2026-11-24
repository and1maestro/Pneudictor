import pytest
from diagnosis.ml import get_pred_label

@pytest.mark.unit
class TestGetPredLabel:
    @pytest.mark.parametrize(
        "preds, expected",
        [
            pytest.param([0.75, 0.25], "normal", id="normal"),
            pytest.param([0.25, 0.75], "pneumonia", id="pneumonia"),
        ]
    )
    def test_get_pred_label(self, preds, expected):
        assert get_pred_label(preds) == expected