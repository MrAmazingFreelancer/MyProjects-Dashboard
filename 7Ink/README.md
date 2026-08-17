# 7Ink Platform

This directory contains the 7ink.com.au applications and shared platform material.

## Applications

- `7Ink-Website`: public 7ink.com.au website
- `7Ink-Dashboard`: staff and admin application
- `7Ink-Platform`: shared architecture, database planning, and reusable platform material

Keep application-specific routes, authentication, and deployment configuration inside the owning application. Put shared contracts and infrastructure planning in `7Ink-Platform` only when more than one application consumes them.

## Local development

Run commands from the application directory you are working on. For the dashboard:

```powershell
cd 7Ink-Dashboard
npm run dev
```
