"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { notFound } from "next/navigation";

const sections = {
  seo: {
    label: "SEO settings",
    eyebrow: "Search visibility",
    description: "Configure the metadata and indexing settings that help people find your website.",
    items: ["Page titles and descriptions", "Search engine indexing", "Sitemap configuration", "Social sharing previews"],
  },
  integrations: {
    label: "Integrations",
    eyebrow: "Connected services",
    description: "Connect analytics, forms, and other services to your website workspace.",
    items: ["Analytics", "Contact forms", "Email notifications", "Third-party services"],
  },
  settings: {
    label: "Website settings",
    eyebrow: "Workspace preferences",
    description: "Update your website identity, deployment preferences, and access options.",
    items: ["Website name", "Deployment settings", "Access preferences", "Danger zone"],
  },
  domains: {
    label: "Domains",
    eyebrow: "Domain management",
    description: "Manage the domains linked to your admin dashboard.",
    items: ["7ink.com.au", "mramazing.online", "mramazing.org", "localhost"],
  },
} as const;

type Section = keyof typeof sections;

export default function WebsiteSectionPage({ params }: { params: { section: string } }) {
  const section = sections[params.section as Section];
  const [domains, setDomains] = useState(["7ink.com.au", "mramazing.online", "mramazing.org", "localhost"]);
  const [domainInput, setDomainInput] = useState("");
  const [domainError, setDomainError] = useState("");

  useEffect(() => {
    const savedDomains = window.localStorage.getItem("7ink-admin-domains");
    if (savedDomains) {
      setDomains(JSON.parse(savedDomains));
    }
  }, []);

  if (!section) {
    notFound();
  }

  function handleAddDomain(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const normalizedDomain = domainInput.trim().toLowerCase().replace(/^https?:\/\//, "").replace(/\/.*$/, "");

    if (!normalizedDomain || !/^(localhost|[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+)$/.test(normalizedDomain)) {
      setDomainError("Enter a valid domain, such as example.com.");
      return;
    }

    if (domains.includes(normalizedDomain)) {
      setDomainError("That domain is already linked.");
      return;
    }

    const updatedDomains = [...domains, normalizedDomain];
    setDomains(updatedDomains);
    window.localStorage.setItem("7ink-admin-domains", JSON.stringify(updatedDomains));
    setDomainInput("");
    setDomainError("");
  }

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
              const href = item === "Overview" ? "/admin/website" : item === "Projects" ? "/admin/dashboard" : `/admin/website/${item.toLowerCase()}`;
              const active = item.toLowerCase() === params.section || (item === "Domains" && params.section === "domains");
              return <Link key={item} href={href} style={{ color: active ? "#57d7ed" : "#8fa4c5", padding: "8px 12px", textDecoration: "none", fontSize: "11px" }}>{item}</Link>;
            })}
          </div>
          <Link href="/admin/apps" style={{ color: "#a9bad5", padding: "13px 16px", textDecoration: "none", fontSize: "12px" }}>• Apps</Link>
        </nav>
        <div style={{ marginTop: "auto" }}><Link href="/admin/settings" style={{ display: "block", color: "#a9bad5", padding: "13px 16px", textDecoration: "none", fontSize: "12px" }}>Settings</Link></div>
      </aside>

      <div style={{ flex: 1, minWidth: 0 }}>
        <header style={{ height: "76px", background: "#ffffff", borderBottom: "1px solid #dce4ef", display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 42px" }}>
          <div style={{ color: "#6b7d9b", fontSize: "12px" }}>Admin workspace / Website</div>
          <Link href="/admin/website" style={{ color: "#163b82", fontSize: "11px", textDecoration: "none", letterSpacing: "1px" }}>WEBSITE OVERVIEW</Link>
        </header>

        <main style={{ padding: "42px", maxWidth: "1000px" }}>
          <div style={{ marginBottom: "30px" }}>
            <div style={{ color: "#6b7d9b", fontSize: "10px", letterSpacing: "2px", marginBottom: "10px", textTransform: "uppercase" }}>{section.eyebrow}</div>
            <h1 style={{ fontFamily: "'Syne', sans-serif", fontSize: "32px", fontWeight: "800", margin: "0 0 8px" }}>{section.label}</h1>
            <p style={{ color: "#6b7d9b", fontSize: "13px", margin: 0 }}>{section.description}</p>
          </div>
          {section.label === "Domains" && (
            <section style={{ background: "#ffffff", border: "1px solid #e0e7f0", borderRadius: "14px", padding: "24px", marginBottom: "18px", boxShadow: "0 8px 22px rgba(30,57,96,0.05)" }}>
              <form onSubmit={handleAddDomain}>
                <label htmlFor="domain-input" style={{ display: "block", color: "#071a3d", fontSize: "13px", fontWeight: "600", marginBottom: "8px" }}>Add a domain</label>
                <div style={{ display: "flex", gap: "10px" }}>
                  <input id="domain-input" value={domainInput} onChange={event => setDomainInput(event.target.value)} placeholder="example.com" autoComplete="url" style={{ flex: 1, minWidth: 0, boxSizing: "border-box", border: "1px solid #cfd9e7", borderRadius: "8px", padding: "12px 14px", color: "#071a3d", fontFamily: "'DM Mono', monospace", fontSize: "12px" }} />
                  <button type="submit" style={{ border: "none", borderRadius: "8px", padding: "12px 16px", background: "#163b82", color: "#ffffff", fontFamily: "'DM Mono', monospace", fontSize: "11px", fontWeight: "700", letterSpacing: "0.5px", cursor: "pointer" }}>ADD DOMAIN</button>
                </div>
                {domainError && <div role="alert" style={{ color: "#c23737", fontSize: "11px", marginTop: "10px" }}>{domainError}</div>}
                <div style={{ color: "#8a9ab1", fontSize: "10px", marginTop: "10px" }}>Enter a domain name or paste a full URL. The protocol is removed automatically.</div>
              </form>
            </section>
          )}

          <section style={{ background: "#ffffff", border: "1px solid #e0e7f0", borderRadius: "14px", padding: "24px", boxShadow: "0 8px 22px rgba(30,57,96,0.05)" }}>
            {(section.label === "Domains" ? domains : section.items).map((item, index) => (
              <div key={item} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "17px 4px", borderBottom: index === section.items.length - 1 ? "none" : "1px solid #e7edf5" }}>
                {section.label === "Domains" ? (
                  <a href={item === "localhost" ? "http://localhost" : `https://${item}`} target="_blank" rel="noreferrer" style={{ color: "#163b82", fontSize: "13px", fontWeight: "600", textDecoration: "underline", textUnderlineOffset: "3px" }}>{item}</a>
                ) : (
                  <div style={{ color: "#071a3d", fontSize: "13px", fontWeight: "600" }}>{item}</div>
                )}
                {section.label === "Domains" && <span style={{ color: item === "localhost" ? "#2763bc" : "#4d9900", background: item === "localhost" ? "#e8f2ff" : "#eef8df", borderRadius: "999px", padding: "6px 10px", fontSize: "10px" }}>{item === "localhost" ? "Development" : "Connected"}</span>}
                {section.label !== "Domains" && <span style={{ color: "#2763bc", fontSize: "16px" }}>→</span>}
              </div>
            ))}
          </section>
        </main>
      </div>
    </div>
  );
}
