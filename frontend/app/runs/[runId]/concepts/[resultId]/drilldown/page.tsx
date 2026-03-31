import { redirect } from "next/navigation";

type DrilldownRedirectPageProps = {
  params: Promise<{
    resultId: string;
    runId: string;
  }>;
};

export default async function DrilldownRedirectPage({
  params,
}: DrilldownRedirectPageProps) {
  const { resultId, runId } = await params;
  redirect(`/runs/${runId}/concepts/${resultId}`);
}
