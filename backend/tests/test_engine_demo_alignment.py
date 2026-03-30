import unittest
from pathlib import Path

from app.services.reconciliation import assign_reconciliation_status


class EngineDemoAlignmentTest(unittest.TestCase):
    def test_demo_seed_matches_expected_narrative(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = assign_reconciliation_status(
            repo_root / "data/demo_seed/payroll.csv",
            repo_root / "data/demo_seed/expected_totals.csv",
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )

        rows = result.comparison_with_diffs.set_index("concept_code_normalized")

        expected_statuses = {
            "BASE_SALARY": "Reconciled",
            "BONUS": "Reconciled",
            "HEALTH_INSURANCE": "Reconciled",
            "INCOME_TAX": "Reconciled",
            "SOCIAL_SECURITY": "Reconciled",
            "OTHER_ADJUSTMENT": "Reconciled",
            "TRANSPORT": "Minor Difference",
            "OVERTIME": "Unreconciled",
            "MEAL_VOUCHER": "Unreconciled",
            "CHILDCARE": "Unreconciled",
        }

        for concept_code, expected_status in expected_statuses.items():
            self.assertEqual(rows.loc[concept_code, "status"], expected_status)

        status_counts = rows["status"].value_counts().to_dict()
        self.assertEqual(status_counts.get("Reconciled", 0), 6)
        self.assertEqual(status_counts.get("Minor Difference", 0), 1)
        self.assertEqual(status_counts.get("Unreconciled", 0), 3)


if __name__ == "__main__":
    unittest.main()
