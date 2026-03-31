import { readFile } from "node:fs/promises";
import path from "node:path";

import {
  parseExpectedTotalsPreview,
  type ExpectedTotalsPreviewRow,
} from "@/lib/utils/csv";

export type DemoSetupBundle = {
  defaultPeriod: string;
  expectedTotals: ExpectedTotalsPreviewRow[];
  seedFiles: {
    conceptMaster: {
      content: string;
      fileName: string;
    };
    employeeReference: {
      content: string;
      fileName: string;
    };
    expectedTotals: {
      content: string;
      fileName: string;
    };
  };
};

function getDemoSeedFilePath(filename: string) {
  return path.resolve(process.cwd(), "..", "data", "demo_seed", filename);
}

export async function getDemoSetupBundle(): Promise<DemoSetupBundle> {
  const expectedTotalsPath = getDemoSeedFilePath("expected_totals.csv");
  const conceptMasterPath = getDemoSeedFilePath("concept_master.csv");
  const employeeReferencePath = getDemoSeedFilePath("employee_reference.csv");
  const [expectedTotalsContent, conceptMasterContent, employeeReferenceContent] =
    await Promise.all([
      readFile(expectedTotalsPath, "utf8"),
      readFile(conceptMasterPath, "utf8"),
      readFile(employeeReferencePath, "utf8"),
    ]);

  return {
    defaultPeriod: "2026-03",
    expectedTotals: parseExpectedTotalsPreview(expectedTotalsContent),
    seedFiles: {
      conceptMaster: {
        content: conceptMasterContent,
        fileName: "concept_master.csv",
      },
      employeeReference: {
        content: employeeReferenceContent,
        fileName: "employee_reference.csv",
      },
      expectedTotals: {
        content: expectedTotalsContent,
        fileName: "expected_totals.csv",
      },
    },
  };
}
