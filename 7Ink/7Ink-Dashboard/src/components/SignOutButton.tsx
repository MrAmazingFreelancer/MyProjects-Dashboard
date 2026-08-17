// src/components/SignOutButton.tsx
"use client";
import { signOut } from "next-auth/react";

export default function SignOutButton() {
  return (
    <button
      onClick={() => signOut({ callbackUrl: "/login" })}
      style={{
        background: "transparent",
        border: "1px solid #2a2a2a",
        borderRadius: "6px",
        color: "#666",
        padding: "6px 14px",
        fontSize: "11px",
        letterSpacing: "1px",
        cursor: "pointer",
        fontFamily: "'DM Mono', monospace",
        transition: "all 0.2s",
      }}
      onMouseOver={e => {
        (e.target as HTMLButtonElement).style.borderColor = "#c8ff00";
        (e.target as HTMLButtonElement).style.color = "#c8ff00";
      }}
      onMouseOut={e => {
        (e.target as HTMLButtonElement).style.borderColor = "#2a2a2a";
        (e.target as HTMLButtonElement).style.color = "#666";
      }}
    >
      SIGN OUT
    </button>
  );
}
