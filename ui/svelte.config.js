import adapterNode from '@sveltejs/adapter-node';
import adapterStatic from '@sveltejs/adapter-static';

const isDocker = process.env.DOCKER_BUILD === 'true';

// When deploying to GitHub Pages the repo name becomes the base path.
const base = process.env.GITHUB_REPOSITORY ? '/' + process.env.GITHUB_REPOSITORY.split('/')[1] : '';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	compilerOptions: {
		runes: ({ filename }) => (filename.split(/[/\\]/).includes('node_modules') ? undefined : true)
	},
	kit: {
		adapter: isDocker
			? adapterNode()
			: adapterStatic({ fallback: '404.html' }),
		...(!isDocker && {
			paths: { base },
			prerender: {
				handleHttpError: ({ path, message }) => {
					if (/\.(svg|ico|png|webp|jpg|jpeg|gif|woff2?)$/.test(path)) return;
					throw new Error(message);
				}
			}
		})
	}
};

export default config;
