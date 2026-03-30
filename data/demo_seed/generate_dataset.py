from __future__ import annotations

import csv
from pathlib import Path


PAYROLL_PERIOD = "2026-03"
OUTPUT_DIR = Path(__file__).resolve().parent


FIRST_NAMES = [
    "Alicia",
    "Bruno",
    "Carla",
    "Diego",
    "Elena",
    "Fabian",
    "Gabriela",
    "Hector",
    "Ines",
    "Javier",
    "Karina",
    "Lucas",
    "Marta",
    "Nicolas",
    "Olga",
    "Pablo",
    "Raquel",
    "Sergio",
    "Tamara",
    "Valentin",
]

LAST_NAMES = [
    "Alonso",
    "Benitez",
    "Cabrera",
    "Dominguez",
    "Estevez",
    "Fernandez",
    "Garrido",
    "Herrera",
    "Iglesias",
    "Jimenez",
    "Lorenzo",
    "Martinez",
    "Navarro",
    "Ortega",
    "Prieto",
    "Quintero",
    "Romero",
    "Suarez",
]

COST_CENTERS = [
    "FIN-ADM",
    "HR-OPS",
    "SALES",
    "TECH",
    "CUSTOMER_SUCCESS",
    "SHARED_SERVICES",
]

CONCEPT_NAMES = {
    "BASE_SALARY": "Base Salary",
    "BONUS": "Bonus",
    "MEAL_VOUCHER": "Meal Voucher",
    "CHILDCARE": "Childcare",
    "TRANSPORT": "Transport",
    "HEALTH_INSURANCE": "Health Insurance",
    "SOCIAL_SECURITY": "Social Security",
    "INCOME_TAX": "Income Tax",
    "OVERTIME": "Overtime",
    "OTHER_ADJUSTMENT": "Other Adjustment",
}

EXPECTED_TOTALS = [
    ("BASE_SALARY", 1200000.00),
    ("BONUS", 48000.00),
    ("MEAL_VOUCHER", 42000.00),
    ("CHILDCARE", 18500.00),
    ("TRANSPORT", 21000.00),
    ("HEALTH_INSURANCE", 18000.00),
    ("SOCIAL_SECURITY", -216000.00),
    ("INCOME_TAX", -198000.00),
    ("OVERTIME", 14000.00),
    ("OTHER_ADJUSTMENT", 3200.00),
]

CONCEPT_MASTER_ROWS = [
    ("BASE_SALARY", "Base Salary", "BASE_SALARY", "Base Salary", "salary", "BASE_SALARY", "positive"),
    ("BONUS", "Bonus", "BONUS", "Bonus", "bonus", "BONUS", "positive"),
    ("MEAL_VOUCHER", "Meal Voucher", "MEAL_VOUCHER", "Meal Voucher", "benefit", "MEAL_VOUCHER", "positive"),
    ("CHILDCARE", "Childcare", "CHILDCARE", "Childcare", "benefit", "CHILDCARE", "positive"),
    ("TRANSPORT", "Transport", "TRANSPORT", "Transport", "benefit", "TRANSPORT", "positive"),
    ("HEALTH_INSURANCE", "Health Insurance", "HEALTH_INSURANCE", "Health Insurance", "benefit", "HEALTH_INSURANCE", "positive"),
    ("SOCIAL_SECURITY", "Social Security", "SOCIAL_SECURITY", "Social Security", "deduction", "SOCIAL_SECURITY", "negative"),
    ("INCOME_TAX", "Income Tax", "INCOME_TAX", "Income Tax", "deduction", "INCOME_TAX", "negative"),
    ("OVERTIME", "Overtime", "OVERTIME", "Overtime", "variable_compensation", "OVERTIME", "positive"),
    ("OTHER_ADJUSTMENT", "Other Adjustment", "OTHER_ADJUSTMENT", "Other Adjustment", "adjustment", "OTHER_ADJUSTMENT", "positive"),
]


def cents_to_str(value: int) -> str:
    return f"{value / 100:.2f}"


def split_weighted(total_cents: int, weights: list[int]) -> list[int]:
    allocated: list[int] = []
    remainder = total_cents
    total_weight = sum(weights)

    for weight in weights[:-1]:
        part = round(total_cents * weight / total_weight)
        allocated.append(part)
        remainder -= part

    allocated.append(remainder)
    return allocated


def build_employees() -> list[dict[str, str]]:
    employees: list[dict[str, str]] = []
    index = 1

    for first_name in FIRST_NAMES:
        for last_name in LAST_NAMES:
            if index <= 220:
                legal_entity = "ARD Spain SL"
                country = "Spain"
            elif index <= 330:
                legal_entity = "ARD Iberia Services SL"
                country = "Spain"
            else:
                legal_entity = "ARD Portugal Unipessoal Lda"
                country = "Portugal"

            employee = {
                "employee_id": f"EMP{index:04d}",
                "employee_name": f"{first_name} {last_name}",
                "legal_entity": legal_entity,
                "country": country,
                "cost_center": COST_CENTERS[(index - 1) % len(COST_CENTERS)],
                "payroll_period": PAYROLL_PERIOD,
                "is_childcare_eligible": "true" if index <= 30 else "false",
            }
            employees.append(employee)
            index += 1

    return employees


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    employees = build_employees()
    payroll_rows: list[dict[str, str]] = []
    record_number = 1

    def add_payroll_row(
        employee: dict[str, str],
        concept_code: str,
        amount_cents: int,
        *,
        concept_name: str | None = None,
        payroll_period: str = PAYROLL_PERIOD,
        posting_date: str = "2026-03-31",
    ) -> None:
        nonlocal record_number
        payroll_rows.append(
            {
                "record_id": f"PAY{record_number:06d}",
                "employee_id": employee["employee_id"],
                "employee_name": employee["employee_name"],
                "legal_entity": employee["legal_entity"],
                "country": employee["country"],
                "cost_center": employee["cost_center"],
                "payroll_period": payroll_period,
                "posting_date": posting_date,
                "concept_code": concept_code,
                "concept_name": concept_name or CONCEPT_NAMES.get(concept_code, concept_code.title()),
                "amount": cents_to_str(amount_cents),
                "currency": "EUR",
            }
        )
        record_number += 1

    # BASE_SALARY -> 1,200,010.00
    salary_totals = []
    for idx in range(len(employees)):
        salary = 315_000 + (idx % 6) * 12_500 + (idx // 60) * 2_000
        salary_totals.append(salary)
    salary_totals[-1] += 120_001_000 - sum(salary_totals)

    for employee, total_cents in zip(employees, salary_totals, strict=True):
        for part in split_weighted(total_cents, [70, 20, 10]):
            add_payroll_row(employee, "BASE_SALARY", part, posting_date="2026-03-30")

    # SOCIAL_SECURITY -> -216,000.00
    for employee in employees:
        add_payroll_row(employee, "SOCIAL_SECURITY", -60_000, posting_date="2026-03-30")

    # INCOME_TAX -> -198,000.00
    for employee in employees:
        add_payroll_row(employee, "INCOME_TAX", -55_000, posting_date="2026-03-30")

    # HEALTH_INSURANCE -> 18,000.00
    for employee in employees[:180]:
        for part in (6_000, 4_000):
            add_payroll_row(employee, "HEALTH_INSURANCE", part, posting_date="2026-03-29")

    # BONUS -> 48,000.00
    for employee in employees[40:100]:
        for idx, part in enumerate((50_000, 30_000), start=1):
            add_payroll_row(employee, "BONUS", part, posting_date=f"2026-03-{20 + idx:02d}")

    # MEAL_VOUCHER -> 38,820.00 including duplicates; plus 5 unmapped lines
    meal_employees = employees[:258]
    duplicate_templates: list[tuple[dict[str, str], int, str, str]] = []

    for idx, employee in enumerate(meal_employees):
        total_cents = 15_000 if idx < 257 else 3_150
        period = "2026-02" if idx < 4 else PAYROLL_PERIOD
        posting_date = "2026-03-02" if idx < 4 else "2026-03-27"
        parts = split_weighted(total_cents, [53, 47])

        for part_index, part in enumerate(parts, start=1):
            add_payroll_row(
                employee,
                "MEAL_VOUCHER",
                part,
                payroll_period=period,
                posting_date=posting_date if period == "2026-02" else f"2026-03-{24 + part_index:02d}",
            )

        if 4 <= idx <= 6:
            duplicate_templates.append((employee, parts[0], PAYROLL_PERIOD, "2026-03-25"))

    for employee, amount_cents, period, posting_date in duplicate_templates:
        add_payroll_row(
            employee,
            "MEAL_VOUCHER",
            amount_cents,
            payroll_period=period,
            posting_date=posting_date,
        )

    for employee in employees[258:263]:
        add_payroll_row(
            employee,
            "MEAL_VCHR",
            15_000,
            concept_name="Meal Voucher Legacy",
            payroll_period=PAYROLL_PERIOD,
            posting_date="2026-03-27",
        )

    # CHILDCARE -> 17,050.00 with 6 eligible employees absent
    childcare_observed = employees[:24]
    for idx, employee in enumerate(childcare_observed):
        amount = 72_500 if idx < 22 else 55_000
        add_payroll_row(employee, "CHILDCARE", amount, posting_date="2026-03-28")

    # TRANSPORT -> 20,760.00
    transport_employees = employees[100:275]
    for idx, employee in enumerate(transport_employees):
        parts = (7_000, 5_000) if idx < 171 else (4_000, 2_000)
        for part_index, part in enumerate(parts, start=1):
            add_payroll_row(employee, "TRANSPORT", part, posting_date=f"2026-03-{17 + part_index:02d}")

    # OVERTIME -> 14,950.00 with one main outlier
    for employee in employees[200:269]:
        add_payroll_row(employee, "OVERTIME", 20_000, posting_date="2026-03-31")
    add_payroll_row(employees[269], "OVERTIME", 115_000, posting_date="2026-03-31")

    # OTHER_ADJUSTMENT -> 3,180.00
    for employee in employees[300:319]:
        add_payroll_row(employee, "OTHER_ADJUSTMENT", 16_000, posting_date="2026-03-31")
    add_payroll_row(employees[319], "OTHER_ADJUSTMENT", 14_000, posting_date="2026-03-31")

    employee_rows = employees

    expected_rows = [
        {
            "payroll_period": PAYROLL_PERIOD,
            "concept_code": concept_code,
            "expected_amount": f"{expected_amount:.2f}",
            "currency": "EUR",
        }
        for concept_code, expected_amount in EXPECTED_TOTALS
    ]

    concept_master_rows = [
        {
            "source_concept_code": source_code,
            "source_concept_name": source_name,
            "normalized_concept_code": normalized_code,
            "normalized_concept_name": normalized_name,
            "concept_category": category,
            "reconciliation_group": group,
            "expected_sign": sign,
            "is_active": "true",
        }
        for (
            source_code,
            source_name,
            normalized_code,
            normalized_name,
            category,
            group,
            sign,
        ) in CONCEPT_MASTER_ROWS
    ]

    write_csv(
        OUTPUT_DIR / "employee_reference.csv",
        [
            "employee_id",
            "employee_name",
            "legal_entity",
            "country",
            "cost_center",
            "payroll_period",
            "is_childcare_eligible",
        ],
        employee_rows,
    )
    write_csv(
        OUTPUT_DIR / "expected_totals.csv",
        ["payroll_period", "concept_code", "expected_amount", "currency"],
        expected_rows,
    )
    write_csv(
        OUTPUT_DIR / "concept_master.csv",
        [
            "source_concept_code",
            "source_concept_name",
            "normalized_concept_code",
            "normalized_concept_name",
            "concept_category",
            "reconciliation_group",
            "expected_sign",
            "is_active",
        ],
        concept_master_rows,
    )
    write_csv(
        OUTPUT_DIR / "payroll.csv",
        [
            "record_id",
            "employee_id",
            "employee_name",
            "legal_entity",
            "country",
            "cost_center",
            "payroll_period",
            "posting_date",
            "concept_code",
            "concept_name",
            "amount",
            "currency",
        ],
        payroll_rows,
    )

    print(f"Wrote {len(employee_rows)} employees")
    print(f"Wrote {len(payroll_rows)} payroll rows")
    print(f"Wrote {len(expected_rows)} expected totals rows")
    print(f"Wrote {len(concept_master_rows)} concept master rows")


if __name__ == "__main__":
    main()
