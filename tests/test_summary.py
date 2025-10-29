from fastapi.testclient import TestClient

from app.main import create_app


def test_summary_report():
    client = TestClient(create_app())
    payload = {
        "report_label": "Quarterly Consolidated",
        "entries": [
            {
                "series": "Asset & Depreciation",
                "model": "SEBIT-DDA",
                "headline_amount": 24726.78,
                "currency": "KRW",
                "details": {"total_depreciation": 233449.88},
            },
            {
                "series": "Expense & Profit",
                "model": "SEBIT-PSRAS",
                "headline_amount": 6154364210.48,
                "currency": "KRW",
                "details": {"recognition_rate": 520.431561},
            },
        ],
    }

    response = client.post("/summary/report", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["report_label"] == "Quarterly Consolidated"
    assert data["total_models"] == 2
    assert data["overall_headline_total"] == 6154388937.26
