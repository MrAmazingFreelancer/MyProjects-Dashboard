# MyProjects-Dashboard

**A curated collection of 50+ active & reference projects spanning multiple languages and frameworks.**

## Workspace Structure

### 🚀 Active Projects (You Own)

**Web Applications:**
- **admin-login** (Next.js + Prisma + NextAuth) — Admin panel with authentication
- **coding-agent-template** (Next.js + Drizzle + Radix UI) — Copilot agent scaffolding framework
- **VideoPlayer** (Next.js + ImageKit) — HLS video player with watermarking & subtitles
- **hometube** (Python + Streamlit) — Self-hosted video downloader & organizer

**Telegram Bots:**
- **CloneBot_V2** (Python + Pyrogram + Gclone) — Google Drive cloner bot; bypasses 750GB limit
- **Auto-Forward-Bot TG** (Python + Pyrogram) — Auto-forward messages between Telegram channels

**Libraries & Plugins (Issues/PR Branches):**
- **hls.js** (TypeScript, branch: `MrAmazingFreelancer/issue4289`) — HLS streaming client library
- **http-streaming** (TypeScript, branch: `MrAmazingFreelancer/issue1597`) — Video.js HTTP streaming plugin
- **gitprofile** (Vite + React, upstream: master) — GitHub portfolio generator

**Utilities:**
- **webdav** (Go, fork) — Lightweight WebDAV server

### 📚 Reference Forks
Git, Git-for-Windows, Github repositories, open-in-vlc, oss-fuzz, and others for reference or contribution.

### 🏢 Workspace Configuration
- **VS Code Settings**: `d:\MyProjects-Dashboard\.vscode\settings.json`
  - Cloud sync enabled (`chat.sessionSync.enabled: true`)
  - Copilot codesearch enabled
  - MCP discovery active
- **Copilot Instructions**: Each project has `.github/copilot-instructions.md` with tech stack, commands, patterns

---

## Tech Stack Summary

| Stack | Projects |
|-------|----------|
| **Node.js/TypeScript** | admin-login, coding-agent-template, VideoPlayer, gitprofile, hls.js, http-streaming |
| **Python** | CloneBot_V2, Auto-Forward-Bot TG, hometube |
| **Go** | webdav |
| **Frontend** | React, Next.js, Vite, Streamlit |
| **Databases** | PostgreSQL (Prisma), Neon (Drizzle) |
| **APIs** | GitHub (Octokit), Telegram (Pyrogram), ImageKit, Google Drive (Gclone) |

---

## Recommended Workflows

### Starting Work
1. Open the specific project folder in VS Code
2. The `.github/copilot-instructions.md` file will auto-load into Copilot context
3. See the file for tech stack, commands, and patterns for that project

### Multi-Project Context
- Use `/agent @Explore` subagent for cross-project questions (keeps context lightweight)
- Reference the workspace structure above when navigating between projects

### Common Tasks
- **Dev Server**: Each project has `npm run dev` or equivalent; check its instructions
- **Building**: `npm run build` (JS), `go build` (Go), `docker build` (Docker)
- **Testing**: `npm run test`, `go test ./...`, or project-specific commands
- **Database Changes** (Next.js/Prisma projects): `npm run db:push` after schema changes

---

## Session Management
- If a session gets long (50+ turns), use `/compact` to summarize context
- For CLI tasks with many steps, write out the full goal upfront
- Cloud sync is enabled; sessions persist across devices

---

## Useful Links
- **Admin-login DB**: Run `npm run db:studio` to inspect Prisma database
- **Coding Agent**: Study `coding-agent-template` as a template for new agents
- **VideoPlayer**: ImageKit free tier for adaptive streaming
- **WebDAV**: RFC 4918 compatible; works with all standard clients
