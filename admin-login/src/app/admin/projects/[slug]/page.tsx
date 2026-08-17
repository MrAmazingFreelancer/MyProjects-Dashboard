import Link from "next/link";
import { notFound } from "next/navigation";

const projects = {
  app1: {
    name: "Test App 1",
    status: "live",
    description: "First test project",
  },
  app2: {
    name: "Test App 2",
    status: "dev",
    description: "Second test project",
  },
} as const;

type ProjectSlug = keyof typeof projects;

export default async function ProjectPage({
  params,
}: {
  params: { slug: string };
}) {
  const project = projects[params.slug as ProjectSlug];

  if (!project) {
    notFound();
  }

  const navigation: Array<[string, string, boolean]> = [
    ["Dashboard", "/admin/dashboard", false],
    ["Website", "/admin/projects", true],
    ["Apps", "/admin/apps", false],
  ];

  return (
    <div style={{ minHeight: "100vh", background: "#edf2f8", color: "#071a3d", fontFamily: "'DM Mono', monospace", display: "flex" }}>
      <aside style={{ width: "248px", minHeight: "100vh", background: "#061536", padding: "30px 16px 24px", display: "flex", flexDirection: "column", flexShrink: 0 }}>
        <div style={{ fontFamily: "'Syne', sans-serif", fontSize: "25px", fontWeight: "800", color: "#ffffff", letterSpacing: "3px", padding: "0 18px 36px" }}>
          7INK
        </div>
        <div style={{ color: "#7790b8", fontSize: "10px", letterSpacing: "2px", padding: "0 18px 12px", textTransform: "uppercase" }}>
          Workspace
        </div>
        <nav style={{ display: "grid", gap: "6px" }} aria-label="Admin navigation">
          {navigation.map(([label, href, active]) => (
            <Link key={label} href={href} style={{ display: "flex", alignItems: "center", gap: "12px", color: active ? "#ffffff" : "#a9bad5", background: active ? "#163b82" : "transparent", borderRadius: "8px", padding: "13px 16px", textDecoration: "none", fontSize: "12px" }}>
              <span style={{ width: "7px", height: "7px", borderRadius: "2px", background: active ? "#57d7ed" : "#7187ac" }} />
              {label}
            </Link>
          ))}
        </nav>
        <div style={{ marginTop: "auto" }}>
          <Link href="/admin/settings" style={{ display: "block", color: "#a9bad5", padding: "13px 16px", textDecoration: "none", fontSize: "12px" }}>
            Settings
          </Link>
        </div>
      </aside>

      <div style={{ flex: 1, minWidth: 0 }}>
        <header style={{ height: "76px", background: "#ffffff", borderBottom: "1px solid #dce4ef", display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 42px" }}>
          <div style={{ color: "#6b7d9b", fontSize: "12px" }}>Admin workspace / Website</div>
          <Link href="/admin/dashboard" style={{ color: "#163b82", fontSize: "11px", textDecoration: "none", letterSpacing: "1px" }}>
            BACK TO DASHBOARD
          </Link>
        </header>

        <main style={{ padding: "42px", maxWidth: "900px" }}>
          <div style={{ marginBottom: "32px" }}>
            <div style={{ color: "#6b7d9b", fontSize: "11px", letterSpacing: "2px", marginBottom: "12px" }}>
              PROJECT
            </div>
            <h1 style={{ fontFamily: "'Syne', sans-serif", fontSize: "32px", fontWeight: "800", margin: "0 0 12px" }}>
              {project.name}
            </h1>
            <p style={{ color: "#6b7d9b", fontSize: "13px", margin: 0 }}>
              {project.description}
            </p>
          </div>

          <section style={{ background: "#ffffff", border: "1px solid #e0e7f0", borderRadius: "14px", padding: "28px", boxShadow: "0 8px 22px rgba(30,57,96,0.05)" }}>
            <div style={{ color: "#6b7d9b", fontSize: "11px", letterSpacing: "2px", marginBottom: "8px" }}>
              STATUS
            </div>
            <div style={{ color: project.status === "live" ? "#77b800" : "#d28b00", fontSize: "14px" }}>
              {project.status.toUpperCase()}
            </div>
            <p style={{ color: "#6b7d9b", fontSize: "12px", lineHeight: 1.6, margin: "24px 0 0" }}>
              This project is registered in the admin dashboard. Add a destination URL in the project model to connect it to the live application.
            </p>
          </section>
        </main>
      </div>
    </div>
  );
}
