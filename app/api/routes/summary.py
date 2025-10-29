from fastapi import APIRouter

from ...schemas import SummaryRequest, SummaryResponse
from ...services import build_summary_report

router = APIRouter()


@router.post(
    "/report",
    response_model=SummaryResponse,
    summary="Aggregate SEBIT model outputs for reporting",
)
def create_summary_report(payload: SummaryRequest) -> SummaryResponse:
    """Group multiple SEBIT model outputs into a series-based summary payload."""
    return build_summary_report(payload)
