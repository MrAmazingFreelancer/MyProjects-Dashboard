// src/app/admin/dashboard/page.tsx
import { getServerSession } from "next-auth";
import { redirect } from "next/navigation";
import { signOut } from "next-auth/react";
import SignOutButton from "@/components/SignOutButton";

export default async function DashboardPage() {
  const session = await getServerSession();
  if (!session) redirect("/login");

  const projects = [
    { name: "Test App 1", url: "/admin/projects/app1", status: "live", description: "First test project" },
    { name: "Test App 2", url: "/admin/projects/app2", status: "dev", description: "Second test project" },
  ];

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0a0a0a",
      fontFamily: "'DM Mono', monospace",
    }}>
      {/* Nav */}
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
        }}>7ink <span style={{ color: "#333", fontWeight: "400", fontSize: "14px" }}>/ admin</span></div>

        <div style={{ display: "flex", alignItems: "center", gap: "20px" }}>
          <span style={{ color: "#444", fontSize: "12px" }}>{session.user?.email}</span>
          <SignOutButton />
        </div>
      </nav>

      {/* Content */}
      <main style={{ padding: "48px 40px", maxWidth: "1100px" }}>
        <div style={{ marginBottom: "48px" }}>
          <h1 style={{
            fontFamily: "'Syne', sans-serif",
            fontSize: "32px",
            fontWeight: "800",
            color: "#fff",
            marginBottom: "8px",
          }}>Dashboard</h1>
          <p style={{ color: "#444", fontSize: "13px" }}>Welcome back, {session.user?.name || session.user?.email}</p>
        </div>

        {/* Stats */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px", marginBottom: "48px" }}>
          {[
            { label: "PROJECTS", value: "2" },
            { label: "LIVE", value: "1" },
            { label: "IN DEV", value: "1" },
          ].map(stat => (
            <div key={stat.label} style={{
              background: "#111",
              border: "1px solid #1a1a1a",
              borderRadius: "12px",
              padding: "24px",
            }}>
              <div style={{ color: "#444", fontSize: "11px", letterSpacing: "2px", marginBottom: "8px" }}>{stat.label}</div>
              <div style={{ color: "#c8ff00", fontSize: "36px", fontFamily: "'Syne', sans-serif", fontWeight: "800" }}>{stat.value}</div>
            </div>
          ))}
        </div>

        {/* Projects */}
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
            <h2 style={{ color: "#fff", fontSize: "16px", fontWeight: "500" }}>Projects</h2>
            <a href="/admin/projects/new" style={{
              background: "#c8ff00",
              color: "#0a0a0a",
              padding: "8px 16px",
              borderRadius: "6px",
              fontSize: "11px",
              letterSpacing: "1px",
              textDecoration: "none",
              fontWeight: "500",
            }}>+ ADD PROJECT</a>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: "16px" }}>
            {projects.map(project => (
              <a key={project.name} href={project.url} className="project-card" style={{
                background: "#111",
                border: "1px solid #1a1a1a",
                borderRadius: "12px",
                padding: "24px",
                textDecoration: "none",
                display: "block",
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
                  <div style={{ color: "#fff", fontSize: "15px", fontWeight: "500" }}>{project.name}</div>
                  <span style={{
                    background: project.status === "live" ? "rgba(200,255,0,0.1)" : "rgba(255,160,0,0.1)",
                    color: project.status === "live" ? "#c8ff00" : "#ffa000",
                    padding: "2px 8px",
                    borderRadius: "4px",
                    fontSize: "10px",
                    letterSpacing: "1px",
                  }}>{project.status.toUpperCase()}</span>
                </div>
                <div style={{ color: "#444", fontSize: "12px" }}>{project.description}</div>
              </a>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
