# 7ink Admin Portal

A Next.js admin portal with NextAuth.js email/password login, Prisma ORM, and role-based access control.

## Setup Steps

### 1. Install dependencies
```bash
npm install
```

### 2. Set up a free database
Go to **https://neon.tech** → create a free account → create a new project → copy the connection string.

### 3. Configure environment variables
Copy `.env.local.example` to `.env.local` and fill in:
```bash
cp .env.local.example .env.local
```

Edit `.env.local`:
- `DATABASE_URL` → paste your Neon.tech connection string
- `NEXTAUTH_SECRET` → run `openssl rand -base64 32` in terminal and paste the result
- `NEXTAUTH_URL` → `https://7ink.com.au`

### 4. Push database schema
```bash
npm run db:push
```

### 5. Create your first admin user
Edit `scripts/create-admin.ts` and change the email and password, then run:
```bash
npx ts-node --compiler-options '{"module":"commonjs"}' scripts/create-admin.ts
```

### 6. Run locally
```bash
npm run dev
```
Visit http://localhost:3000/login

### 7. Deploy to Vercel
```bash
# Push to GitHub first, then connect repo in Vercel
# Add environment variables in Vercel dashboard:
# Settings → Environment Variables → add DATABASE_URL, NEXTAUTH_SECRET, NEXTAUTH_URL
```

## Adding More Users
Use Prisma Studio to manage users:
```bash
npm run db:studio
```

Or create another script similar to `scripts/create-admin.ts` with `role: "user"`.

## Adding Projects
Edit `src/app/admin/dashboard/page.tsx` and add entries to the `projects` array.

Each project can be:
- A page within this Next.js app at `/admin/projects/yourapp`
- An iframe embedding another URL
- A link to a separate Vercel deployment
