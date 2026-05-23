import "@/styles/globals.css";
import "@/styles/layout.css";
import { ImageKitProvider } from "@imagekit/next";
import Link from "next/link";
import ParticlesBackground from "@/components/ParticlesBackground";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const urlEndpoint =
    process.env.NEXT_PUBLIC_IMAGEKIT_URL_ENDPOINT ||
    "https://ik.imagekit.io/mramazing/VPData";

  return (
    <html lang="en">
      <body>
        <ImageKitProvider urlEndpoint={urlEndpoint}>
          <ParticlesBackground />
          <div className="app-layer">
            <nav className="nav">
              <div className="nav-container">
                <Link href="/VideoPlayer" className="nav-logo">
                  <span className="nav-logo-mark">7</span>
                  <span className="nav-logo-text">
                    <strong>7ink</strong>
                    <span>VideoPlayer</span>
                  </span>
                </Link>
                <div className="nav-links">
                  <Link href="/VideoPlayer" className="nav-link">
                    Library
                  </Link>
                  <Link href="/v10" className="nav-link">
                    v10 Lab
                  </Link>
                  <Link href="/upload" className="nav-button">
                    Upload
                  </Link>
                  <Link href="/avatar" className="nav-link">
                    Avatar
                  </Link>
                </div>
              </div>
            </nav>
            <main className="main">{children}</main>
          </div>
        </ImageKitProvider>
      </body>
    </html>
  );
}
