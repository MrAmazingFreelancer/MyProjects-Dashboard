# 7Ink Platform Shared Material

This directory is the home for material shared by the 7Ink applications.

## Ownership

- `architecture/`: system boundaries, decisions, and deployment notes
- `database/`: shared schema decisions, migration plans, and seed conventions
- `packages/`: reusable types, validation, UI, and configuration packages when they are needed by more than one application

The dashboard currently owns its Prisma runtime and schema. Extract shared database code here only after the website or another application needs the same models.
