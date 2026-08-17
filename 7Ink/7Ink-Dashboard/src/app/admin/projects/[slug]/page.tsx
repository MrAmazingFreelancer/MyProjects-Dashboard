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

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0a0a0a",
      color: "#fff",
      fontFamily: "'DM Mono', monospace",
    }}>
      <nav style={{
        borderBottom: "1px solid #1a1a1a",
        padding: "0 40px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        height: "60px",
      }}>
        <div style={{
          fontFamily: "'Syne', sans-serif",
          fontSize: "20px",
          fontWeight: "800",
          color: "#c8ff00",
        }}>
          7ink <span style={{ color: "#333", fontWeight: "400", fontSize: "14px" }}>/ admin</span>
        </div>
        <Link href="/admin/dashboard" style={{ color: "#888", fontSize: "12px", textDecoration: "none" }}>
          BACK TO DASHBOARD
        </Link>
      </nav>

      <main style={{ padding: "48px 40px", maxWidth: "800px" }}>
        <div style={{ marginBottom: "32px" }}>
          <div style={{ color: "#666", fontSize: "11px", letterSpacing: "2px", marginBottom: "12px" }}>
            PROJECT
          </div>
          <h1 style={{
            fontFamily: "'Syne', sans-serif",
            fontSize: "32px",
            fontWeight: "800",
            margin: "0 0 12px",
          }}>
            {project.name}
          </h1>
          <p style={{ color: "#666", fontSize: "13px", margin: 0 }}>
            {project.description}
          </p>
        </div>

        <section style={{
          background: "#111",
          border: "1px solid #1a1a1a",
          borderRadius: "12px",
          padding: "28px",
        }}>
          <div style={{ color: "#444", fontSize: "11px", letterSpacing: "2px", marginBottom: "8px" }}>
            STATUS
          </div>
          <div style={{ color: project.status === "live" ? "#c8ff00" : "#ffa000", fontSize: "14px" }}>
            {project.status.toUpperCase()}
          </div>
          <p style={{ color: "#555", fontSize: "12px", lineHeight: 1.6, margin: "24px 0 0" }}>
            This project is registered in the admin dashboard. Add a destination URL in the project model to connect it to the live application.
          </p>
        </section>
      </main>
    </div>
  );
}
