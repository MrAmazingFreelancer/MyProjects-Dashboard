/** @type {import('next').NextConfig} */
const nextConfig = {
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
