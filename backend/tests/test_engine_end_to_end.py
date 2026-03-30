import unittest
from pathlib import Path

from app.schemas import ReconciliationEngineInput
from app.services.reconciliation import run_reconciliation_engine


class EngineEndToEndTest(unittest.TestCase):
    def test_engine_runs_end_to_end_with_demo_seed(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = run_reconciliation_engine(
            ReconciliationEngineInput(
                payroll=repo_root / "data/demo_seed/payroll.csv",
                expected_totals=repo_root / "data/demo_seed/expected_totals.csv",
                concept_master=repo_root / "data/demo_seed/concept_master.csv",
                target_period="2026-03",
            )
        )

        self.assertEqual(len(result.summary_rows), 10)
        self.assertEqual(result.run_metrics["concepts_reconciled"], 6)
        self.assertEqual(result.run_metrics["concepts_minor_difference"], 1)
        self.assertEqual(result.run_metrics["concepts_unreconciled"], 3)
        self.assertEqual(result.run_metrics["overall_run_status"], "unreconciled")

        keyed = {row.concept_code_normalized: row for row in result.summary_rows}
        self.assertEqual(keyed["TRANSPORT"].status, "Minor Difference")
        self.assertEqual(keyed["MEAL_VOUCHER"].status, "Unreconciled")
        self.assertEqual(keyed["BASE_SALARY"].status, "Reconciled")


if __name__ == "__main__":
    unittest.main()
