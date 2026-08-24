# GitProfile

## Stack
- **Runtime**: Node.js 18+
- **Framework**: Vite (modern bundler)
- **UI**: React 19 with TypeScript
- **Styling**: Tailwind CSS
- **Linting**: ESLint, Prettier
- **Blog Integration**: blog-js library

## Project Structure
```
src/
  components/         # React components
  pages/              # Page layouts
  styles/             # Tailwind CSS
  App.tsx             # Root component
index.html            # HTML entry point
vite.config.ts        # Vite configuration
```

## Key Patterns
- **Automatic Portfolio**: Pulls data from GitHub profile to generate portfolio site
- **Configurable**: Customizable via config file (colors, sections, links)
- **Static Generation**: Builds to static HTML/CSS/JS
- **Blog Integration**: Uses @arifszn/blog-js for blog posts
- **Responsive**: Mobile-first with Tailwind

## Common Commands
```bash
npm install                    # Install dependencies
npm run dev                    # Vite dev server (http://localhost:5173)
npm run build                  # Production build → dist/
npm run lint                   # ESLint check
npm run lint:fix               # Auto-fix linting issues
npm run prettier               # Check code formatting
npm run prettier:fix           # Auto-format all files
npm run preview                # Preview production build locally
```

## Important Files
- `src/App.tsx` — Main app component
- `src/components/` — Reusable UI components
- `public/config.json` — Profile configuration
- `vite.config.ts` — Build & dev server config

## Notes
- This is a forked copy of arifszn/gitprofile; upstream is at `master` branch (default is `main`)
- Vite rebuilds very fast; dev experience is smooth
- Before pushing, run both `lint` and `prettier:fix`
- GitHub Actions likely generate the portfolio automatically on pushes
