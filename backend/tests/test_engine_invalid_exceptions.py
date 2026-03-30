import unittest
from pathlib import Path

import pandas as pd

from app.schemas import ReconciliationEngineInput
from app.services.reconciliation import (
    EXCEPTION_PRIORITY_ORDER,
    build_concept_explanations,
    build_exception_impact_summary,
    build_ranked_exception_causes,
    build_structured_exception_items,
    detect_duplicate_records,
    detect_invalid_data_quality_issues,
    detect_misclassified_concepts,
    detect_missing_expected_totals,
    detect_missing_population,
    detect_out_of_period_records,
    detect_outlier_amounts,
    detect_sign_errors,
    detect_unmapped_concept_records,
    run_reconciliation_engine,
)


class EngineInvalidExceptionsTest(unittest.TestCase):
    def test_invalid_data_quality_issues_are_structured_per_record_cause(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        payroll = pd.DataFrame(
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
                    "amount": "abc",
                    "currency": "EUR",
                },
                {
                    "record_id": "R2",
                    "employee_id": "",
                    "employee_name": "Luis",
                    "legal_entity": "ARD Spain SL",
                    "country": "Spain",
                    "cost_center": "OPS",
                    "payroll_period": "2026-03",
                    "posting_date": "2026-03-31",
                    "concept_code": "MEAL_VOUCHER",
                    "concept_name": "Meal Voucher",
                    "amount": 100.0,
                    "currency": "EUR",
                },
            ]
        )

        result = detect_invalid_data_quality_issues(
            payroll,
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )

        self.assertEqual(result.invalid_record_count, 2)
        self.assertEqual(len(result.invalid_exceptions), 2)
        rows = result.invalid_exceptions.set_index("record_id")
        self.assertEqual(rows.loc["R1", "issue_code"], "invalid_amount")
        self.assertTrue(rows.loc["R1", "blocking"])
        self.assertEqual(rows.loc["R2", "issue_code"], "missing_employee_id")
        self.assertFalse(rows.loc["R2", "blocking"])

    def test_detection_distinguishes_blocking_vs_partial_invalidation(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        partial_only = pd.DataFrame(
            [
                {
                    "record_id": "R1",
                    "employee_id": "",
                    "employee_name": "Ana",
                    "legal_entity": "ARD Spain SL",
                    "country": "Spain",
                    "cost_center": "OPS",
                    "payroll_period": "2026-03",
                    "posting_date": "2026-03-31",
                    "concept_code": "MEAL_VOUCHER",
                    "concept_name": "Meal Voucher",
                    "amount": 100.0,
                    "currency": "EUR",
                }
            ]
        )
        partial_result = detect_invalid_data_quality_issues(
            partial_only,
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )
        self.assertFalse(partial_result.run_has_blocking_data_quality_issues)
        self.assertTrue(partial_result.has_partial_invalidation_only)

        blocking = partial_only.astype({"amount": "object"}).copy()
        blocking.loc[0, "amount"] = "abc"
        blocking_result = detect_invalid_data_quality_issues(
            blocking,
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )
        self.assertTrue(blocking_result.run_has_blocking_data_quality_issues)
        self.assertFalse(blocking_result.has_partial_invalidation_only)

    def test_engine_exposes_invalid_data_quality_artifacts_and_metrics(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        payroll = pd.DataFrame(
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
                    "amount": "abc",
                    "currency": "EUR",
                }
            ]
        )
        expected = pd.DataFrame(
            [
                {
                    "payroll_period": "2026-03",
                    "concept_code": "MEAL_VOUCHER",
                    "expected_amount": 100.0,
                    "currency": "EUR",
                }
            ]
        )

        result = run_reconciliation_engine(
            ReconciliationEngineInput(
                payroll=payroll,
                expected_totals=expected,
                concept_master=repo_root / "data/demo_seed/concept_master.csv",
                target_period="2026-03",
            )
        )

        self.assertEqual(result.run_metrics["invalid_record_count"], 1)
        self.assertEqual(result.run_metrics["blocking_data_quality_issue_count"], 1)
        self.assertTrue(result.run_metrics["run_has_blocking_data_quality_issues"])
        self.assertIsNotNone(result.debug_artifacts.invalid_data_quality_exceptions)
        self.assertEqual(
            len(result.debug_artifacts.invalid_data_quality_exceptions),
            1,
        )

    def test_out_of_period_detection_supports_period_and_posting_date_signals(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        payroll = pd.DataFrame(
            [
                {
                    "record_id": "R1",
                    "employee_id": "EMP1",
                    "employee_name": "Ana",
                    "legal_entity": "ARD Spain SL",
                    "country": "Spain",
                    "cost_center": "OPS",
                    "payroll_period": "2026-02",
                    "posting_date": "2026-02-28",
                    "concept_code": "MEAL_VOUCHER",
                    "concept_name": "Meal Voucher",
                    "amount": 100.0,
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
                    "posting_date": "2026-02-28",
                    "concept_code": "MEAL_VOUCHER",
                    "concept_name": "Meal Voucher",
                    "amount": 250.0,
                    "currency": "EUR",
                },
            ]
        )

        result = detect_out_of_period_records(
            payroll,
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )

        self.assertEqual(result.out_of_period_record_count, 2)
        self.assertEqual(result.total_estimated_impact_amount, 350.0)
        rows = result.out_of_period_exceptions.set_index("record_id")
        self.assertEqual(
            rows.loc["R1", "temporal_mismatch_source"],
            "payroll_period_and_posting_date",
        )
        self.assertEqual(rows.loc["R2", "temporal_mismatch_source"], "posting_date")

    def test_demo_seed_out_of_period_impact_is_aggregated_by_concept(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = detect_out_of_period_records(
            repo_root / "data/demo_seed/payroll.csv",
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )

        self.assertEqual(result.out_of_period_record_count, 8)
        self.assertEqual(result.total_estimated_impact_amount, 600.0)
        self.assertEqual(len(result.impact_by_concept), 1)
        self.assertEqual(
            result.impact_by_concept.iloc[0]["concept_code_normalized"],
            "MEAL_VOUCHER",
        )
        self.assertEqual(
            result.impact_by_concept.iloc[0]["out_of_period_record_count"],
            8,
        )

    def test_engine_exposes_out_of_period_artifacts_and_metrics(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = run_reconciliation_engine(
            ReconciliationEngineInput(
                payroll=repo_root / "data/demo_seed/payroll.csv",
                expected_totals=repo_root / "data/demo_seed/expected_totals.csv",
                concept_master=repo_root / "data/demo_seed/concept_master.csv",
                target_period="2026-03",
            )
        )

        self.assertEqual(result.run_metrics["out_of_period_record_count"], 8)
        self.assertEqual(
            result.run_metrics["out_of_period_total_estimated_impact_amount"],
            600.0,
        )
        self.assertIsNotNone(result.debug_artifacts.out_of_period_exceptions)
        self.assertIsNotNone(result.debug_artifacts.out_of_period_impact_by_concept)

    def test_demo_seed_unmapped_concept_detection_groups_raw_patterns(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = detect_unmapped_concept_records(
            repo_root / "data/demo_seed/payroll.csv",
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )

        self.assertEqual(result.unmapped_record_count, 5)
        self.assertEqual(len(result.impact_by_raw_concept), 1)
        self.assertEqual(result.impact_by_raw_concept.iloc[0]["concept_code"], "MEAL_VCHR")

    def test_demo_seed_duplicate_record_detection_identifies_groups_and_impact(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = detect_duplicate_records(
            repo_root / "data/demo_seed/payroll.csv",
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )

        self.assertEqual(result.duplicate_group_count, 3)
        self.assertEqual(result.duplicate_record_count, 6)
        self.assertAlmostEqual(result.total_estimated_duplicate_impact_amount, 238.5)
        self.assertEqual(len(result.impact_by_concept), 1)
        self.assertEqual(
            result.impact_by_concept.iloc[0]["concept_code_normalized"],
            "MEAL_VOUCHER",
        )

    def test_missing_expected_total_detects_observed_units_without_reference(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        payroll = pd.DataFrame(
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
        )
        expected = pd.DataFrame(
            [
                {
                    "payroll_period": "2026-03",
                    "concept_code": "BASE_SALARY",
                    "expected_amount": 100.0,
                    "currency": "EUR",
                }
            ]
        )

        result = detect_missing_expected_totals(
            payroll,
            expected,
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )

        self.assertEqual(result.missing_expected_count, 1)
        self.assertEqual(result.total_observed_amount_without_expected, 100.0)
        self.assertEqual(
            result.missing_expected_exceptions.iloc[0]["concept_code_normalized"],
            "BONUS",
        )

    def test_engine_exposes_unmapped_duplicate_and_missing_expected_artifacts(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = run_reconciliation_engine(
            ReconciliationEngineInput(
                payroll=repo_root / "data/demo_seed/payroll.csv",
                expected_totals=repo_root / "data/demo_seed/expected_totals.csv",
                concept_master=repo_root / "data/demo_seed/concept_master.csv",
                target_period="2026-03",
            )
        )

        self.assertEqual(result.run_metrics["unmapped_record_count"], 5)
        self.assertEqual(result.run_metrics["duplicate_group_count"], 3)
        self.assertEqual(result.run_metrics["missing_expected_total_count"], 0)
        self.assertIsNotNone(result.debug_artifacts.unmapped_concept_exceptions)
        self.assertIsNotNone(result.debug_artifacts.duplicate_record_exceptions)
        self.assertIsNotNone(result.debug_artifacts.missing_expected_total_exceptions)

    def test_demo_seed_outlier_detection_identifies_dominant_overtime_record(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = detect_outlier_amounts(
            repo_root / "data/demo_seed/payroll.csv",
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )

        self.assertEqual(result.outlier_record_count, 1)
        self.assertEqual(result.total_estimated_outlier_impact_amount, 950.0)
        self.assertEqual(
            result.outlier_exceptions.iloc[0]["concept_code_normalized"],
            "OVERTIME",
        )

    def test_missing_population_uses_employee_reference_for_childcare(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = detect_missing_population(
            repo_root / "data/demo_seed/payroll.csv",
            repo_root / "data/demo_seed/expected_totals.csv",
            repo_root / "data/demo_seed/concept_master.csv",
            repo_root / "data/demo_seed/employee_reference.csv",
            target_period="2026-03",
        )

        self.assertEqual(result.missing_population_record_count, 6)
        self.assertEqual(
            result.total_estimated_missing_population_impact_amount,
            1450.0,
        )
        self.assertEqual(
            result.missing_population_exceptions.iloc[0]["concept_code_normalized"],
            "CHILDCARE",
        )

    def test_engine_exposes_outlier_and_missing_population_artifacts(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = run_reconciliation_engine(
            ReconciliationEngineInput(
                payroll=repo_root / "data/demo_seed/payroll.csv",
                expected_totals=repo_root / "data/demo_seed/expected_totals.csv",
                concept_master=repo_root / "data/demo_seed/concept_master.csv",
                employee_reference=repo_root / "data/demo_seed/employee_reference.csv",
                target_period="2026-03",
            )
        )

        self.assertEqual(result.run_metrics["outlier_record_count"], 1)
        self.assertEqual(
            result.run_metrics["missing_population_record_count"],
            6,
        )
        self.assertIsNotNone(result.debug_artifacts.outlier_amount_exceptions)
        self.assertIsNotNone(result.debug_artifacts.missing_population_exceptions)

    def test_structured_exception_items_follow_priority_contract(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        invalid_detection = detect_invalid_data_quality_issues(
            pd.DataFrame(
                [
                    {
                        "record_id": "R1",
                        "employee_id": "EMP1",
                        "employee_name": "Ana",
                        "legal_entity": "ARD Spain SL",
                        "country": "Spain",
                        "cost_center": "OPS",
                        "payroll_period": "2026-02",
                        "posting_date": "2026-02-28",
                        "concept_code": "MEAL_VOUCHER",
                        "concept_name": "Meal Voucher",
                        "amount": "abc",
                        "currency": "EUR",
                    }
                ]
            ),
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )
        structured = build_structured_exception_items(
            invalid_detection=invalid_detection,
            out_of_period_detection=detect_out_of_period_records(
                repo_root / "data/demo_seed/payroll.csv",
                repo_root / "data/demo_seed/concept_master.csv",
                target_period="2026-03",
            ),
            unmapped_detection=detect_unmapped_concept_records(
                repo_root / "data/demo_seed/payroll.csv",
                repo_root / "data/demo_seed/concept_master.csv",
                target_period="2026-03",
            ),
            duplicate_detection=detect_duplicate_records(
                repo_root / "data/demo_seed/payroll.csv",
                repo_root / "data/demo_seed/concept_master.csv",
                target_period="2026-03",
            ),
            missing_expected_detection=detect_missing_expected_totals(
                repo_root / "data/demo_seed/payroll.csv",
                repo_root / "data/demo_seed/expected_totals.csv",
                repo_root / "data/demo_seed/concept_master.csv",
                target_period="2026-03",
            ),
            outlier_detection=detect_outlier_amounts(
                repo_root / "data/demo_seed/payroll.csv",
                repo_root / "data/demo_seed/concept_master.csv",
                target_period="2026-03",
            ),
            missing_population_detection=detect_missing_population(
                repo_root / "data/demo_seed/payroll.csv",
                repo_root / "data/demo_seed/expected_totals.csv",
                repo_root / "data/demo_seed/concept_master.csv",
                repo_root / "data/demo_seed/employee_reference.csv",
                target_period="2026-03",
            ),
        )

        self.assertGreater(len(structured), 0)
        self.assertEqual(structured[0].exception_type, EXCEPTION_PRIORITY_ORDER[0])
        self.assertEqual(structured[0].scope_level, "record")

    def test_engine_exposes_structured_exceptions_bundle(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = run_reconciliation_engine(
            ReconciliationEngineInput(
                payroll=repo_root / "data/demo_seed/payroll.csv",
                expected_totals=repo_root / "data/demo_seed/expected_totals.csv",
                concept_master=repo_root / "data/demo_seed/concept_master.csv",
                employee_reference=repo_root / "data/demo_seed/employee_reference.csv",
                target_period="2026-03",
            )
        )

        self.assertGreater(len(result.debug_artifacts.structured_exceptions), 0)
        self.assertEqual(
            result.debug_artifacts.structured_exceptions[0].exception_type,
            "Out-of-Period Record",
        )

    def test_impact_summary_and_ranking_match_demo_wow_cases(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = run_reconciliation_engine(
            ReconciliationEngineInput(
                payroll=repo_root / "data/demo_seed/payroll.csv",
                expected_totals=repo_root / "data/demo_seed/expected_totals.csv",
                concept_master=repo_root / "data/demo_seed/concept_master.csv",
                employee_reference=repo_root / "data/demo_seed/employee_reference.csv",
                target_period="2026-03",
            )
        )

        impact_summary = build_exception_impact_summary(
            result.debug_artifacts.structured_exceptions
        )
        ranked = build_ranked_exception_causes(
            result.debug_artifacts.structured_exceptions
        )

        overtime_outlier = impact_summary.loc[
            (impact_summary["concept_scope"] == "OVERTIME")
            & (impact_summary["exception_type"] == "Outlier Amount")
        ].iloc[0]
        childcare_missing_population = impact_summary.loc[
            (impact_summary["concept_scope"] == "CHILDCARE")
            & (
                impact_summary["exception_type"]
                == "Missing Record / Missing Population"
            )
        ].iloc[0]

        self.assertEqual(overtime_outlier["estimated_impact_amount"], 950.0)
        self.assertEqual(
            childcare_missing_population["estimated_impact_amount"],
            1450.0,
        )

        top_ranked = ranked.groupby("concept_scope").first()
        self.assertEqual(top_ranked.loc["OVERTIME", "exception_type"], "Outlier Amount")
        self.assertEqual(
            top_ranked.loc["CHILDCARE", "exception_type"],
            "Missing Record / Missing Population",
        )

    def test_concept_explanations_cover_wow_cases(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        result = run_reconciliation_engine(
            ReconciliationEngineInput(
                payroll=repo_root / "data/demo_seed/payroll.csv",
                expected_totals=repo_root / "data/demo_seed/expected_totals.csv",
                concept_master=repo_root / "data/demo_seed/concept_master.csv",
                employee_reference=repo_root / "data/demo_seed/employee_reference.csv",
                target_period="2026-03",
            )
        )

        explanations = build_concept_explanations(
            result.summary_rows,
            result.debug_artifacts.ranked_exception_causes,
            result.debug_artifacts.structured_exceptions,
        )
        keyed = {item.concept_code_normalized: item for item in explanations}

        self.assertIn("Outlier Amount", keyed["OVERTIME"].probable_causes[0].exception_type)
        self.assertIn(
            "Missing Record / Missing Population",
            keyed["CHILDCARE"].probable_causes[0].exception_type,
        )
        meal_voucher_causes = [
            cause.exception_type for cause in keyed["MEAL_VOUCHER"].probable_causes
        ]
        self.assertIn("Out-of-Period Record", meal_voucher_causes)
        self.assertIn("Unmapped Concept", meal_voucher_causes)
        self.assertIn("Duplicate Record", meal_voucher_causes)
        self.assertIsNotNone(keyed["MEAL_VOUCHER"].recommended_action)
        self.assertIn(
            "Missing Record / Missing Population",
            keyed["CHILDCARE"].probable_causes[0].exception_type,
        )
        self.assertIn("eligible employees", keyed["CHILDCARE"].recommended_action)
        self.assertIn("Outlier Amount", keyed["OVERTIME"].probable_causes[0].exception_type)
        self.assertIn("outlier", keyed["OVERTIME"].recommended_action.lower())
        self.assertIn("minor difference", keyed["TRANSPORT"].summary_statement.lower())
        self.assertIsNone(keyed["TRANSPORT"].recommended_action)

    def test_sign_error_detection_flags_unexpected_polarity(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        payroll = pd.DataFrame(
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
                    "concept_code": "BASE_SALARY",
                    "concept_name": "Base Salary",
                    "amount": -100.0,
                    "currency": "EUR",
                }
            ]
        )
        result = detect_sign_errors(
            payroll,
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )

        self.assertEqual(result.sign_error_record_count, 1)
        self.assertEqual(
            result.sign_error_exceptions.iloc[0]["concept_code_normalized"],
            "BASE_SALARY",
        )

    def test_misclassified_detection_requires_explicit_configuration(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        configured = detect_misclassified_concepts(
            repo_root / "data/demo_seed/payroll.csv",
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
            configured_raw_concept_codes={"MEAL_VCHR"},
        )
        default = detect_misclassified_concepts(
            repo_root / "data/demo_seed/payroll.csv",
            repo_root / "data/demo_seed/concept_master.csv",
            target_period="2026-03",
        )

        self.assertEqual(default.misclassified_record_count, 0)
        self.assertGreater(configured.misclassified_record_count, 0)


if __name__ == "__main__":
    unittest.main()
