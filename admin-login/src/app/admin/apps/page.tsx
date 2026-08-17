import { getServerSession } from "next-auth";
import { redirect } from "next/navigation";
import Link from "next/link";

const apps = [
  { name: "Website Manager", description: "Manage websites, projects, and connected domains.", href: "/admin/website", status: "ACTIVE" },
  { name: "Project Workspace", description: "Review and manage the projects linked to 7ink.", href: "/admin/projects", status: "ACTIVE" },
];

export default async function AppsPage() {
  const session = await getServerSession();
  if (!session) redirect("/login");

  return (
    <div style={{ minHeight: "100vh", background: "#edf2f8", color: "#071a3d", fontFamily: "'DM Mono', monospace", display: "flex" }}>
      <aside style={{ width: "248px", minHeight: "100vh", background: "#061536", padding: "30px 16px 24px", display: "flex", flexDirection: "column", flexShrink: 0 }}>
        <div style={{ fontFamily: "'Syne', sans-serif", fontSize: "25px", fontWeight: "800", color: "#ffffff", letterSpacing: "3px", padding: "0 18px 36px" }}>7INK</div>
        <div style={{ color: "#7790b8", fontSize: "10px", letterSpacing: "2px", padding: "0 18px 12px", textTransform: "uppercase" }}>Workspace</div>
        <nav style={{ display: "grid", gap: "6px" }} aria-label="Admin navigation">
          <Link href="/admin/dashboard" style={{ color: "#a9bad5", padding: "13px 16px", textDecoration: "none", fontSize: "12px" }}>• Dashboard</Link>
          <Link href="/admin/website" style={{ color: "#a9bad5", padding: "13px 16px", textDecoration: "none", fontSize: "12px" }}>• Website</Link>
          <Link href="/admin/apps" style={{ display: "flex", gap: "12px", color: "#ffffff", background: "#163b82", borderRadius: "8px", padding: "13px 16px", textDecoration: "none", fontSize: "12px" }}><span style={{ color: "#57d7ed" }}>•</span> Apps</Link>
        </nav>
        <div style={{ marginTop: "auto" }}><Link href="/admin/settings" style={{ display: "block", color: "#a9bad5", padding: "13px 16px", textDecoration: "none", fontSize: "12px" }}>Settings</Link></div>
      </aside>

      <div style={{ flex: 1, minWidth: 0 }}>
        <header style={{ height: "76px", background: "#ffffff", borderBottom: "1px solid #dce4ef", display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 42px" }}>
          <div style={{ color: "#6b7d9b", fontSize: "12px" }}>Admin workspace / Apps</div>
          <div style={{ color: "#163b82", fontSize: "11px", letterSpacing: "1px" }}>APP MANAGEMENT</div>
        </header>

        <main style={{ padding: "42px", maxWidth: "1100px" }}>
          <div style={{ marginBottom: "30px" }}>
            <div style={{ color: "#6b7d9b", fontSize: "10px", letterSpacing: "2px", marginBottom: "10px", textTransform: "uppercase" }}>Workspace</div>
            <h1 style={{ fontFamily: "'Syne', sans-serif", fontSize: "32px", fontWeight: "800", margin: "0 0 8px" }}>Apps</h1>
            <p style={{ color: "#6b7d9b", fontSize: "13px", margin: 0 }}>Access the tools connected to your 7ink admin dashboard.</p>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "16px" }}>
            {apps.map(app => (
              <Link key={app.name} href={app.href} style={{ background: "#ffffff", border: "1px solid #e0e7f0", borderRadius: "14px", padding: "24px", textDecoration: "none", boxShadow: "0 8px 22px rgba(30,57,96,0.05)" }}>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "14px" }}>
                  <div style={{ color: "#071a3d", fontSize: "16px", fontWeight: "600" }}>{app.name}</div>
                  <span style={{ color: "#4d9900", background: "#eef8df", borderRadius: "999px", padding: "6px 10px", fontSize: "10px" }}>{app.status}</span>
                </div>
                <div style={{ color: "#6b7d9b", fontSize: "12px", lineHeight: 1.6 }}>{app.description}</div>
                <div style={{ color: "#2763bc", fontSize: "11px", marginTop: "20px" }}>OPEN APP →</div>
              </Link>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
