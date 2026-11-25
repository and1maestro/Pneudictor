import pytest
from diagnosis.ml import get_pred_label, calculate_xray_probability, get_ai_model, MODEL_PATH
import numpy as np

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

@pytest.mark.unit
class TestCalculateXrayProbability:
    def test_returns_model_error_when_model_is_none(self, mocker):
        mocker.patch("diagnosis.ml.get_ai_model", return_value=None)
        mock_create_batches = mocker.patch(
            "diagnosis.ml.create_data_batches",
            autospec=True,
        )

        result = calculate_xray_probability("fake_xray.img")

        assert result == ("Model Error", 0.0)
        mock_create_batches.assert_not_called()

    def test_returns_prediction_label_and_probability(self, mocker):
        fake_model = mocker.Mock()
        fake_model.predict.return_value = np.array([[0.2, 0.8]])
        mocker.patch("diagnosis.ml.get_ai_model", return_value=fake_model)

        fake_batch = mocker.Mock()
        mock_create_batches = mocker.patch("diagnosis.ml.create_data_batches", return_value=fake_batch, autospec=True)

        label, probability = calculate_xray_probability("fake_path")

        assert label == "pneumonia"
        assert probability == pytest.approx(80.0)
        mock_create_batches.assert_called_once_with(["fake_path"], test_data=True)
        fake_model.predict.assert_called_once_with(fake_batch)

@pytest.mark.unit
class TestGetAiModel:
    @pytest.fixture(autouse=True)
    def reset_ai_model(self, monkeypatch):
        monkeypatch.setattr("diagnosis.ml._ai_model", None)

    def test_loads_model_only_once_and_caches_it(self, mocker):
        fake_model = mocker.Mock()
        mock_load_model = mocker.patch("diagnosis.ml.load_model", return_value=fake_model)

        first_call = get_ai_model()
        second_call = get_ai_model()

        assert first_call is fake_model
        assert second_call is fake_model
        mock_load_model.assert_called_once_with(MODEL_PATH)

    def test_returns_none_when_load_model_fails(self, mocker):
        mock_load_model = mocker.patch("diagnosis.ml.load_model", side_effect=OSError("Model file not found"))

        result = get_ai_model()

        assert result == None
        mock_load_model.assert_called_once_with(MODEL_PATH)