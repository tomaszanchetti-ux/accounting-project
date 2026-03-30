import unittest
from pathlib import Path

import pandas as pd

from app.services.reconciliation import (
    assign_reconciliation_status,
    build_observed_totals,
    calculate_differences,
)


class EngineAggregationAndStatusTest(unittest.TestCase):
    def test_observed_totals_group_by_period_and_concept(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = build_observed_totals(
            repo_root / "data/demo_seed/payroll.csv",
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )
        self.assertEqual(result.total_groups, 10)

    def test_diff_metrics_are_calculated(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = calculate_differences(
            repo_root / "data/demo_seed/payroll.csv",
            repo_root / "data/demo_seed/expected_totals.csv",
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )
        rows = result.comparison_with_diffs.set_index("concept_code_normalized")
        self.assertEqual(rows.loc["BASE_SALARY", "absolute_diff"], 10.0)
        self.assertEqual(rows.loc["TRANSPORT", "absolute_diff"], -240.0)

    def test_status_bands_and_invalid_incomplete(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = assign_reconciliation_status(
            repo_root / "data/demo_seed/payroll.csv",
            repo_root / "data/demo_seed/expected_totals.csv",
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )
        rows = result.comparison_with_diffs.set_index("concept_code_normalized")
        self.assertEqual(rows.loc["BASE_SALARY", "status"], "Reconciled")
        self.assertEqual(rows.loc["TRANSPORT", "status"], "Minor Difference")
        self.assertEqual(rows.loc["MEAL_VOUCHER", "status"], "Unreconciled")

        dataframe = pd.DataFrame(
            [
                {
                    "payroll_period": "2026-03",
                    "concept_code": "BASE_SALARY",
                    "expected_amount": 100.0,
                    "currency": "EUR",
                }
            ]
        )
        invalid = assign_reconciliation_status(
            pd.DataFrame(
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
                        "concept_code": "BONUS",
                        "concept_name": "Bonus",
                        "amount": 100.0,
                        "currency": "EUR",
                    }
                ]
            ),
            dataframe,
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )
        self.assertEqual(
            invalid.comparison_with_diffs.iloc[0]["status"],
            "Invalid / Incomplete",
        )


if __name__ == "__main__":
    unittest.main()
