# Admin Login Project

## Stack
- **Runtime**: Node.js 18+
- **Framework**: Next.js 14 (app router)
- **ORM**: Prisma 5
- **Auth**: NextAuth v4 + Prisma adapter
- **DB**: PostgreSQL (via Prisma)
- **Security**: bcryptjs for password hashing
- **TypeScript**: v5 strict mode

## Project Structure
```
src/
  app/          # Next.js app router pages
  auth/         # Auth middleware & providers
  prisma/       # Schema + migrations
  scripts/      # DB utilities
```

## Key Patterns
- **Authentication**: NextAuth.js with Prisma adapter; session stored in DB
- **Database**: All schema in `prisma/schema.prisma`; use `prisma studio` for debugging
- **Middleware**: Auth checks in `src/auth/middleware.ts`
- **Build**: Runs `prisma generate` before Next.js build

## Common Commands
```bash
npm run dev           # Start dev server (http://localhost:3000)
npm run build         # Build + generate Prisma client
npm run start         # Start production server
npm run lint          # ESLint + TypeScript check
npm run db:push       # Sync schema to DB (dev only)
npm run db:studio     # Open Prisma Studio (visual DB explorer)
```

## Important Files
- `prisma/schema.prisma` — data model; sync to DB with `npm run db:push`
- `src/auth/middleware.ts` — auth flow for protected routes
- `src/app/layout.tsx` — root layout + providers

## Notes
- Never commit `.env.local` (add to `.gitignore`)
- Prisma client auto-generates; run `prisma generate` if types are stale
- Always run `npm run build` locally before pushing (catches Prisma + type errors)
