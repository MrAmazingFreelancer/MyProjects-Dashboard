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

  const navigation = [
    { label: "Dashboard", href: "/admin/dashboard", active: true },
    { label: "Website", href: "/admin/website" },
    { label: "Apps", href: "/admin/apps" },
  ];

  return (
    <div style={{
      minHeight: "100vh",
      background: "#edf2f8",
      fontFamily: "'DM Mono', monospace",
      color: "#071a3d",
      display: "flex",
    }}>
      <aside style={{
        width: "248px",
        minHeight: "100vh",
        background: "#061536",
        padding: "30px 16px 24px",
        display: "flex",
        flexDirection: "column",
        flexShrink: 0,
      }}>
        <div style={{
          fontFamily: "'Syne', sans-serif",
          fontSize: "25px",
          fontWeight: "800",
          color: "#ffffff",
          letterSpacing: "3px",
          padding: "0 18px 36px",
        }}>7INK</div>

        <div style={{ color: "#7790b8", fontSize: "10px", letterSpacing: "2px", padding: "0 18px 12px", textTransform: "uppercase" }}>
          Workspace
        </div>

        <nav style={{ display: "grid", gap: "6px" }} aria-label="Admin navigation">
          {navigation.map(item => (
            <div key={item.label}>
              <a href={item.href} style={{
                display: "flex",
                alignItems: "center",
                gap: "12px",
                color: item.active ? "#ffffff" : "#a9bad5",
                background: item.active ? "#163b82" : "transparent",
                borderRadius: "8px",
                padding: "13px 16px",
                textDecoration: "none",
                fontSize: "12px",
                letterSpacing: "0.4px",
              }}>
                <span style={{ width: "7px", height: "7px", borderRadius: "2px", background: item.active ? "#57d7ed" : "#7187ac" }} />
                {item.label}
                {item.label === "Website" && <span style={{ marginLeft: "auto", color: "#7790b8", fontSize: "11px" }}>›</span>}
              </a>
            </div>
          ))}
        </nav>

        <div style={{ marginTop: "auto" }}>
          <a href="/admin/settings" style={{ display: "block", color: "#a9bad5", padding: "13px 16px", textDecoration: "none", fontSize: "12px" }}>
            Settings
          </a>
          <div style={{ borderTop: "1px solid rgba(255,255,255,0.1)", margin: "14px 16px 18px" }} />
          <div style={{ color: "#7790b8", fontSize: "11px", padding: "0 16px 12px", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            {session.user?.email}
          </div>
          <div style={{ padding: "0 16px" }}><SignOutButton /></div>
        </div>
      </aside>

      <div style={{ flex: 1, minWidth: 0 }}>
        <header style={{
          height: "76px",
          background: "#ffffff",
          borderBottom: "1px solid #dce4ef",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 42px",
        }}>
          <div style={{ color: "#6b7d9b", fontSize: "12px" }}>Admin workspace / Overview</div>
          <div style={{ color: "#163b82", fontSize: "11px", letterSpacing: "1px" }}>7INK ADMIN</div>
        </header>

        <main style={{ padding: "42px", maxWidth: "1280px" }}>
          <div style={{ marginBottom: "34px" }}>
          <h1 style={{
            fontFamily: "'Syne', sans-serif",
            fontSize: "32px",
            fontWeight: "800",
            color: "#071a3d",
            marginBottom: "8px",
          }}>Dashboard</h1>
            <p style={{ color: "#6b7d9b", fontSize: "13px" }}>Welcome back, {session.user?.name || session.user?.email}</p>
          </div>

        {/* Stats */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: "18px", marginBottom: "42px" }}>
          {[
            { label: "PROJECTS", value: "2" },
            { label: "LIVE", value: "1" },
            { label: "IN DEV", value: "1" },
          ].map(stat => (
            <div key={stat.label} style={{
              background: "#ffffff",
              border: "1px solid #e0e7f0",
              borderRadius: "14px",
              padding: "24px",
              boxShadow: "0 8px 22px rgba(30,57,96,0.05)",
            }}>
              <div style={{ color: "#6b7d9b", fontSize: "11px", letterSpacing: "2px", marginBottom: "8px" }}>{stat.label}</div>
              <div style={{ color: "#163b82", fontSize: "36px", fontFamily: "'Syne', sans-serif", fontWeight: "800" }}>{stat.value}</div>
            </div>
          ))}
        </div>

        {/* Projects */}
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
            <h2 style={{ color: "#071a3d", fontSize: "18px", fontWeight: "600" }}>Projects</h2>
            <a href="/admin/projects/new" style={{
              background: "#163b82",
              color: "#ffffff",
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
                background: "#ffffff",
                border: "1px solid #e0e7f0",
                borderRadius: "14px",
                padding: "24px",
                textDecoration: "none",
                display: "block",
                boxShadow: "0 8px 22px rgba(30,57,96,0.05)",
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
                  <div style={{ color: "#071a3d", fontSize: "15px", fontWeight: "600" }}>{project.name}</div>
                  <span style={{
                    background: project.status === "live" ? "rgba(200,255,0,0.1)" : "rgba(255,160,0,0.1)",
                    color: project.status === "live" ? "#c8ff00" : "#ffa000",
                    padding: "2px 8px",
                    borderRadius: "4px",
                    fontSize: "10px",
                    letterSpacing: "1px",
                  }}>{project.status.toUpperCase()}</span>
                </div>
                <div style={{ color: "#6b7d9b", fontSize: "12px" }}>{project.description}</div>
              </a>
            ))}
          </div>
        </div>
        </main>
      </div>
    </div>
  );
}
