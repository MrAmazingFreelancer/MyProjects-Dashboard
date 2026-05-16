// next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow embedding other projects in iframes within /admin
  async headers() {
    return [
      {
        source: "/admin/:path*",
        headers: [
          { key: "X-Frame-Options", value: "SAMEORIGIN" },
        ],
      },
    ];
  },
};

export default nextConfig;
