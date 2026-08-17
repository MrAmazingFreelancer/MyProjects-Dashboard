import { getServerSession } from "next-auth";
import { redirect } from "next/navigation";
import Link from "next/link";

const projects = [
  { name: "Test App 1", href: "/admin/projects/app1", status: "LIVE", description: "First test project" },
  { name: "Test App 2", href: "/admin/projects/app2", status: "DEV", description: "Second test project" },
];

export default async function ProjectsPage() {
  const session = await getServerSession();
  if (!session) redirect("/login");

  return (
    <div style={{ minHeight: "100vh", background: "#edf2f8", color: "#071a3d", fontFamily: "'DM Mono', monospace", display: "flex" }}>
      <aside style={{ width: "248px", minHeight: "100vh", background: "#061536", padding: "30px 16px 24px", display: "flex", flexDirection: "column", flexShrink: 0 }}>
        <div style={{ fontFamily: "'Syne', sans-serif", fontSize: "25px", fontWeight: "800", color: "#ffffff", letterSpacing: "3px", padding: "0 18px 36px" }}>7INK</div>
        <div style={{ color: "#7790b8", fontSize: "10px", letterSpacing: "2px", padding: "0 18px 12px", textTransform: "uppercase" }}>Workspace</div>
        <nav style={{ display: "grid", gap: "6px" }} aria-label="Admin navigation">
          <Link href="/admin/dashboard" style={{ color: "#a9bad5", padding: "13px 16px", textDecoration: "none", fontSize: "12px" }}>• Dashboard</Link>
          <Link href="/admin/website" style={{ display: "flex", justifyContent: "space-between", color: "#ffffff", background: "#163b82", borderRadius: "8px", padding: "13px 16px", textDecoration: "none", fontSize: "12px" }}>Website <span style={{ color: "#57d7ed" }}>⌄</span></Link>
          <div style={{ margin: "4px 0 8px 35px", borderLeft: "1px solid #31518a", display: "grid" }}>
            {["Overview", "Projects", "Domains", "SEO", "Integrations", "Settings"].map(item => {
              const href = item === "Overview" ? "/admin/website" : item === "Projects" ? "/admin/projects" : `/admin/website/${item.toLowerCase()}`;
              return <Link key={item} href={href} style={{ color: item === "Projects" ? "#57d7ed" : "#8fa4c5", padding: "8px 12px", textDecoration: "none", fontSize: "11px" }}>{item}</Link>;
            })}
          </div>
          <Link href="/admin/apps" style={{ color: "#a9bad5", padding: "13px 16px", textDecoration: "none", fontSize: "12px" }}>• Apps</Link>
        </nav>
        <div style={{ marginTop: "auto" }}><Link href="/admin/settings" style={{ display: "block", color: "#a9bad5", padding: "13px 16px", textDecoration: "none", fontSize: "12px" }}>Settings</Link></div>
      </aside>

      <div style={{ flex: 1, minWidth: 0 }}>
        <header style={{ height: "76px", background: "#ffffff", borderBottom: "1px solid #dce4ef", display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 42px" }}>
          <div style={{ color: "#6b7d9b", fontSize: "12px" }}>Admin workspace / Website / Projects</div>
          <Link href="/admin/website" style={{ color: "#163b82", fontSize: "11px", textDecoration: "none", letterSpacing: "1px" }}>WEBSITE OVERVIEW</Link>
        </header>

        <main style={{ padding: "42px", maxWidth: "1100px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: "30px" }}>
            <div>
              <div style={{ color: "#6b7d9b", fontSize: "10px", letterSpacing: "2px", marginBottom: "10px", textTransform: "uppercase" }}>Website</div>
              <h1 style={{ fontFamily: "'Syne', sans-serif", fontSize: "32px", fontWeight: "800", margin: "0 0 8px" }}>Projects</h1>
              <p style={{ color: "#6b7d9b", fontSize: "13px", margin: 0 }}>Projects linked to your admin dashboard.</p>
            </div>
            <Link href="/admin/projects/new" style={{ background: "#163b82", color: "#ffffff", borderRadius: "7px", padding: "11px 16px", textDecoration: "none", fontSize: "11px", fontWeight: "700", letterSpacing: "1px" }}>+ ADD PROJECT</Link>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "16px" }}>
            {projects.map(project => (
              <Link key={project.name} href={project.href} style={{ background: "#ffffff", border: "1px solid #e0e7f0", borderRadius: "14px", padding: "24px", textDecoration: "none", boxShadow: "0 8px 22px rgba(30,57,96,0.05)" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                  <div style={{ color: "#071a3d", fontSize: "15px", fontWeight: "600" }}>{project.name}</div>
                  <span style={{ color: project.status === "LIVE" ? "#4d9900" : "#d28b00", background: project.status === "LIVE" ? "#eef8df" : "#fff4d9", borderRadius: "999px", padding: "6px 10px", fontSize: "10px" }}>{project.status}</span>
                </div>
                <div style={{ color: "#6b7d9b", fontSize: "12px" }}>{project.description}</div>
              </Link>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
