// src/app/login/page.tsx
"use client";

import { Suspense, useEffect, useState } from "react";
import { signIn } from "next-auth/react";
import { useRouter, useSearchParams } from "next/navigation";

const meshBackgroundSvg = `data:image/svg+xml,${encodeURIComponent(`
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900">
    <rect width="1600" height="900" fill="transparent"/>
    <g fill="none" stroke="rgba(255,255,255,0.88)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M102 460 L332 165 L465 432 L403 648 L131 634 Z"/>
      <path d="M332 165 L517 273 L465 432 L403 648 L331 520 Z"/>
      <path d="M517 273 L698 170 L626 500 L465 432 Z"/>
      <path d="M131 634 L403 648 L331 520 L200 750 Z"/>
      <path d="M626 500 L698 170 L894 322 L796 618 L626 500 Z"/>
      <path d="M796 618 L894 322 L1094 428 L1056 698 L776 742 Z"/>
      <path d="M1094 428 L1292 247 L1442 451 L1385 675 L1056 698 Z"/>
      <path d="M1385 675 L1442 451 L1568 534 L1514 770 L1268 820 Z"/>
      <path d="M627 574 L796 618 L776 742 L594 712 Z"/>
      <path d="M594 712 L776 742 L778 874 L501 802 Z"/>
      <path d="M220 760 L331 520 L200 750 L121 862 Z"/>
      <path d="M501 802 L594 712 L627 574 L516 658 Z"/>
      <path d="M370 46 L533 146 L450 332 L361 234 Z"/>
      <path d="M978 194 L1096 109 L1218 170 L1140 322 L969 277 Z"/>
      <path d="M1188 185 L1420 151 L1336 464 L1168 330 Z"/>
      <path d="M1113 562 L1254 452 L1401 503 L1335 718 L1138 648 Z"/>
      <path d="M1278 820 L1514 770 L1350 893 L1128 848 Z"/>
      <path d="M143 238 L256 78 L340 202 L265 372 L98 318 Z"/>
      <path d="M212 468 L375 372 L504 455 L432 607 L240 620 Z"/>
      <path d="M865 661 L1016 601 L1113 757 L967 847 L796 799 Z"/>
      <path d="M1090 110 L1207 62 L1330 146 L1268 242 L1168 160 Z"/>
    </g>
    <g fill="rgba(255,255,255,0.95)" stroke="rgba(255,255,255,0.85)" stroke-width="0.8">
      <circle cx="102" cy="460" r="3"/>
      <circle cx="332" cy="165" r="3"/>
      <circle cx="465" cy="432" r="3"/>
      <circle cx="403" cy="648" r="3"/>
      <circle cx="131" cy="634" r="3"/>
      <circle cx="517" cy="273" r="3"/>
      <circle cx="698" cy="170" r="3"/>
      <circle cx="626" cy="500" r="3"/>
      <circle cx="796" cy="618" r="3"/>
      <circle cx="894" cy="322" r="3"/>
      <circle cx="1094" cy="428" r="3"/>
      <circle cx="1056" cy="698" r="3"/>
      <circle cx="1292" cy="247" r="3"/>
      <circle cx="1442" cy="451" r="3"/>
      <circle cx="1385" cy="675" r="3"/>
      <circle cx="1568" cy="534" r="3"/>
      <circle cx="1514" cy="770" r="3"/>
      <circle cx="1268" cy="820" r="3"/>
      <circle cx="594" cy="712" r="3"/>
      <circle cx="776" cy="742" r="3"/>
      <circle cx="778" cy="874" r="3"/>
      <circle cx="501" cy="802" r="3"/>
      <circle cx="200" cy="750" r="3"/>
      <circle cx="121" cy="862" r="3"/>
      <circle cx="516" cy="658" r="3"/>
      <circle cx="265" cy="372" r="3"/>
      <circle cx="98" cy="318" r="3"/>
      <circle cx="143" cy="238" r="3"/>
      <circle cx="256" cy="78" r="3"/>
      <circle cx="340" cy="202" r="3"/>
      <circle cx="220" cy="760" r="3"/>
      <circle cx="370" cy="46" r="3"/>
      <circle cx="533" cy="146" r="3"/>
      <circle cx="450" cy="332" r="3"/>
      <circle cx="361" cy="234" r="3"/>
      <circle cx="978" cy="194" r="3"/>
      <circle cx="1096" cy="109" r="3"/>
      <circle cx="1218" cy="170" r="3"/>
      <circle cx="1140" cy="322" r="3"/>
      <circle cx="969" cy="277" r="3"/>
      <circle cx="1188" cy="185" r="3"/>
      <circle cx="1420" cy="151" r="3"/>
      <circle cx="1336" cy="464" r="3"/>
      <circle cx="1168" cy="330" r="3"/>
      <circle cx="1113" cy="562" r="3"/>
      <circle cx="1254" cy="452" r="3"/>
      <circle cx="1401" cy="503" r="3"/>
      <circle cx="1335" cy="718" r="3"/>
      <circle cx="1138" cy="648" r="3"/>
      <circle cx="967" cy="847" r="3"/>
      <circle cx="796" cy="799" r="3"/>
      <circle cx="1016" cy="601" r="3"/>
      <circle cx="1090" cy="110" r="3"/>
      <circle cx="1207" cy="62" r="3"/>
      <circle cx="1330" cy="146" r="3"/>
      <circle cx="1268" cy="242" r="3"/>
      <circle cx="1168" cy="160" r="3"/>
    </g>
  </svg>
`)}`;

export default function LoginPage() {
  return (
    <Suspense fallback={<div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", color: "#c8ff00", fontFamily: "'DM Mono', monospace" }}>Loading…</div>}>
      <LoginForm />
    </Suspense>
  );
}

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [currentYear, setCurrentYear] = useState<number | null>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const isUnauthorized = searchParams.get("error") === "unauthorized";
  const callbackUrl = searchParams.get("callbackUrl") || "/admin/dashboard";

  useEffect(() => {
    setCurrentYear(new Date().getFullYear());
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const trimmedEmail = email.trim();
    const trimmedPassword = password.trim();

    if (!trimmedEmail || !trimmedPassword) {
      setError("Please enter both your email and password.");
      return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(trimmedEmail)) {
      setError("Please enter a valid email address.");
      return;
    }

    if (trimmedPassword.length < 6) {
      setError("Password must be at least 6 characters long.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const res = await signIn("credentials", {
        email: trimmedEmail,
        password: trimmedPassword,
        redirect: false,
      });

      if (res?.ok) {
        router.push(callbackUrl);
        return;
      }

      if (res?.error === "CredentialsSignin" || res?.status === 401) {
        setError("Invalid email or password.");
      } else {
        setError("Unable to sign in right now. Please try again.");
      }
    } catch {
      setError("Unable to sign in right now. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontFamily: "'DM Mono', monospace",
      backgroundColor: "#050505",
      backgroundImage: `radial-gradient(circle at top, rgba(200,255,0,0.08), transparent 28%), url("${meshBackgroundSvg}")`,
      backgroundSize: "cover, cover",
      backgroundPosition: "center, center",
      backgroundRepeat: "no-repeat, no-repeat",
      position: "relative",
      overflow: "hidden",
      padding: "24px",
    }}>
      <div style={{
        position: "absolute",
        inset: 0,
        backgroundImage: "linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px)",
        backgroundSize: "24px 24px",
        maskImage: "radial-gradient(circle at center, black 30%, transparent 100%)",
      }} />

      <div style={{
        width: "100%",
        maxWidth: "860px",
        position: "relative",
        zIndex: 1,
      }}>
        <div style={{
          display: "grid",
          gridTemplateColumns: "0.95fr 1.05fr",
          borderRadius: "22px",
          overflow: "hidden",
          background: "rgba(17,17,17,0.9)",
          border: "1px solid rgba(255,255,255,0.07)",
          boxShadow: "0 24px 64px rgba(0,0,0,0.45)",
        }}>
          <div style={{
            background: "linear-gradient(160deg, rgba(200,255,0,0.08), rgba(200,255,0,0.02) 26%, rgba(255,255,255,0.01) 100%)",
            borderRight: "1px solid rgba(255,255,255,0.04)",
            padding: "34px 30px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
          }}>
            <div style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "8px",
              marginBottom: "22px",
              color: "#c8ff00",
              fontSize: "10px",
              letterSpacing: "2.5px",
              textTransform: "uppercase",
            }}>
              <span style={{
                width: "7px",
                height: "7px",
                borderRadius: "50%",
                background: "#c8ff00",
                boxShadow: "0 0 14px rgba(200,255,0,0.8)",
              }} />
              Secure access
            </div>

            <div style={{
              fontFamily: "'Syne', sans-serif",
              fontSize: "48px",
              lineHeight: 1,
              fontWeight: "800",
              letterSpacing: "-1.6px",
              color: "#f4f4f4",
              marginBottom: "14px",
            }}>
              7ink
            </div>

            <div style={{
              color: "#a0a0a0",
              fontSize: "13px",
              lineHeight: "1.8",
              maxWidth: "320px",
              marginBottom: "24px",
            }}>
              Manage projects, talent, and day-to-day operations from one secure admin workspace.
            </div>

            <div style={{
              display: "flex",
              gap: "10px",
              flexWrap: "wrap",
            }}>
              {[
                "Projects",
                "Analytics",
                "Users",
                "Operations",
              ].map((item) => (
                <div key={item} style={{
                  border: "1px solid rgba(200,255,0,0.2)",
                  background: "rgba(200,255,0,0.04)",
                  color: "#d9ff66",
                  borderRadius: "999px",
                  padding: "8px 12px",
                  fontSize: "10px",
                  letterSpacing: "1.5px",
                  textTransform: "uppercase",
                }}>
                  {item}
                </div>
              ))}
            </div>
          </div>

          <div style={{
            padding: "34px 30px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            background: "rgba(10,10,10,0.8)",
          }}>
            <div style={{ width: "100%", maxWidth: "340px" }}>
              <div style={{ marginBottom: "24px" }}>
                <div style={{
                  color: "#666",
                  fontSize: "10px",
                  letterSpacing: "2px",
                  marginBottom: "8px",
                  textTransform: "uppercase",
                }}>
                  Admin portal
                </div>
                <div style={{
                  fontFamily: "'Syne', sans-serif",
                  fontSize: "30px",
                  fontWeight: "800",
                  letterSpacing: "-1.1px",
                  color: "#f5f5f5",
                }}>
                  Sign in
                </div>
              </div>

              {isUnauthorized && (
                <div style={{
                  background: "rgba(255,60,60,0.08)",
                  border: "1px solid rgba(255,60,60,0.28)",
                  borderRadius: "10px",
                  padding: "12px 14px",
                  marginBottom: "18px",
                  color: "#ff8c8c",
                  fontSize: "12px",
                }}>
                  You don't have permission to access that page.
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: "18px" }}>
                  <label style={{ display: "block", color: "#8a8a8a", fontSize: "10px", letterSpacing: "2px", marginBottom: "8px", textTransform: "uppercase" }}>
                    Email
                  </label>
                  <input
                    className="login-input"
                    type="email"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    autoComplete="email"
                    placeholder="admin@7ink.com.au"
                    aria-label="Email"
                    style={{
                      width: "100%",
                      background: "rgba(6,6,6,0.9)",
                      border: "1px solid rgba(255,255,255,0.08)",
                      borderRadius: "10px",
                      padding: "13px 14px",
                      color: "#e8e8e8",
                      fontSize: "14px",
                      fontFamily: "'DM Mono', monospace",
                    }}
                  />
                </div>

                <div style={{ marginBottom: "16px" }}>
                  <label style={{ display: "block", color: "#8a8a8a", fontSize: "10px", letterSpacing: "2px", marginBottom: "8px", textTransform: "uppercase" }}>
                    Password
                  </label>
                  <div style={{ position: "relative" }}>
                    <input
                      className="login-input"
                      type={showPassword ? "text" : "password"}
                      value={password}
                      onChange={e => setPassword(e.target.value)}
                      autoComplete="current-password"
                      placeholder="Enter password"
                      aria-label="Password"
                      style={{
                        width: "100%",
                        background: "rgba(6,6,6,0.9)",
                        border: "1px solid rgba(255,255,255,0.08)",
                        borderRadius: "10px",
                        padding: "13px 50px 13px 14px",
                        color: "#e8e8e8",
                        fontSize: "14px",
                        fontFamily: "'DM Mono', monospace",
                      }}
                    />
                    <button
                      type="button"
                      aria-label={showPassword ? "Hide password" : "Show password"}
                      onClick={() => setShowPassword(prev => !prev)}
                      style={{
                        position: "absolute",
                        right: "12px",
                        top: "50%",
                        transform: "translateY(-50%)",
                        border: "none",
                        background: "transparent",
                        color: "#a0a0a0",
                        fontSize: "10px",
                        fontFamily: "'DM Mono', monospace",
                        letterSpacing: "1px",
                        cursor: "pointer",
                      }}
                    >
                      {showPassword ? "HIDE" : "SHOW"}
                    </button>
                  </div>
                </div>

                <div style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: "18px",
                  color: "#777",
                  fontSize: "10px",
                  letterSpacing: "1px",
                }}>
                  <span>Secure access</span>
                  <button
                    type="button"
                    onClick={() => setError("Contact your administrator to reset your password.")}
                    style={{
                      background: "transparent",
                      border: "none",
                      color: "#c8ff00",
                      font: "inherit",
                      cursor: "pointer",
                      textDecoration: "underline",
                    }}
                  >
                    Forgot password?
                  </button>
                </div>

                {error && (
                  <div style={{
                    color: "#ff8c8c",
                    fontSize: "12px",
                    marginBottom: "16px",
                    textAlign: "center",
                  }}>{error}</div>
                )}

                <button
                  className="login-btn"
                  type="submit"
                  disabled={loading}
                  style={{
                    width: "100%",
                    background: "linear-gradient(135deg, #c8ff00 0%, #d9ff4d 100%)",
                    color: "#0a0a0a",
                    border: "none",
                    borderRadius: "10px",
                    padding: "14px 16px",
                    fontSize: "12px",
                    fontWeight: "700",
                    fontFamily: "'DM Mono', monospace",
                    letterSpacing: "2px",
                    cursor: "pointer",
                    transition: "all 0.2s",
                    boxShadow: "0 12px 24px rgba(200,255,0,0.2)",
                  }}
                >
                  {loading ? "SIGNING IN..." : "SIGN IN →"}
                </button>

                <div style={{
                  marginTop: "18px",
                  color: "#777",
                  fontSize: "11px",
                  textAlign: "center",
                }}>
                  Don't have an account?{" "}
                  <a href="/signup" style={{
                    color: "#c8ff00",
                    textDecoration: "underline",
                    textUnderlineOffset: "3px",
                  }}>
                    Sign up
                  </a>
                </div>
              </form>
            </div>
          </div>
        </div>

        <div style={{ textAlign: "center", marginTop: "16px", color: "#4a4a4a", fontSize: "10px", letterSpacing: "1px" }}>
          7ink.com.au © {currentYear ?? ""}
        </div>
      </div>
    </div>
  );
}
