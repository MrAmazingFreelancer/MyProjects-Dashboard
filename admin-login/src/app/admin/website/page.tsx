import Link from "next/link";

const websiteFeatures = [
  { label: "Overview", description: "Review your website status and recent activity.", href: "/admin/website" },
  { label: "Projects", description: "Manage the websites connected to this workspace.", href: "/admin/dashboard" },
  { label: "Domains", description: "Add a custom domain and manage DNS connections.", href: "/admin/website/domains" },
  { label: "SEO settings", description: "Configure metadata, search visibility, and sitemap options.", href: "/admin/website/seo" },
  { label: "Integrations", description: "Connect analytics, forms, and third-party services.", href: "/admin/website/integrations" },
  { label: "Website settings", description: "Update the website name, deployment, and access preferences.", href: "/admin/website/settings" },
];

const domains = [
  { name: "7ink.com.au", url: "https://7ink.com.au", status: "Connected", type: "Primary domain" },
  { name: "mramazing.online", url: "https://mramazing.online", status: "Connected", type: "Custom domain" },
  { name: "mramazing.org", url: "https://mramazing.org", status: "Connected", type: "Custom domain" },
  { name: "localhost", url: "http://localhost", status: "Development", type: "Local domain" },
];

const projects = [
  { name: "Test App 1", description: "First test project", href: "/admin/projects/app1", status: "LIVE" },
  { name: "Test App 2", description: "Second test project", href: "/admin/projects/app2", status: "DEV" },
];

const navigation = [
  ["Dashboard", "/admin/dashboard", false],
  ["Website", "/admin/website", true],
  ["Apps", "/admin/apps", false],
] as const;

export default function WebsitePage() {
  return (
    <div style={{ minHeight: "100vh", background: "#edf2f8", color: "#071a3d", fontFamily: "'DM Mono', monospace", display: "flex" }}>
      <aside style={{ width: "248px", minHeight: "100vh", background: "#061536", padding: "30px 16px 24px", display: "flex", flexDirection: "column", flexShrink: 0 }}>
        <div style={{ fontFamily: "'Syne', sans-serif", fontSize: "25px", fontWeight: "800", color: "#ffffff", letterSpacing: "3px", padding: "0 18px 36px" }}>7INK</div>
        <div style={{ color: "#7790b8", fontSize: "10px", letterSpacing: "2px", padding: "0 18px 12px", textTransform: "uppercase" }}>Workspace</div>
        <nav style={{ display: "grid", gap: "6px" }} aria-label="Admin navigation">
          {navigation.map(([label, href, active]) => (
            <div key={label}>
              <Link href={href} style={{ display: "flex", alignItems: "center", gap: "12px", color: active ? "#ffffff" : "#a9bad5", background: active ? "#163b82" : "transparent", borderRadius: "8px", padding: "13px 16px", textDecoration: "none", fontSize: "12px" }}>
                <span style={{ width: "7px", height: "7px", borderRadius: "2px", background: active ? "#57d7ed" : "#7187ac" }} />
                {label}
                {active && <span style={{ marginLeft: "auto", color: "#57d7ed", fontSize: "11px" }}>⌄</span>}
              </Link>
              {active && (
                <div style={{ margin: "4px 0 8px 35px", borderLeft: "1px solid #31518a", display: "grid" }}>
                  {["Overview", "Projects", "Domains", "SEO", "Integrations", "Settings"].map((item, index) => (
                    <Link key={item} href={index === 0 ? "/admin/website" : index === 1 ? "/admin/dashboard" : `/admin/website/${item.toLowerCase()}`} style={{ color: index === 0 ? "#57d7ed" : "#8fa4c5", padding: "8px 12px", textDecoration: "none", fontSize: "11px" }}>
                      {item}
                    </Link>
                  ))}
                </div>
              )}
            </div>
          ))}
        </nav>
        <div style={{ marginTop: "auto" }}><Link href="/admin/settings" style={{ display: "block", color: "#a9bad5", padding: "13px 16px", textDecoration: "none", fontSize: "12px" }}>Settings</Link></div>
      </aside>

      <div style={{ flex: 1, minWidth: 0 }}>
        <header style={{ height: "76px", background: "#ffffff", borderBottom: "1px solid #dce4ef", display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 42px" }}>
          <div style={{ color: "#6b7d9b", fontSize: "12px" }}>Admin workspace / Website</div>
          <div style={{ color: "#163b82", fontSize: "11px", letterSpacing: "1px" }}>WEBSITE MANAGEMENT</div>
        </header>

        <main style={{ padding: "42px", maxWidth: "1100px" }}>
          <div style={{ marginBottom: "30px" }}>
            <div style={{ color: "#6b7d9b", fontSize: "10px", letterSpacing: "2px", marginBottom: "10px", textTransform: "uppercase" }}>Website</div>
            <h1 style={{ fontFamily: "'Syne', sans-serif", fontSize: "32px", fontWeight: "800", margin: "0 0 8px" }}>Website settings</h1>
            <p style={{ color: "#6b7d9b", fontSize: "13px", margin: 0 }}>Manage your website, domains, and connected services from one place.</p>
          </div>

          <section style={{ background: "linear-gradient(135deg, #163b82, #2763bc)", borderRadius: "14px", padding: "26px 30px", color: "#ffffff", marginBottom: "28px", boxShadow: "0 12px 28px rgba(22,59,130,0.18)" }}>
            <div style={{ fontSize: "10px", letterSpacing: "2px", opacity: 0.72, marginBottom: "10px" }}>GET STARTED</div>
            <div style={{ fontFamily: "'Syne', sans-serif", fontSize: "23px", fontWeight: "800", marginBottom: "8px" }}>Connect a domain</div>
            <div style={{ color: "#dcecff", fontSize: "12px", marginBottom: "20px" }}>Give your website a professional address with a custom domain.</div>
            <Link href="/admin/website/domains" style={{ display: "inline-block", background: "#ffffff", color: "#163b82", borderRadius: "7px", padding: "11px 16px", textDecoration: "none", fontSize: "11px", fontWeight: "700", letterSpacing: "1px" }}>+ ADD DOMAIN</Link>
          </section>

          <section style={{ background: "#ffffff", border: "1px solid #e0e7f0", borderRadius: "14px", padding: "24px", marginBottom: "28px", boxShadow: "0 8px 22px rgba(30,57,96,0.05)" }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "18px" }}>
              <div>
                <h2 style={{ color: "#071a3d", fontFamily: "'Syne', sans-serif", fontSize: "19px", margin: "0 0 6px" }}>Domains</h2>
                <p style={{ color: "#6b7d9b", fontSize: "11px", margin: 0 }}>Domains linked to your admin dashboard.</p>
              </div>
              <span style={{ color: "#6b7d9b", fontSize: "11px" }}>{domains.length} domains</span>
            </div>
            <div style={{ display: "grid", gap: "10px" }}>
              {domains.map(domain => (
                <div key={domain.name} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: "16px", border: "1px solid #e7edf5", borderRadius: "9px", padding: "14px 16px" }}>
                  <div>
                    <a href={domain.url} target="_blank" rel="noreferrer" style={{ color: "#163b82", fontSize: "13px", fontWeight: "600", marginBottom: "5px", textDecoration: "underline", textUnderlineOffset: "3px" }}>{domain.name}</a>
                    <div style={{ color: "#8a9ab1", fontSize: "10px" }}>{domain.type}</div>
                  </div>
                  <span style={{ color: domain.status === "Connected" ? "#4d9900" : "#2763bc", background: domain.status === "Connected" ? "#eef8df" : "#e8f2ff", borderRadius: "999px", padding: "6px 10px", fontSize: "10px", whiteSpace: "nowrap" }}>
                    {domain.status}
                  </span>
                </div>
              ))}
            </div>
          </section>

          <section style={{ background: "#ffffff", border: "1px solid #e0e7f0", borderRadius: "14px", padding: "24px", marginBottom: "28px", boxShadow: "0 8px 22px rgba(30,57,96,0.05)" }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "18px" }}>
              <div>
                <h2 style={{ color: "#071a3d", fontFamily: "'Syne', sans-serif", fontSize: "19px", margin: "0 0 6px" }}>Projects</h2>
                <p style={{ color: "#6b7d9b", fontSize: "11px", margin: 0 }}>Projects managed by the admin dashboard.</p>
              </div>
              <Link href="/admin/projects/new" style={{ color: "#163b82", fontSize: "11px", textDecoration: "none", fontWeight: "700" }}>+ ADD PROJECT</Link>
            </div>
            <div style={{ display: "grid", gap: "10px" }}>
              {projects.map(project => (
                <Link key={project.name} href={project.href} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: "16px", border: "1px solid #e7edf5", borderRadius: "9px", padding: "14px 16px", textDecoration: "none" }}>
                  <div>
                    <div style={{ color: "#163b82", fontSize: "13px", fontWeight: "600", marginBottom: "5px" }}>{project.name}</div>
                    <div style={{ color: "#8a9ab1", fontSize: "10px" }}>{project.description}</div>
                  </div>
                  <span style={{ color: project.status === "LIVE" ? "#4d9900" : "#d28b00", background: project.status === "LIVE" ? "#eef8df" : "#fff4d9", borderRadius: "999px", padding: "6px 10px", fontSize: "10px" }}>{project.status}</span>
                </Link>
              ))}
            </div>
          </section>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(270px, 1fr))", gap: "16px" }}>
            {websiteFeatures.map(feature => (
              <Link key={feature.label} href={feature.href} style={{ background: "#ffffff", border: "1px solid #e0e7f0", borderRadius: "14px", padding: "22px", textDecoration: "none", boxShadow: "0 8px 22px rgba(30,57,96,0.05)" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                  <div style={{ color: "#071a3d", fontSize: "15px", fontWeight: "600" }}>{feature.label}</div>
                  <span style={{ color: "#2763bc", fontSize: "16px" }}>→</span>
                </div>
                <div style={{ color: "#6b7d9b", fontSize: "12px", lineHeight: 1.6 }}>{feature.description}</div>
              </Link>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
