import pytest
from diagnosis.utils import get_risk_class, calculate_psi_score
from types import SimpleNamespace

@pytest.fixture
def make_patient_data():
    def _make(**overrides):
        defaults = {
            "gender": "M",
            "age": 20,
            "nursing_home": False,
            "cancer": False,
            "liver_disease": False,
            "heart_disease": False,
            "cerebrovascular_disease": False,
            "renal_disease": False,
            "altered_mental_status": False,
            "respiratory_rate": 16,
            "systolic_bp": 120,
            "temperature": 36.6,
            "pulse": 75,
            "hemoglobin": 110,
        }
        defaults.update(overrides)
        return SimpleNamespace(**defaults)
    return _make

@pytest.mark.unit
class TestGetRiskClass:
    @pytest.mark.parametrize(
        "score, expected_risk_class, expected_mortality",
        [
            pytest.param(-1, "I (Low)", "0.1%", id="negative_score"),
            pytest.param(50, "I (Low)", "0.1%", id="higher_edge_first_class"),
            pytest.param(51, "II (Low)", "0.6%", id="lower_edge_second_class"),
            pytest.param(70, "II (Low)", "0.6%", id="higher_edge_second_class"),
            pytest.param(71, "III (Moderate)", "0.9 - 2.8%", id="lower_edge_third_class"),
            pytest.param(90, "III (Moderate)", "0.9 - 2.8%", id="higher_edge_third_class"),
            pytest.param(91, "IV (High)", "8.2 - 9.3%", id="lower_edge_fourth_class"),
            pytest.param(130, "IV (High)", "8.2 - 9.3%", id="higher_edge_fourth_class"),
            pytest.param(131, "V (Very high)", "27 - 31%", id="fifth_class")
        ]
    )
    def test_get_risk_class(self, score, expected_risk_class, expected_mortality):
        assert get_risk_class(score) == (expected_risk_class, expected_mortality)

@pytest.mark.unit
class TestCalculatePSIScore():
    @pytest.mark.parametrize(
        "overrides, expected_score",
        [
            # Demographics
            pytest.param({}, 20, id="healthy_male"),
            pytest.param({"gender": "F"}, 10, id="healthy_female"),
            pytest.param({"gender": "F", "age": 5}, -5, id="young_girl_negative_score"),

            # Boolean risk factors
            pytest.param({"nursing_home": True}, 30, id="nursing_home"),
            pytest.param({"cancer": True}, 50, id="cancer"),
            pytest.param({"liver_disease": True}, 40, id="liver_disease"),
            pytest.param({"heart_disease": True}, 30, id="heart_disease"),
            pytest.param({"cerebrovascular_disease": True}, 30, id="cerebrovascular_disease"),
            pytest.param({"renal_disease": True}, 30, id="renal_disease"),
            pytest.param({"altered_mental_status": True}, 40, id="altered_mental_status"),

            # Vital sign & lab boundaries
            pytest.param({"respiratory_rate": 29}, 20, id="respiratory_rate_below_threshold"),
            pytest.param({"respiratory_rate": 30}, 40, id="respiratory_rate_at_threshold"),
            pytest.param({"systolic_bp": 90}, 20, id="systolic_bp_at_threshold"),
            pytest.param({"systolic_bp": 89}, 40, id="systolic_bp_below_threshold"),
            pytest.param({"temperature": 34.9}, 35, id="temperature_below_low_threshold"),
            pytest.param({"temperature": 35.0}, 20, id="temperature_at_low_threshold"),
            pytest.param({"temperature": 39.9}, 20, id="temperature_below_high_threshold"),
            pytest.param({"temperature": 40.0}, 35, id="temperature_at_high_threshold"),
            pytest.param({"pulse": 124}, 20, id="pulse_below_threshold"),
            pytest.param({"pulse": 125}, 30, id="pulse_at_threshold"),
            pytest.param({"hemoglobin": 100}, 20, id="hemoglobin_at_threshold"),
            pytest.param({"hemoglobin": 99}, 30, id="hemoglobin_below_threshold"),

            # All risk factors active
            pytest.param(
                {
                    "nursing_home": True,
                    "cancer": True,
                    "liver_disease": True,
                    "heart_disease": True,
                    "cerebrovascular_disease": True,
                    "renal_disease": True,
                    "altered_mental_status": True,
                    "respiratory_rate": 30,
                    "systolic_bp": 89,
                    "temperature": 40.0,
                    "pulse": 125,
                    "hemoglobin": 99,
                },
                205,
                id="all_risk_factors_combined",
            ),
        ]
    )
    def test_calculate_psi_score(self, make_patient_data, overrides, expected_score):
        data = make_patient_data(**overrides)
        assert calculate_psi_score(data) == expected_score
