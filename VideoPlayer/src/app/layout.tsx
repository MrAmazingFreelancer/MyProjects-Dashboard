import "@/styles/globals.css";
import "@/styles/layout.css";
import { ImageKitProvider } from "@imagekit/next";
import Link from "next/link";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <ImageKitProvider urlEndpoint={process.env.NEXT_PUBLIC_IMAGEKIT_URL_ENDPOINT!}>
          <nav className="nav">
            <div className="nav-container">
              <Link href="/" className="nav-logo">
                VideoPlayer
              </Link>
              <div className="nav-links">
                <Link href="/" className="nav-link">
                  Library
                </Link>
                <Link href="/upload" className="nav-button">
                  Upload
                </Link>
              </div>
            </div>
          </nav>
          <main className="main">{children}</main>
        </ImageKitProvider>
      </body>
    </html>
  );
}
