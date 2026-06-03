# SvelteKit Skeleton Starter

A starter template for building web apps with [SvelteKit](https://kit.svelte.dev) and [Skeleton UI](https://skeleton.dev).

## Stack

- **SvelteKit** with Svelte 5 (runes mode)
- **Skeleton UI** v4 + Tailwind CSS v4
- **TypeScript**
- Prettier + ESLint

## Getting started

Clone and install:

```sh
git clone git@github.com:mistahuman/sveltekit-skeleton-starter.git
cd sveltekit-skeleton-starter
npm install
```

Copy the environment file:

```sh
cp env.sample .env
```

Start the dev server:

```sh
npm run dev
```

## Scripts

| Command           | Description                    |
| ----------------- | ------------------------------ |
| `npm run dev`     | Start dev server               |
| `npm run build`   | Production build               |
| `npm run preview` | Preview the production build   |
| `npm run check`   | Type-check with `svelte-check` |
| `npm run lint`    | Prettier + ESLint check        |
| `npm run format`  | Auto-format with Prettier      |

## Adapters

The project supports two build targets via the `DOCKER_BUILD` environment variable:

| Context             | Adapter          | Output                        |
| ------------------- | ---------------- | ----------------------------- |
| Default             | `adapter-static` | Static files for GitHub Pages |
| `DOCKER_BUILD=true` | `adapter-node`   | Node.js server on port 3000   |

### GitHub Pages

Deployments to GitHub Pages are handled automatically by the included GitHub Actions workflow on every push to `main`.

### Docker

When used as part of [fullstack-webapp-starter](https://github.com/mistahuman/fullstack-webapp-starter), the `Dockerfile` sets `DOCKER_BUILD=true` at build time, switching to `adapter-node` and exposing a server on port 3000.

## Recreate from scratch

```sh
npx sv@0.15.2 create --template minimal --types ts \
  --add prettier eslint tailwindcss="plugins:typography,forms" \
  sveltekit-adapter="adapter:auto" mcp="ide:claude-code+setup:remote" \
  --install npm sveltekit-skeleton-starter
```
