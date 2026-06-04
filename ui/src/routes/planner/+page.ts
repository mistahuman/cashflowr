import type { PageLoad } from './$types';
import { createSettingsApi, createMonthsApi } from '$lib/api/client';

export const prerender = false;

export const load: PageLoad = async ({ fetch }) => {
	const [settings, months] = await Promise.all([
		createSettingsApi(fetch).get(),
		createMonthsApi(fetch).list()
	]);
	return { settings, months };
};
