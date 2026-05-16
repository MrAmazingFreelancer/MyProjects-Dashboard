// src/app/login/page.tsx
"use client";

import { useState } from "react";
import { signIn } from "next-auth/react";
import { useRouter, useSearchParams } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const isUnauthorized = searchParams.get("error") === "unauthorized";

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    const res = await signIn("credentials", {
      email,
      password,
      redirect: false,
    });

    if (res?.error) {
      setError("Invalid email or password");
      setLoading(false);
    } else {
      router.push("/admin/dashboard");
    }
  }

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0a0a0a",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontFamily: "'DM Mono', monospace",
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@700;800&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        input:-webkit-autofill { -webkit-box-shadow: 0 0 0 30px #111 inset !important; -webkit-text-fill-color: #e0e0e0 !important; }
        .login-input:focus { outline: none; border-color: #c8ff00 !important; box-shadow: 0 0 0 2px rgba(200,255,0,0.15); }
        .login-btn:hover { background: #d4ff1a !important; transform: translateY(-1px); }
        .login-btn:active { transform: translateY(0); }
        .login-btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
      `}</style>

      <div style={{
        width: "100%",
        maxWidth: "420px",
        padding: "0 24px",
      }}>
        {/* Logo */}
        <div style={{ textAlign: "center", marginBottom: "48px" }}>
          <div style={{
            fontFamily: "'Syne', sans-serif",
            fontSize: "36px",
            fontWeight: "800",
            color: "#c8ff00",
            letterSpacing: "-1px",
          }}>7ink</div>
          <div style={{ color: "#444", fontSize: "12px", marginTop: "4px", letterSpacing: "3px" }}>ADMIN PORTAL</div>
        </div>

        {/* Card */}
        <div style={{
          background: "#111",
          border: "1px solid #222",
          borderRadius: "12px",
          padding: "40px",
        }}>
          {isUnauthorized && (
            <div style={{
              background: "rgba(255,60,60,0.1)",
              border: "1px solid rgba(255,60,60,0.3)",
              borderRadius: "8px",
              padding: "12px 16px",
              marginBottom: "24px",
              color: "#ff6060",
              fontSize: "13px",
            }}>
              You don't have permission to access that page.
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: "20px" }}>
              <label style={{ display: "block", color: "#666", fontSize: "11px", letterSpacing: "2px", marginBottom: "8px" }}>
                EMAIL
              </label>
              <input
                className="login-input"
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
                style={{
                  width: "100%",
                  background: "#0a0a0a",
                  border: "1px solid #2a2a2a",
                  borderRadius: "8px",
                  padding: "12px 16px",
                  color: "#e0e0e0",
                  fontSize: "14px",
                  fontFamily: "'DM Mono', monospace",
                  transition: "all 0.2s",
                }}
              />
            </div>

            <div style={{ marginBottom: "28px" }}>
              <label style={{ display: "block", color: "#666", fontSize: "11px", letterSpacing: "2px", marginBottom: "8px" }}>
                PASSWORD
              </label>
              <input
                className="login-input"
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
                style={{
                  width: "100%",
                  background: "#0a0a0a",
                  border: "1px solid #2a2a2a",
                  borderRadius: "8px",
                  padding: "12px 16px",
                  color: "#e0e0e0",
                  fontSize: "14px",
                  fontFamily: "'DM Mono', monospace",
                  transition: "all 0.2s",
                }}
              />
            </div>

            {error && (
              <div style={{
                color: "#ff6060",
                fontSize: "13px",
                marginBottom: "20px",
                textAlign: "center",
              }}>{error}</div>
            )}

            <button
              className="login-btn"
              type="submit"
              disabled={loading}
              style={{
                width: "100%",
                background: "#c8ff00",
                color: "#0a0a0a",
                border: "none",
                borderRadius: "8px",
                padding: "14px",
                fontSize: "13px",
                fontWeight: "500",
                fontFamily: "'DM Mono', monospace",
                letterSpacing: "2px",
                cursor: "pointer",
                transition: "all 0.2s",
              }}
            >
              {loading ? "SIGNING IN..." : "SIGN IN →"}
            </button>
          </form>
        </div>

        <div style={{ textAlign: "center", marginTop: "24px", color: "#333", fontSize: "11px" }}>
          7ink.com.au © {new Date().getFullYear()}
        </div>
      </div>
    </div>
  );
}
