import type { PageLoad } from './$types';
import { createSummaryApi, createMonthsApi } from '$lib/api/client';

export const prerender = false;

export const load: PageLoad = async ({ fetch }) => {
	const [trends, months] = await Promise.all([
		createSummaryApi(fetch).trends(),
		createMonthsApi(fetch).list()
	]);
	return { trends: trends.months, months };
};
