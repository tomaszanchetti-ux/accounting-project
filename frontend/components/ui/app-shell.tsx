type AppShellProps = {
  children: React.ReactNode;
};

export function AppShell({ children }: AppShellProps) {
  return (
    <main className="min-h-screen px-4 py-6 text-foreground sm:px-6 lg:px-8">
      <div className="mx-auto flex min-h-[calc(100vh-3rem)] w-full max-w-7xl flex-col gap-6 rounded-[28px] border border-border-subtle/90 bg-surface/90 p-4 shadow-[0_24px_80px_rgba(28,39,56,0.14)] backdrop-blur md:p-6">
        {children}
      </div>
    </main>
  );
}
