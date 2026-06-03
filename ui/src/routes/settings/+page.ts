import type { PageLoad } from './$types';
import { createSettingsApi } from '$lib/api/client';

export const prerender = false;

export const load: PageLoad = async ({ fetch }) => {
	const settings = await createSettingsApi(fetch).get();
	return { settings };
};
