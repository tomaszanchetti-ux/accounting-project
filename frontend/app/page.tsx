import { getBackendHealth } from "@/lib/api/client";

export default async function Home() {
  const health = await getBackendHealth();

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-12 text-slate-50">
      <div className="mx-auto flex min-h-[calc(100vh-6rem)] max-w-5xl flex-col justify-between rounded-[32px] border border-white/10 bg-white/5 p-8 shadow-2xl shadow-slate-950/40 backdrop-blur md:p-12">
        <div className="space-y-6">
          <span className="inline-flex rounded-full border border-emerald-400/30 bg-emerald-400/10 px-4 py-1 text-sm font-medium text-emerald-200">
            Accounting Reconciliation MVP
          </span>
          <div className="max-w-3xl space-y-4">
            <h1 className="text-4xl font-semibold tracking-tight text-balance md:text-6xl">
              Conciliacion payroll vs contabilidad con foco en claridad operativa.
            </h1>
            <p className="max-w-2xl text-lg leading-8 text-slate-300">
              Esta primera version dejara visible el setup tecnico del producto y
              preparara el camino para cargar archivos, ejecutar runs y explicar
              diferencias con reglas explicitas.
            </p>
          </div>
        </div>

        <div className="grid gap-4 pt-10 md:grid-cols-3">
          <section className="rounded-3xl border border-white/10 bg-slate-900/80 p-5">
            <p className="text-sm uppercase tracking-[0.2em] text-slate-400">
              Estado
            </p>
            <p className="mt-3 text-2xl font-semibold text-white">
              Epic 00 en progreso
            </p>
          </section>
          <section className="rounded-3xl border border-white/10 bg-slate-900/80 p-5">
            <p className="text-sm uppercase tracking-[0.2em] text-slate-400">
              Frontend
            </p>
            <p className="mt-3 text-2xl font-semibold text-white">
              Next.js listo para crecer
            </p>
          </section>
          <section className="rounded-3xl border border-white/10 bg-slate-900/80 p-5">
            <p className="text-sm uppercase tracking-[0.2em] text-slate-400">
              Siguiente paso
            </p>
            <p className="mt-3 text-2xl font-semibold text-white">
              Base visual y API health check
            </p>
          </section>
        </div>

        <section className="mt-6 rounded-3xl border border-white/10 bg-slate-900/80 p-5">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.2em] text-slate-400">
                Backend health check
              </p>
              <p className="mt-3 text-2xl font-semibold text-white">
                {health.ok ? "Conectado" : "Pendiente"}
              </p>
            </div>
            <div className="max-w-2xl space-y-2 text-sm text-slate-300">
              <p>{health.summary}</p>
              <p className="font-mono text-xs text-slate-400">
                API base URL: {health.apiBaseUrl}
              </p>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
