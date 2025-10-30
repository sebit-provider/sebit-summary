from fastapi.testclient import TestClient

from app.main import create_app


def test_summary_report():
    client = TestClient(create_app())
    payload = {
        "report_label": "Quarterly Consolidated",
        "model_outputs": [
            {
                "model_name": "SEBIT-DDA",
                "payload": {
                    "asset_label": "facility-line-1",
                    "schedule": [],
                    "total_depreciation": 233449.88,
                    "total_revaluation_gain_loss": 5400.25,
                    "total_unrecognised_revaluation": 250.0,
                },
                "currency": "KRW",
            },
            {
                "model_name": "SEBIT-PSRAS",
                "payload": {
                    "portfolio_label": "insurance-cohort-1",
                    "assumed_revenue_recognition_rate": 0.4125,
                    "new_subscriber_average_payment": 263500.0,
                    "existing_subscriber_average_payment": 185200.0,
                    "payment_comparison_index": -0.0451,
                    "payment_index_baseline_amount": 512480000.0,
                    "pure_performance_break_even": 18250000.0,
                    "final_recognised_revenue": 6154364210.48,
                },
                "currency": "KRW",
            },
        ],
    }

    response = client.post("/summary/report", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["report_label"] == "Quarterly Consolidated"
    assert data["total_models"] == 2
    assert data["overall_headline_total"] == 6154369610.73
    first_entry = data["entries"][0]
    assert first_entry["series"] == "Asset & Depreciation"
    assert first_entry["model"] == "SEBIT-DDA"
    assert first_entry["headline_amount"] == 5400.25
    assert first_entry["details"]["total_depreciation"] == 233449.88
