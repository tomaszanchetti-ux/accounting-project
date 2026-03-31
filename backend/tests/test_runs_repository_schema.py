from __future__ import annotations

import unittest
from unittest.mock import patch

from app.repositories.runs import PsycopgRunsRepository


class _FakeCursor:
    def __init__(self, table_refs: list[str | None]):
        self._table_refs = iter(table_refs)
        self.executed: list[tuple[str, tuple[object, ...] | None]] = []

    def __enter__(self) -> _FakeCursor:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def execute(self, query: str, params: tuple[object, ...] | None = None) -> None:
        self.executed.append((query, params))

    def fetchone(self) -> dict[str, str | None]:
        return {"table_ref": next(self._table_refs)}


class _FakeConnection:
    def __init__(self, cursor: _FakeCursor):
        self._cursor = cursor
        self.committed = False

    def __enter__(self) -> _FakeConnection:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def cursor(self) -> _FakeCursor:
        return self._cursor

    def commit(self) -> None:
        self.committed = True


class RunsRepositorySchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        PsycopgRunsRepository._schema_initialized = False

    def tearDown(self) -> None:
        PsycopgRunsRepository._schema_initialized = False

    def test_ensure_schema_skips_runtime_ddl_when_tables_already_exist(self) -> None:
        repository = PsycopgRunsRepository()
        cursor = _FakeCursor(
            [
                "reconciliation_runs",
                "uploaded_files",
                "expected_totals_used",
                "reconciliation_results",
                "reconciliation_exceptions",
                "run_payroll_lines",
            ]
        )
        connection = _FakeConnection(cursor)

        with patch("app.repositories.runs.get_db_connection", return_value=connection):
            repository.ensure_schema()

        self.assertTrue(PsycopgRunsRepository._schema_initialized)
        self.assertFalse(connection.committed)
        self.assertEqual(len(cursor.executed), 6)
        self.assertTrue(
            all("to_regclass" in query for query, _ in cursor.executed),
        )


if __name__ == "__main__":
    unittest.main()
