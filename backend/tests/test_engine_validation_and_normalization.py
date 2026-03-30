import unittest
from pathlib import Path

import pandas as pd

from app.services.reconciliation import (
    normalize_payroll_concepts,
    normalize_payroll_periods,
    validate_payroll_records,
    validate_payroll_schema,
)


class EngineValidationAndNormalizationTest(unittest.TestCase):
    def test_missing_required_columns_are_blocking(self) -> None:
        dataframe = pd.DataFrame([{"record_id": "R1", "amount": 10}])
        result = validate_payroll_schema(dataframe)
        self.assertTrue(result.is_blocking)
        self.assertIn("employee_id", result.missing_required_columns)

    def test_invalid_amount_marks_record_invalid(self) -> None:
        dataframe = pd.DataFrame(
            [
                {
                    "record_id": "R1",
                    "employee_id": "EMP1",
                    "payroll_period": "2026-03",
                    "posting_date": "2026-03-31",
                    "concept_code": "BONUS",
                    "concept_name": "Bonus",
                    "amount": "abc",
                    "currency": "EUR",
                }
            ]
        )
        result = validate_payroll_records(dataframe)
        self.assertEqual(result.invalid_record_count, 1)
        self.assertIn("invalid_amount", result.validated_records.iloc[0]["invalid_reasons"])

    def test_payroll_period_can_be_derived_from_posting_date(self) -> None:
        dataframe = pd.DataFrame(
            [
                {
                    "record_id": "R1",
                    "employee_id": "EMP1",
                    "payroll_period": "",
                    "posting_date": "2026-03-31",
                    "concept_code": "BONUS",
                    "concept_name": "Bonus",
                    "amount": 100,
                    "currency": "EUR",
                }
            ]
        )
        result = normalize_payroll_periods(dataframe, target_period="2026-03")
        self.assertEqual(
            result.normalized_records.iloc[0]["payroll_period_normalized"],
            "2026-03",
        )
        self.assertTrue(result.normalized_records.iloc[0]["payroll_period_derived"])

    def test_concept_mapping_covers_match_and_unmapped(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        dataframe = pd.DataFrame(
            [
                {
                    "record_id": "R1",
                    "employee_id": "EMP1",
                    "employee_name": "Ana",
                    "legal_entity": "ARD Spain SL",
                    "country": "Spain",
                    "cost_center": "OPS",
                    "payroll_period": "2026-03",
                    "posting_date": "2026-03-31",
                    "concept_code": "MEAL_VOUCHER",
                    "concept_name": "Meal Voucher",
                    "amount": 100,
                    "currency": "EUR",
                },
                {
                    "record_id": "R2",
                    "employee_id": "EMP2",
                    "employee_name": "Luis",
                    "legal_entity": "ARD Spain SL",
                    "country": "Spain",
                    "cost_center": "OPS",
                    "payroll_period": "2026-03",
                    "posting_date": "2026-03-31",
                    "concept_code": "MEAL_VCHR",
                    "concept_name": "Meal Voucher Legacy",
                    "amount": 100,
                    "currency": "EUR",
                },
            ]
        )
        result = normalize_payroll_concepts(
            dataframe,
            repo_root / "data/demo_seed/concept_master.csv",
        )
        self.assertEqual(result.normalized_records.iloc[0]["concept_mapping_method"], "code")
        self.assertFalse(result.normalized_records.iloc[0]["is_unmapped_concept"])
        self.assertTrue(result.normalized_records.iloc[1]["is_unmapped_concept"])


if __name__ == "__main__":
    unittest.main()
