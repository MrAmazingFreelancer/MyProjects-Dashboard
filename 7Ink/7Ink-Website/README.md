# 7ink.com.au Website

Website deployment for 7ink.com.au using Vercel + Cloudflare

## Quick Start

See [QUICK_SETUP.md](QUICK_SETUP.md) for deployment instructions.

## Setup

- **Domain**: Crazy Domains (7ink.com.au)
- **DNS**: Cloudflare
- **Deployment**: Vercel
- **Repository**: GitHub

## Files

- `package.json` - Build configuration
- `vercel.json` - Vercel deployment settings
- `.gitignore` - Git ignore rules
- `DEPLOYMENT_GUIDE.md` - Complete setup guide
- `QUICK_SETUP.md` - Quick reference guide

## Development

Work on files locally in the xampp repo:
```bash
d:\xampp\htdocs\7ink.local
```

When ready to deploy, push to this repo for Vercel auto-deployment.

## Local Development

```bash
cd d:\xampp\htdocs\7ink.local
# Edit files
# Test locally
```

## Deploy to Vercel

Push to this repository:
```bash
git push origin main
```

Vercel will automatically detect changes and deploy.

## Cloudflare Stream Direct Upload Setup

To enable direct creator uploads from `CloudflareVideoPlayer.html`, add these Vercel Environment Variables:

- `CLOUDFLARE_ACCOUNT_ID` - Your Cloudflare account ID.
- `CLOUDFLARE_STREAM_API_TOKEN` - API token with Stream write permissions.

After adding environment variables, redeploy the project so `/api/stream-upload-url` can issue one-time upload URLs securely.
