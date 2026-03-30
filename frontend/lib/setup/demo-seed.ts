import { readFile } from "node:fs/promises";
import path from "node:path";

import {
  parseExpectedTotalsPreview,
  type ExpectedTotalsPreviewRow,
} from "@/lib/utils/csv";

export type DemoSetupBundle = {
  defaultPeriod: string;
  expectedTotals: ExpectedTotalsPreviewRow[];
  referenceFiles: {
    conceptMasterPath: string;
    employeeReferencePath: string;
    expectedTotalsPath: string;
  };
};

function getDemoSeedFilePath(filename: string) {
  return path.resolve(process.cwd(), "..", "data", "demo_seed", filename);
}

export async function getDemoSetupBundle(): Promise<DemoSetupBundle> {
  const expectedTotalsPath = getDemoSeedFilePath("expected_totals.csv");
  const conceptMasterPath = getDemoSeedFilePath("concept_master.csv");
  const employeeReferencePath = getDemoSeedFilePath("employee_reference.csv");
  const expectedTotalsContent = await readFile(expectedTotalsPath, "utf8");

  return {
    defaultPeriod: "2026-03",
    expectedTotals: parseExpectedTotalsPreview(expectedTotalsContent),
    referenceFiles: {
      conceptMasterPath,
      employeeReferencePath,
      expectedTotalsPath,
    },
  };
}
