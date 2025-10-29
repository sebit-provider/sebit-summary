from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field


class SummaryEntry(BaseModel):
    series: str = Field(..., description="Model family label (e.g., Asset & Depreciation).")
    model: str = Field(..., description="Specific model name (e.g., SEBIT-DDA).")
    headline_amount: float = Field(
        ...,
        description="Primary numeric amount to aggregate (e.g., final recognised revenue).",
    )
    currency: Optional[str] = Field(
        default=None,
        description="Optional currency code for the headline amount (e.g., KRW).",
    )
    details: Dict[str, float] = Field(
        default_factory=dict,
        description="Additional numeric metrics to display alongside the model output.",
    )


class SummaryRequest(BaseModel):
    report_label: Optional[str] = Field(
        default="SEBIT Summary Report",
        description="Friendly label for the generated report.",
    )
    as_of: Optional[datetime] = Field(
        default=None,
        description="Timestamp representing when the underlying figures were captured.",
    )
    entries: list[SummaryEntry] = Field(
        ...,
        min_length=1,
        description="List of model outputs to include in the summary.",
    )


class SummarySeriesHighlight(BaseModel):
    model: str
    headline_amount: float


class SummarySeriesAggregate(BaseModel):
    series: str
    model_count: int
    headline_total: float
    headline_average: float
    headline_min: float
    headline_max: float
    top_model: SummarySeriesHighlight
    bottom_model: SummarySeriesHighlight


class SummaryEntryResult(BaseModel):
    series: str
    model: str
    headline_amount: float
    currency: Optional[str]
    details: Dict[str, float]


class SummaryResponse(BaseModel):
    report_label: str
    as_of: Optional[datetime]
    total_models: int
    overall_headline_total: float
    series_summary: list[SummarySeriesAggregate]
    entries: list[SummaryEntryResult]
