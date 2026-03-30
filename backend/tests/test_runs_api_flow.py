import unittest
from csv import DictReader
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from uuid import uuid4

import pandas as pd
from fastapi.testclient import TestClient

from app.api.routes.runs import get_runs_service
from app.main import app
from app.schemas.runs import (
    ExpectedTotalUsedRecord,
    RunExceptionRecord,
    RunPayrollLineRecord,
    RunRecord,
    RunResultRecord,
    UploadedFileRecord,
)
from app.services.runs import RunsService


class InMemoryRunsRepository:
    def __init__(self) -> None:
        self.runs: dict[str, RunRecord] = {}
        self.uploaded_files: dict[str, dict[str, UploadedFileRecord]] = {}
        self.expected_totals_used: dict[str, list[ExpectedTotalUsedRecord]] = {}
        self.results: dict[str, list[RunResultRecord]] = {}
        self.exceptions: dict[str, list[RunExceptionRecord]] = {}
        self.payroll_lines: dict[str, list[RunPayrollLineRecord]] = {}

    def create_run(
        self,
        *,
        run_label: str,
        period: str,
        legal_entity_scope: str | None = None,
        tolerance_profile_label: str | None = None,
        rules_version: str | None = None,
    ) -> RunRecord:
        run = RunRecord(
            id=str(uuid4()),
            run_label=run_label,
            period=period,
            status="DRAFT",
            legal_entity_scope=legal_entity_scope,
            tolerance_profile_label=tolerance_profile_label,
            rules_version=rules_version,
            created_at=datetime.now(timezone.utc),
        )
        self.runs[run.id] = run
        return run

    def get_run(self, run_id: str) -> RunRecord | None:
        return self.runs.get(run_id)

    def update_run_status(
        self,
        run_id: str,
        *,
        status: str,
        overall_status: str | None = None,
        completed_at: datetime | None = None,
        error_message: str | None = None,
    ) -> RunRecord | None:
        run = self.runs.get(run_id)
        if not run:
            return None

        updated = run.model_copy(
            update={
                "status": status,
                "overall_status": overall_status
                if overall_status is not None
                else run.overall_status,
                "completed_at": completed_at if completed_at is not None else run.completed_at,
                "error_message": error_message,
            }
        )
        self.runs[run_id] = updated
        return updated

    def upsert_uploaded_file(
        self,
        *,
        run_id: str,
        file_name: str,
        file_type: str,
        source_kind: str,
        storage_path: str,
        storage_bucket: str | None = None,
    ) -> UploadedFileRecord:
        uploaded = UploadedFileRecord(
            id=str(uuid4()),
            run_id=run_id,
            file_name=file_name,
            file_type=file_type,
            source_kind=source_kind,
            storage_bucket=storage_bucket,
            storage_path=storage_path,
            uploaded_at=datetime.now(timezone.utc),
        )
        self.uploaded_files.setdefault(run_id, {})[file_type] = uploaded
        return uploaded

    def list_uploaded_files(self, run_id: str) -> list[UploadedFileRecord]:
        return list(self.uploaded_files.get(run_id, {}).values())

    def persist_run_execution(
        self,
        *,
        run_id: str,
        expected_totals_used: list[ExpectedTotalUsedRecord],
        results: list[RunResultRecord],
        exceptions: list[RunExceptionRecord],
        payroll_lines: list[RunPayrollLineRecord],
        final_status: str,
        overall_status: str,
        source_file_name: str | None,
        record_count: int,
        concept_count: int,
        run_metrics: dict[str, str | int | float | bool | None],
        completed_at: datetime,
    ) -> RunRecord:
        self.expected_totals_used[run_id] = expected_totals_used
        self.results[run_id] = results
        self.exceptions[run_id] = exceptions
        self.payroll_lines[run_id] = payroll_lines

        run = self.runs[run_id]
        updated = run.model_copy(
            update={
                "status": final_status,
                "overall_status": overall_status,
                "source_file_name": source_file_name,
                "record_count": record_count,
                "concept_count": concept_count,
                "run_metrics": run_metrics,
                "completed_at": completed_at,
                "error_message": None,
            }
        )
        self.runs[run_id] = updated
        return updated

    def list_results(self, run_id: str) -> list[RunResultRecord]:
        items = list(self.results.get(run_id, []))
        order = {
            "Invalid / Incomplete": 1,
            "Unreconciled": 2,
            "Minor Difference": 3,
            "Reconciled": 4,
        }
        return sorted(
            items,
            key=lambda item: (
                order.get(item.status, 99),
                abs(item.absolute_diff),
                item.concept_code_normalized,
            ),
            reverse=False,
        )

    def get_result(self, run_id: str, result_id: str) -> RunResultRecord | None:
        return next(
            (
                result
                for result in self.results.get(run_id, [])
                if result.id == result_id
            ),
            None,
        )

    def list_exceptions(
        self,
        run_id: str,
        *,
        result_id: str | None = None,
    ) -> list[RunExceptionRecord]:
        items = list(self.exceptions.get(run_id, []))
        if result_id is None:
            return items
        return [item for item in items if item.result_id == result_id]

    def list_payroll_lines(
        self,
        run_id: str,
        *,
        concept_code_normalized: str | None = None,
    ) -> list[RunPayrollLineRecord]:
        items = list(self.payroll_lines.get(run_id, []))
        if concept_code_normalized is None:
            return items
        return [
            item
            for item in items
            if item.concept_code_normalized == concept_code_normalized
        ]


class InMemoryStorageGateway:
    def __init__(self) -> None:
        self.files: dict[tuple[str, str], bytes] = {}

    def build_input_path(self, run_id: str, filename: str) -> str:
        return f"runs/{run_id}/inputs/{filename}"

    def upload_input_file(
        self,
        *,
        run_id: str,
        filename: str,
        file_bytes: bytes,
        content_type: str,
    ) -> tuple[str, str]:
        del content_type
        bucket_name = "test-raw-inputs"
        storage_path = self.build_input_path(run_id, filename)
        self.files[(bucket_name, storage_path)] = file_bytes
        return bucket_name, storage_path

    def download_file(self, bucket_name: str, storage_path: str) -> bytes:
        return self.files[(bucket_name, storage_path)]


class RunsApiFlowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryRunsRepository()
        self.storage_gateway = InMemoryStorageGateway()
        app.dependency_overrides[get_runs_service] = lambda: RunsService(
            self.repository,
            storage_gateway=self.storage_gateway,
        )
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()

    def test_create_upload_execute_and_query_run_flow(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        create_response = self.client.post(
            "/runs",
            json={
                "run_label": "Demo March 2026",
                "period": "2026-03",
            },
        )
        self.assertEqual(create_response.status_code, 201)
        run_id = create_response.json()["run"]["id"]

        file_refs = {
            "payroll": repo_root / "data/demo_seed/payroll.csv",
            "expected_totals": repo_root / "data/demo_seed/expected_totals.csv",
            "concept_master": repo_root / "data/demo_seed/concept_master.csv",
            "employee_reference": repo_root / "data/demo_seed/employee_reference.csv",
        }

        for file_type, path in file_refs.items():
            response = self.client.post(
                f"/runs/{run_id}/upload",
                json={
                    "file_name": path.name,
                    "file_type": file_type,
                    "storage_path": str(path),
                    "source_kind": "local_path",
                },
            )
            self.assertEqual(response.status_code, 201)

        execute_response = self.client.post(
            f"/runs/{run_id}/execute",
            json={},
        )
        self.assertEqual(execute_response.status_code, 200)
        execute_payload = execute_response.json()
        self.assertEqual(
            execute_payload["run"]["status"],
            "RECONCILED_WITH_EXCEPTIONS",
        )
        self.assertEqual(execute_payload["run"]["overall_status"], "unreconciled")
        expected_record_count = len(pd.read_csv(file_refs["payroll"]))
        self.assertEqual(execute_payload["run"]["record_count"], expected_record_count)
        self.assertEqual(execute_payload["run"]["concept_count"], 10)

        summary_response = self.client.get(f"/runs/{run_id}/summary")
        self.assertEqual(summary_response.status_code, 200)
        summary_payload = summary_response.json()
        self.assertEqual(summary_payload["metrics"]["overall_run_status"], "unreconciled")
        self.assertEqual(summary_payload["metrics"]["concepts_reconciled"], 6)
        self.assertEqual(len(summary_payload["preview_results"]), 5)
        self.assertGreaterEqual(len(summary_payload["event_log"]), 4)

        results_response = self.client.get(f"/runs/{run_id}/results")
        self.assertEqual(results_response.status_code, 200)
        results_payload = results_response.json()
        self.assertEqual(results_payload["total_results"], 10)
        meal_voucher = next(
            result
            for result in results_payload["results"]
            if result["concept_code_normalized"] == "MEAL_VOUCHER"
        )
        self.assertEqual(meal_voucher["status"], "Unreconciled")

        detail_response = self.client.get(
            f"/runs/{run_id}/results/{meal_voucher['id']}"
        )
        self.assertEqual(detail_response.status_code, 200)
        detail_payload = detail_response.json()
        self.assertEqual(
            detail_payload["result"]["concept_code_normalized"],
            "MEAL_VOUCHER",
        )
        self.assertGreater(len(detail_payload["exceptions"]), 0)
        self.assertEqual(
            detail_payload["concept_analysis"]["header"]["concept_code_normalized"],
            "MEAL_VOUCHER",
        )
        self.assertGreater(
            detail_payload["concept_analysis"]["evidence_summary"]["total_exceptions"],
            0,
        )
        self.assertGreaterEqual(len(detail_payload["event_log"]), 4)

        drilldown_response = self.client.get(
            f"/runs/{run_id}/results/{meal_voucher['id']}/drilldown"
        )
        self.assertEqual(drilldown_response.status_code, 200)
        drilldown_payload = drilldown_response.json()
        self.assertGreater(drilldown_payload["total_rows"], 0)
        self.assertEqual(
            drilldown_payload["summary"]["concept_code_normalized"],
            "MEAL_VOUCHER",
        )
        self.assertGreater(
            len(drilldown_payload["filter_context"]["available_exception_types"]),
            0,
        )
        self.assertTrue(
            any(
                "Out-of-Period Record" in row["exception_flags"]
                for row in drilldown_payload["rows"]
            )
        )
        self.assertEqual(len(self.repository.uploaded_files[run_id]), 4)
        self.assertEqual(len(self.repository.results[run_id]), 10)
        self.assertGreater(len(self.repository.exceptions[run_id]), 0)
        self.assertIn("overall_run_status", self.repository.runs[run_id].run_metrics)

        summary_export_response = self.client.get(f"/runs/{run_id}/exports/summary")
        self.assertEqual(summary_export_response.status_code, 200)
        self.assertIn(
            "attachment; filename=",
            summary_export_response.headers["content-disposition"],
        )
        summary_rows = list(DictReader(StringIO(summary_export_response.text)))
        self.assertEqual(len(summary_rows), 10)
        self.assertTrue(
            any(row["concept_code"] == "MEAL_VOUCHER" for row in summary_rows)
        )

        detail_export_response = self.client.get(
            f"/runs/{run_id}/results/{meal_voucher['id']}/exports/detail"
        )
        self.assertEqual(detail_export_response.status_code, 200)
        self.assertIn(
            "attachment; filename=",
            detail_export_response.headers["content-disposition"],
        )
        detail_rows = list(DictReader(StringIO(detail_export_response.text)))
        self.assertGreater(len(detail_rows), 0)
        self.assertTrue(
            all(row["concept_code"] == "MEAL_VOUCHER" for row in detail_rows)
        )
        self.assertTrue(
            any(
                "Out-of-Period Record" in row["exception_type"]
                for row in detail_rows
            )
        )

    def test_multipart_upload_persists_to_storage_and_is_executable(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        create_response = self.client.post(
            "/runs",
            json={
                "run_label": "Multipart Demo",
                "period": "2026-03",
            },
        )
        self.assertEqual(create_response.status_code, 201)
        run_id = create_response.json()["run"]["id"]

        for file_type, path in {
            "payroll": repo_root / "data/demo_seed/payroll.csv",
            "expected_totals": repo_root / "data/demo_seed/expected_totals.csv",
            "concept_master": repo_root / "data/demo_seed/concept_master.csv",
        }.items():
            with path.open("rb") as file_handle:
                response = self.client.post(
                    f"/runs/{run_id}/upload",
                    data={"file_type": file_type},
                    files={"file": (path.name, file_handle, "text/csv")},
                )
            self.assertEqual(response.status_code, 201)
            payload = response.json()["uploaded_file"]
            self.assertEqual(payload["source_kind"], "supabase_storage")
            self.assertEqual(payload["storage_bucket"], "test-raw-inputs")

        execute_response = self.client.post(f"/runs/{run_id}/execute", json={})
        self.assertEqual(execute_response.status_code, 200)
        execute_payload = execute_response.json()
        self.assertEqual(
            execute_payload["run"]["status"],
            "RECONCILED_WITH_EXCEPTIONS",
        )
        self.assertEqual(execute_payload["run"]["overall_status"], "unreconciled")


if __name__ == "__main__":
    unittest.main()
