import Link from "next/link";

export default function NotFound() {
  return (
    <main style={styles.page}>
      <section style={styles.wrap} aria-labelledby="not-found-title">
        <h1 style={styles.code}>404</h1>
        <h2 style={styles.title} id="not-found-title">
          Page Not Found
        </h2>
        <p style={styles.message}>
          The page you are looking for does not exist or has been moved.
        </p>
        <Link href="/login" style={styles.link}>
          Back to Login
        </Link>
      </section>
    </main>
  );
}

const styles: Record<string, React.CSSProperties> = {
  page: {
    minHeight: "100vh",
    margin: 0,
    display: "grid",
    placeItems: "center",
    textAlign: "center",
    padding: "24px",
    color: "#ffffff",
    background:
      "radial-gradient(circle at 20% 20%, #1c1c1c 0%, #111111 45%, #090909 100%)",
    fontFamily: 'Montserrat, "Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
  },
  wrap: {
    maxWidth: "720px",
  },
  code: {
    margin: 0,
    lineHeight: 0.9,
    fontWeight: 900,
    fontSize: "clamp(92px, 24vw, 220px)",
    letterSpacing: "8px",
    color: "transparent",
    WebkitTextStroke: "2px #ffffff",
    textShadow: "0 0 40px rgba(255,255,255,0.15)",
  },
  title: {
    margin: "12px 0 8px",
    textTransform: "uppercase",
    letterSpacing: "2px",
    fontWeight: 700,
    fontSize: "clamp(24px, 4vw, 34px)",
  },
  message: {
    margin: "0 0 28px",
    color: "#b8b8b8",
    fontSize: "16px",
  },
  link: {
    display: "inline-block",
    textDecoration: "none",
    color: "#111111",
    background: "#ffd166",
    textTransform: "uppercase",
    letterSpacing: "1px",
    fontWeight: 700,
    padding: "12px 20px",
    borderRadius: "999px",
  },
};
