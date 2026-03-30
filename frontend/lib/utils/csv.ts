export type CsvRecord = Record<string, string>;

type ParsedCsv = {
  headers: string[];
  rows: CsvRecord[];
};

export type ExpectedTotalsPreviewRow = {
  conceptCode: string;
  currency: string;
  expectedAmount: number;
  payrollPeriod: string;
};

export type PayrollPreview = {
  conceptCount: number;
  detectedPeriod: string | null;
  legalEntityCount: number;
  recordCount: number;
};

function splitCsvLine(line: string) {
  const result: string[] = [];
  let current = "";
  let inQuotes = false;

  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    const nextChar = line[index + 1];

    if (char === '"') {
      if (inQuotes && nextChar === '"') {
        current += '"';
        index += 1;
        continue;
      }

      inQuotes = !inQuotes;
      continue;
    }

    if (char === "," && !inQuotes) {
      result.push(current.trim());
      current = "";
      continue;
    }

    current += char;
  }

  result.push(current.trim());
  return result;
}

export function parseSimpleCsv(text: string): ParsedCsv {
  const lines = text
    .replace(/\r\n/g, "\n")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

  if (lines.length === 0) {
    return { headers: [], rows: [] };
  }

  const headers = splitCsvLine(lines[0]);
  const rows = lines.slice(1).map((line) => {
    const values = splitCsvLine(line);
    const record: CsvRecord = {};

    headers.forEach((header, index) => {
      record[header] = values[index] ?? "";
    });

    return record;
  });

  return { headers, rows };
}

export function parseExpectedTotalsPreview(
  text: string,
): ExpectedTotalsPreviewRow[] {
  const { rows } = parseSimpleCsv(text);

  return rows.map((row) => ({
    conceptCode: row.concept_code ?? "",
    currency: row.currency ?? "EUR",
    expectedAmount: Number.parseFloat(row.expected_amount ?? "0"),
    payrollPeriod: row.payroll_period ?? "",
  }));
}

export function parsePayrollPreview(text: string): PayrollPreview {
  const { rows } = parseSimpleCsv(text);
  const conceptCodes = new Set<string>();
  const legalEntities = new Set<string>();
  const periods = new Set<string>();

  rows.forEach((row) => {
    if (row.concept_code) {
      conceptCodes.add(row.concept_code);
    }

    if (row.legal_entity) {
      legalEntities.add(row.legal_entity);
    }

    if (row.payroll_period) {
      periods.add(row.payroll_period);
    }
  });

  return {
    conceptCount: conceptCodes.size,
    detectedPeriod: periods.size === 1 ? [...periods][0] : null,
    legalEntityCount: legalEntities.size,
    recordCount: rows.length,
  };
}
