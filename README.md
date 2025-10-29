# SEBIT Summary API

Standalone FastAPI service that aggregates SEBIT model outputs into reporting payloads. Deploy this repository separately from the core SEBIT Engine so that financial statements (UI/UX) can call a dedicated reporting endpoint without exposing the modelling stack.

## Endpoints

- POST /summary/report ? Accepts multiple model outputs (series, model name, headline amount, optional details) and returns:
  - Overall totals
  - Per-series counts and aggregates
  - Entry-level breakdowns ready for dashboard display
- GET /health ? Basic readiness probe.

## Quickstart

`ash
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
`

## Example request

`ash
curl -X POST http://localhost:8000/summary/report \
  -H "Content-Type: application/json" \
  -d '{
        "report_label": "Quarterly Consolidated",
        "entries": [
          {
            "series": "Asset & Depreciation",
            "model": "SEBIT-DDA",
            "headline_amount": 24726.78,
            "currency": "KRW",
            "details": {"total_depreciation": 233449.88}
          },
          {
            "series": "Expense & Profit",
            "model": "SEBIT-PSRAS",
            "headline_amount": 6154364210.48,
            "currency": "KRW",
            "details": {"recognition_rate": 520.431561}
          }
        ]
      }'
`

## Integration Notes

- The core SEBIT Engine should call this service with the relevant model outputs once computations are complete.
- Responses can be cached or persisted for audit trails before rendering in the financial statement UI.
- Authentication/authorisation can be layered on this microservice independently of the modelling API.
