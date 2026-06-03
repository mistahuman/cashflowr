import type { PageLoad } from './$types';
import { createMonthsApi } from '$lib/api/client';

export const prerender = false;

export const load: PageLoad = async ({ fetch }) => {
	const months = await createMonthsApi(fetch).list();
	return { months };
};
