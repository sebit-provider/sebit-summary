from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Union

from pydantic import BaseModel, Field, model_validator


# -----------------------------------------------------------------------------
# Model-specific detail DTOs
# -----------------------------------------------------------------------------


class DdaDetails(BaseModel):
    asset_label: str
    schedule: List[Dict[str, Any]] = Field(default_factory=list)
    total_depreciation: float
    total_revaluation_gain_loss: float
    total_unrecognised_revaluation: float


class LamDetails(BaseModel):
    lease_label: str
    schedule: List[Dict[str, Any]] = Field(default_factory=list)
    total_revaluation_gain_loss: float
    total_interest_expense: float
    total_termination_adjustment: float


class RvmDetails(BaseModel):
    resource_label: str
    daily_average_extraction: float
    standard_extraction_value: float
    total_extraction_value: float
    extraction_rate: float
    market_change_index: float
    market_sensitivity: float
    final_revaluation_value: float


class CeemDetails(BaseModel):
    expense_label: str
    daily_average_usage_units: float
    standard_usage_value_non_quantitative: float
    standard_usage_value_quantitative: Optional[float]
    selected_standard_usage_value: float
    total_consumable_usage_value: float
    adjusted_consumable_usage_value: float
    usage_change_rate: float
    market_change_index: float
    market_sensitivity_value: float
    final_revaluation_value: float


class BdmDetails(BaseModel):
    bond_label: str
    daily_estimated_usage: float
    estimated_value_ps: float
    market_beta: float
    final_book_value: float
    interest_cost: float
    interest_type: str


class BelmDetails(BaseModel):
    debtor_label: str
    daily_estimated_repayment: float
    expected_repayment_at_evaluation: float
    interest_rate_adjustment: float
    actual_interest_cost: float
    preliminary_bad_debt_ratio: float
    final_bad_debt_ratio: float


class CprmDetails(BaseModel):
    exposure_id: str
    assumed_bad_debt_occurrence_rate: float
    convertible_bond_rate: float
    convertible_bond_first_amount: float
    average_past_bad_debt_recovery: float
    average_convertible_bond_price: float
    additional_adjustment_beta: float
    final_convertible_bond_amount: float
    trigger_applied: bool
    convertible_bond_rate_adjustment: float
    final_adjusted_convertible_bond_rate: float


class CocimQuarterAdjustment(BaseModel):
    quarter_index: int
    adjustment_value: float
    pre_compound_balance: float
    post_compound_balance: float


class CocimDetails(BaseModel):
    portfolio_label: str
    account_ratio: float
    initial_compound_measurement: float
    quarterly_adjustments: List[CocimQuarterAdjustment] = Field(default_factory=list)
    annual_compound_growth_rate: float
    compound_growth_trigger_applied: bool
    compound_adjustment_amount: float
    final_adjusted_balance: float


class FarexDetails(BaseModel):
    contract_id: str
    last_year_trade_ratio: float
    current_year_trade_ratio: float
    export_import_beta: float
    adjustment_indicator: float
    inflation_adjusted_rate: float
    final_adjusted_rate: float
    revaluation_amount: float


class TctBeamDetails(BaseModel):
    model_label: str
    evaluation_years: int
    cumulative_fixed_cost: float
    cumulative_variable_cost: float
    cumulative_operating_profit: float
    break_even_year_index: Optional[int]
    schedule: List[Dict[str, Any]] = Field(default_factory=list)


class CpmrvDetails(BaseModel):
    asset_label: str
    last_year_average_performance: float
    current_year_log_ratio: float
    monthly_growth_risk: float
    risk_direction: str
    relative_asset_risk: float
    adjusted_crypto_value: float


class DcbpraDetails(BaseModel):
    asset_label: str
    growth_percentage_factor: float
    real_growth_adjustment: float
    last_year_average_performance: float
    current_year_log_ratio: float
    monthly_growth_risk: float
    risk_adjustment_component: float
    risk_direction: str
    adjusted_beta: float
    baseline_capm_return: float
    adjusted_expected_return: float


class PsrasDetails(BaseModel):
    portfolio_label: str
    assumed_revenue_recognition_rate: float
    new_subscriber_average_payment: float
    existing_subscriber_average_payment: float
    payment_comparison_index: float
    payment_index_baseline_amount: float
    pure_performance_break_even: float
    final_recognised_revenue: float


class LsmrvDetails(BaseModel):
    evaluation_label: str
    probability_distribution_a: float
    probability_distribution_b: float
    growth_correction_value: float
    cumulative_adjustment_value: float
    expected_adjustment_value: float
    final_adjustment_amount: float


ModelDetailUnion = Union[
    DdaDetails,
    LamDetails,
    RvmDetails,
    CeemDetails,
    BdmDetails,
    BelmDetails,
    CprmDetails,
    CocimDetails,
    FarexDetails,
    TctBeamDetails,
    CpmrvDetails,
    DcbpraDetails,
    PsrasDetails,
    LsmrvDetails,
]


@dataclass(frozen=True)
class ModelRegistryEntry:
    model: str
    series: str
    detail_model: Type[BaseModel]
    headline_key: str


MODEL_REGISTRY: Dict[str, ModelRegistryEntry] = {
    "SEBIT-DDA": ModelRegistryEntry(
        model="SEBIT-DDA",
        series="Asset & Depreciation",
        detail_model=DdaDetails,
        headline_key="total_revaluation_gain_loss",
    ),
    "SEBIT-LAM": ModelRegistryEntry(
        model="SEBIT-LAM",
        series="Asset & Depreciation",
        detail_model=LamDetails,
        headline_key="total_revaluation_gain_loss",
    ),
    "SEBIT-RVM": ModelRegistryEntry(
        model="SEBIT-RVM",
        series="Asset & Depreciation",
        detail_model=RvmDetails,
        headline_key="final_revaluation_value",
    ),
    "SEBIT-CEEM": ModelRegistryEntry(
        model="SEBIT-CEEM",
        series="Expense & Profitability",
        detail_model=CeemDetails,
        headline_key="final_revaluation_value",
    ),
    "SEBIT-BDM": ModelRegistryEntry(
        model="SEBIT-BDM",
        series="Expense & Profitability",
        detail_model=BdmDetails,
        headline_key="final_book_value",
    ),
    "SEBIT-BELM": ModelRegistryEntry(
        model="SEBIT-BELM",
        series="Expense & Profitability",
        detail_model=BelmDetails,
        headline_key="final_bad_debt_ratio",
    ),
    "SEBIT-CPRM": ModelRegistryEntry(
        model="SEBIT-CPRM",
        series="Capital & Risk Derivatives",
        detail_model=CprmDetails,
        headline_key="final_convertible_bond_amount",
    ),
    "SEBIT-C-OCIM": ModelRegistryEntry(
        model="SEBIT-C-OCIM",
        series="Capital & Risk Derivatives",
        detail_model=CocimDetails,
        headline_key="final_adjusted_balance",
    ),
    "SEBIT-FAREX": ModelRegistryEntry(
        model="SEBIT-FAREX",
        series="Capital & Risk Derivatives",
        detail_model=FarexDetails,
        headline_key="revaluation_amount",
    ),
    "SEBIT-TCT-BEAM": ModelRegistryEntry(
        model="SEBIT-TCT-BEAM",
        series="Advanced Analytics",
        detail_model=TctBeamDetails,
        headline_key="cumulative_operating_profit",
    ),
    "SEBIT-CPMRV": ModelRegistryEntry(
        model="SEBIT-CPMRV",
        series="Advanced Analytics",
        detail_model=CpmrvDetails,
        headline_key="adjusted_crypto_value",
    ),
    "SEBIT-DCBPRA": ModelRegistryEntry(
        model="SEBIT-DCBPRA",
        series="Advanced Analytics",
        detail_model=DcbpraDetails,
        headline_key="adjusted_expected_return",
    ),
    "SEBIT-PSRAS": ModelRegistryEntry(
        model="SEBIT-PSRAS",
        series="Insurance & Service Revenue",
        detail_model=PsrasDetails,
        headline_key="final_recognised_revenue",
    ),
    "SEBIT-LSMRV": ModelRegistryEntry(
        model="SEBIT-LSMRV",
        series="Probability Revaluation",
        detail_model=LsmrvDetails,
        headline_key="final_adjustment_amount",
    ),
}


class SummaryEntry(BaseModel):
    series: str = Field(..., description="Model family label (e.g., Asset & Depreciation).")
    model: str = Field(..., description="Specific model identifier (e.g., SEBIT-DDA).")
    headline_amount: float = Field(
        ...,
        description="Primary numeric amount for the model (e.g., final recognised revenue).",
    )
    currency: Optional[str] = Field(
        default=None,
        description="Currency code associated with the headline amount.",
    )
    details: ModelDetailUnion = Field(
        ...,
        description="Structured detail payload for the given SEBIT model.",
    )

    @classmethod
    def from_model_output(cls, model_name: str, data: Dict[str, Any], currency: Optional[str] = None) -> "SummaryEntry":
        entry = MODEL_REGISTRY.get(model_name)
        if entry is None:
            raise ValueError(f"Model '{model_name}' is not registered for summary aggregation.")

        detail_instance = entry.detail_model(**data)
        headline_value = data.get(entry.headline_key)
        if headline_value is None:
            raise ValueError(
                f"Model '{model_name}' output missing headline key '{entry.headline_key}'."
            )

        return cls(
            series=entry.series,
            model=entry.model,
            headline_amount=float(headline_value),
            currency=currency,
            details=detail_instance,
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
    details: Dict[str, Any]


class SummaryModelOutput(BaseModel):
    model_name: str = Field(..., description="Registered SEBIT model identifier (e.g., SEBIT-DDA).")
    payload: Dict[str, Any] = Field(
        ...,
        description="Raw output returned by the SEBIT model endpoint.",
    )
    currency: Optional[str] = Field(
        default=None,
        description="Optional override for the headline currency code.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "model_name": "SEBIT-DDA",
                "payload": {
                    "asset_label": "facility-line-1",
                    "schedule": [],
                    "total_depreciation": 233449.88,
                    "total_revaluation_gain_loss": 5400.25,
                    "total_unrecognised_revaluation": 250.0,
                },
                "currency": "KRW",
            }
        }
    }


class SummaryReportRequest(BaseModel):
    report_label: Optional[str] = Field(
        default="SEBIT Summary Report",
        description="Friendly label for the generated report.",
    )
    as_of: Optional[datetime] = Field(
        default=None,
        description="Timestamp representing when the figures were captured.",
    )
    entries: Optional[List[SummaryEntry]] = Field(
        default=None,
        description="Pre-built summary entries (optional when model_outputs is provided).",
    )
    model_outputs: Optional[List[SummaryModelOutput]] = Field(
        default=None,
        min_length=1,
        description="Raw SEBIT model outputs that will be converted into entries automatically.",
    )

    @model_validator(mode="after")
    def _validate_sources(self) -> "SummaryReportRequest":
        if not self.entries and not self.model_outputs:
            raise ValueError("Either 'entries' or 'model_outputs' must be provided.")
        return self

    def resolve_entries(self) -> List[SummaryEntry]:
        if self.entries:
            return self.entries
        assert self.model_outputs, "model_outputs should be available when entries is None"
        return [
            SummaryEntry.from_model_output(item.model_name, item.payload, currency=item.currency)
            for item in self.model_outputs
        ]

    model_config = {
        "json_schema_extra": {
            "example": {
                "report_label": "October Portfolio Update",
                "as_of": "2025-10-30T09:40:15.788Z",
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
        }
    }


class SummaryReportResponse(BaseModel):
    report_label: str
    as_of: Optional[datetime]
    total_models: int
    overall_headline_total: float
    series_summary: List[SummarySeriesAggregate]
    entries: List[SummaryEntryResult]

    model_config = {
        "json_schema_extra": {
            "example": {
                "report_label": "October Portfolio Update",
                "as_of": "2025-10-30T09:40:15.788Z",
                "total_models": 2,
                "overall_headline_total": 6154369610.73,
                "series_summary": [
                    {
                        "series": "Asset & Depreciation",
                        "model_count": 1,
                        "headline_total": 5400.25,
                        "headline_average": 5400.25,
                        "headline_min": 5400.25,
                        "headline_max": 5400.25,
                        "top_model": {"model": "SEBIT-DDA", "headline_amount": 5400.25},
                        "bottom_model": {"model": "SEBIT-DDA", "headline_amount": 5400.25},
                    },
                    {
                        "series": "Insurance & Service Revenue",
                        "model_count": 1,
                        "headline_total": 6154364210.48,
                        "headline_average": 6154364210.48,
                        "headline_min": 6154364210.48,
                        "headline_max": 6154364210.48,
                        "top_model": {"model": "SEBIT-PSRAS", "headline_amount": 6154364210.48},
                        "bottom_model": {"model": "SEBIT-PSRAS", "headline_amount": 6154364210.48},
                    },
                ],
                "entries": [
                    {
                        "series": "Asset & Depreciation",
                        "model": "SEBIT-DDA",
                        "headline_amount": 5400.25,
                        "currency": "KRW",
                        "details": {
                            "asset_label": "facility-line-1",
                            "schedule": [],
                            "total_depreciation": 233449.88,
                            "total_revaluation_gain_loss": 5400.25,
                            "total_unrecognised_revaluation": 250.0,
                        },
                    },
                    {
                        "series": "Insurance & Service Revenue",
                        "model": "SEBIT-PSRAS",
                        "headline_amount": 6154364210.48,
                        "currency": "KRW",
                        "details": {
                            "portfolio_label": "insurance-cohort-1",
                            "assumed_revenue_recognition_rate": 0.4125,
                            "new_subscriber_average_payment": 263500.0,
                            "existing_subscriber_average_payment": 185200.0,
                            "payment_comparison_index": -0.0451,
                            "payment_index_baseline_amount": 512480000.0,
                            "pure_performance_break_even": 18250000.0,
                            "final_recognised_revenue": 6154364210.48,
                        },
                    },
                ],
            }
        }
    }

