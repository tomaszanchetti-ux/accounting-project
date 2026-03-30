# ruff: noqa: E402

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.db import get_db_connection
from app.repositories import PsycopgRunsRepository
from app.schemas.runs import RunCreateRequest, RunExecuteRequest, RunFileReferenceRequest
from app.services.runs import RunsService

DEMO_PERIOD = "2026-03"
CANONICAL_RUN_LABEL = "Demo March 2026 - Canonical Walkthrough"
EXPECTED_STATUSES = {
    "MEAL_VOUCHER": "Unreconciled",
    "CHILDCARE": "Unreconciled",
    "OVERTIME": "Unreconciled",
    "TRANSPORT": "Minor Difference",
}
EXPECTED_STATUS_COUNTS = {
    "Reconciled": 6,
    "Minor Difference": 1,
    "Unreconciled": 3,
}
FILE_MAP = {
    "payroll": REPO_ROOT / "data" / "demo_seed" / "payroll.csv",
    "expected_totals": REPO_ROOT / "data" / "demo_seed" / "expected_totals.csv",
    "concept_master": REPO_ROOT / "data" / "demo_seed" / "concept_master.csv",
    "employee_reference": REPO_ROOT / "data" / "demo_seed" / "employee_reference.csv",
}


def get_repository() -> PsycopgRunsRepository:
    repository = PsycopgRunsRepository()
    repository.ensure_schema()
    return repository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create or reset the canonical demo run for the Accounting MVP."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser(
        "create",
        help="Create the canonical demo run from local demo_seed files.",
    )
    create_parser.add_argument(
        "--run-label",
        default=CANONICAL_RUN_LABEL,
        help="Label to use for the demo run.",
    )
    create_parser.add_argument(
        "--period",
        default=DEMO_PERIOD,
        help="Target period for the demo run.",
    )
    create_parser.add_argument(
        "--reset-first",
        action="store_true",
        help="Delete existing runs with the same label and period before creating a new one.",
    )
    create_parser.add_argument(
        "--allow-duplicates",
        action="store_true",
        help="Allow creating a new demo run even if one with the same label already exists.",
    )

    reset_parser = subparsers.add_parser(
        "reset",
        help="Delete existing canonical demo runs for the selected label and period.",
    )
    reset_parser.add_argument(
        "--run-label",
        default=CANONICAL_RUN_LABEL,
        help="Label of the demo run(s) to remove.",
    )
    reset_parser.add_argument(
        "--period",
        default=DEMO_PERIOD,
        help="Period of the demo run(s) to remove.",
    )

    list_parser = subparsers.add_parser(
        "list",
        help="List existing canonical demo runs for the selected label and period.",
    )
    list_parser.add_argument(
        "--run-label",
        default=CANONICAL_RUN_LABEL,
        help="Label of the demo run(s) to list.",
    )
    list_parser.add_argument(
        "--period",
        default=DEMO_PERIOD,
        help="Period of the demo run(s) to list.",
    )

    return parser


def validate_demo_seed_files() -> None:
    missing_paths = [path for path in FILE_MAP.values() if not path.exists()]
    if missing_paths:
        missing_display = ", ".join(str(path) for path in missing_paths)
        raise FileNotFoundError(f"Missing demo seed files: {missing_display}")


def list_demo_runs(*, run_label: str, period: str) -> list[dict[str, str]]:
    get_repository()
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, run_label, period, status, overall_status, created_at
                FROM reconciliation_runs
                WHERE run_label = %s
                  AND period = %s
                ORDER BY created_at DESC
                """,
                (run_label, period),
            )
            rows = cursor.fetchall()

    return rows


def reset_demo_runs(*, run_label: str, period: str) -> int:
    get_repository()
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM reconciliation_runs
                WHERE run_label = %s
                  AND period = %s
                RETURNING id
                """,
                (run_label, period),
            )
            deleted_rows = cursor.fetchall()
        connection.commit()

    return len(deleted_rows)


def create_demo_run(
    *,
    run_label: str,
    period: str,
    reset_first: bool,
    allow_duplicates: bool,
) -> str:
    validate_demo_seed_files()
    existing_runs = list_demo_runs(run_label=run_label, period=period)
    if existing_runs and not reset_first and not allow_duplicates:
        raise RuntimeError(
            "A demo run with the same label already exists. "
            "Use 'reset' or rerun with --reset-first."
        )

    if reset_first:
        removed = reset_demo_runs(run_label=run_label, period=period)
        print(f"Removed {removed} existing demo run(s) before create.")

    service = RunsService(get_repository())
    run_response = service.create_run(
        RunCreateRequest(
            run_label=run_label,
            period=period,
        )
    )
    run_id = run_response.run.id

    for file_type, path in FILE_MAP.items():
        service.register_file_reference(
            run_id,
            RunFileReferenceRequest(
                file_name=path.name,
                file_type=file_type,
                storage_path=str(path),
                source_kind="local_path",
            ),
        )

    execute_response = service.execute_run(
        run_id,
        RunExecuteRequest(),
    )
    results = service.list_results(run_id).results
    result_by_concept = {
        result.concept_code_normalized: result.status for result in results
    }

    for concept_code, expected_status in EXPECTED_STATUSES.items():
        actual_status = result_by_concept.get(concept_code)
        if actual_status != expected_status:
            raise RuntimeError(
                f"Concept {concept_code} expected status {expected_status}, got {actual_status}."
            )

    status_counts = Counter(result.status for result in results)
    for status_name, expected_count in EXPECTED_STATUS_COUNTS.items():
        if status_counts.get(status_name, 0) != expected_count:
            raise RuntimeError(
                f"Expected {expected_count} result(s) with status {status_name}, "
                f"got {status_counts.get(status_name, 0)}."
            )

    print(f"Created demo run: {run_id}")
    print(f"Run label: {run_label}")
    print(f"Period: {period}")
    print(f"Run status: {execute_response.run.status}")
    print(f"Overall status: {execute_response.run.overall_status}")
    print("Narrative checkpoints:")
    for concept_code in ("MEAL_VOUCHER", "CHILDCARE", "OVERTIME", "TRANSPORT"):
        print(f"  - {concept_code}: {result_by_concept[concept_code]}")

    return run_id


def print_demo_runs(*, run_label: str, period: str) -> None:
    runs = list_demo_runs(run_label=run_label, period=period)
    if not runs:
        print("No demo runs found.")
        return

    for run in runs:
        print(
            f"{run['id']} | {run['created_at']} | "
            f"{run['status']} | {run['overall_status']} | {run['run_label']}"
        )


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "create":
            create_demo_run(
                run_label=args.run_label,
                period=args.period,
                reset_first=args.reset_first,
                allow_duplicates=args.allow_duplicates,
            )
        elif args.command == "reset":
            removed = reset_demo_runs(run_label=args.run_label, period=args.period)
            print(f"Removed {removed} demo run(s).")
        elif args.command == "list":
            print_demo_runs(run_label=args.run_label, period=args.period)
        else:
            parser.error(f"Unknown command: {args.command}")
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
