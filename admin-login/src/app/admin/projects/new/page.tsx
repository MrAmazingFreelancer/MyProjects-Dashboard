import Link from "next/link";

export default function NewProjectPage() {
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

      <main style={{ padding: "48px 40px", maxWidth: "640px" }}>
        <div style={{ marginBottom: "32px" }}>
          <h1 style={{
            fontFamily: "'Syne', sans-serif",
            fontSize: "32px",
            fontWeight: "800",
            margin: "0 0 8px",
          }}>
            New project
          </h1>
          <p style={{ color: "#666", fontSize: "13px", margin: 0 }}>
            Add a project to your admin workspace.
          </p>
        </div>

        <form style={{
          background: "#111",
          border: "1px solid #1a1a1a",
          borderRadius: "12px",
          padding: "32px",
        }}>
          <label style={{ display: "block", color: "#888", fontSize: "11px", letterSpacing: "2px", marginBottom: "8px" }}>
            PROJECT NAME
          </label>
          <input
            type="text"
            name="name"
            placeholder="My project"
            required
            style={{
              boxSizing: "border-box",
              width: "100%",
              background: "#0a0a0a",
              border: "1px solid #2a2a2a",
              borderRadius: "8px",
              padding: "12px 16px",
              color: "#e0e0e0",
              fontSize: "14px",
              fontFamily: "'DM Mono', monospace",
              marginBottom: "24px",
            }}
          />

          <label style={{ display: "block", color: "#888", fontSize: "11px", letterSpacing: "2px", marginBottom: "8px" }}>
            PROJECT URL
          </label>
          <input
            type="url"
            name="url"
            placeholder="https://example.com"
            required
            style={{
              boxSizing: "border-box",
              width: "100%",
              background: "#0a0a0a",
              border: "1px solid #2a2a2a",
              borderRadius: "8px",
              padding: "12px 16px",
              color: "#e0e0e0",
              fontSize: "14px",
              fontFamily: "'DM Mono', monospace",
              marginBottom: "28px",
            }}
          />

          <div style={{ display: "flex", gap: "12px" }}>
            <Link href="/admin/dashboard" style={{
              flex: 1,
              border: "1px solid #2a2a2a",
              borderRadius: "8px",
              padding: "14px",
              color: "#888",
              fontSize: "12px",
              textAlign: "center",
              textDecoration: "none",
            }}>
              CANCEL
            </Link>
            <button type="submit" disabled style={{
              flex: 1,
              border: "none",
              borderRadius: "8px",
              padding: "14px",
              background: "#333",
              color: "#777",
              fontSize: "12px",
              fontFamily: "'DM Mono', monospace",
              cursor: "not-allowed",
            }}>
              SAVE PROJECT
            </button>
          </div>
          <p style={{ color: "#555", fontSize: "11px", lineHeight: 1.6, margin: "20px 0 0" }}>
            Project storage is not configured yet. The page is ready for the Project database model and save action.
          </p>
        </form>
      </main>
    </div>
  );
}
