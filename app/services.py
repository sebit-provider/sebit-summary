from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

from .schemas import (
    SummaryEntry,
    SummaryEntryResult,
    SummaryReportRequest,
    SummaryReportResponse,
    SummarySeriesAggregate,
    SummarySeriesHighlight,
)


def build_summary_report(payload: SummaryReportRequest) -> SummaryReportResponse:
    entries: List[SummaryEntry] = payload.entries
    total_models = len(entries)
    overall_total = sum(entry.headline_amount for entry in entries)

    grouped: Dict[str, List[SummaryEntry]] = defaultdict(list)
    for entry in entries:
        grouped[entry.series].append(entry)

    series_summary: List[SummarySeriesAggregate] = []
    for series, series_entries in grouped.items():
        headline_values = [item.headline_amount for item in series_entries]
        headline_total = sum(headline_values)
        model_count = len(series_entries)
        headline_average = headline_total / model_count if model_count else 0.0
        headline_min = min(headline_values) if headline_values else 0.0
        headline_max = max(headline_values) if headline_values else 0.0

        top_entry = max(series_entries, key=lambda item: item.headline_amount)
        bottom_entry = min(series_entries, key=lambda item: item.headline_amount)

        series_summary.append(
            SummarySeriesAggregate(
                series=series,
                model_count=model_count,
                headline_total=round(headline_total, 2),
                headline_average=round(headline_average, 2),
                headline_min=round(headline_min, 2),
                headline_max=round(headline_max, 2),
                top_model=SummarySeriesHighlight(
                    model=top_entry.model,
                    headline_amount=round(top_entry.headline_amount, 2),
                ),
                bottom_model=SummarySeriesHighlight(
                    model=bottom_entry.model,
                    headline_amount=round(bottom_entry.headline_amount, 2),
                ),
            )
        )

    response_entries = [
        SummaryEntryResult(
            series=entry.series,
            model=entry.model,
            headline_amount=round(entry.headline_amount, 2),
            currency=entry.currency,
            details=entry.details.model_dump(),
        )
        for entry in entries
    ]

    return SummaryReportResponse(
        report_label=payload.report_label or "SEBIT Summary Report",
        as_of=payload.as_of,
        total_models=total_models,
        overall_headline_total=round(overall_total, 2),
        series_summary=series_summary,
        entries=response_entries,
    )
