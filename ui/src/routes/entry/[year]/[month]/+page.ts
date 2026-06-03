import type { PageLoad } from './$types';
import { createMonthsApi } from '$lib/api/client';

export const prerender = false;

export const load: PageLoad = async ({ params, fetch }) => {
	const year = parseInt(params.year);
	const month = parseInt(params.month);
	const entry = await createMonthsApi(fetch).get(year, month);
	return { entry };
};
