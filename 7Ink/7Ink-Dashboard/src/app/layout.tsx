// src/app/layout.tsx
import type { Metadata } from "next";
import SessionWrapper from "@/components/SessionWrapper";
import "./globals.css";

export const metadata: Metadata = {
  title: "7ink Admin",
  description: "7ink Admin Portal",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, padding: 0, background: "#0a0a0a" }}>
        <SessionWrapper>{children}</SessionWrapper>
      </body>
    </html>
  );
}
