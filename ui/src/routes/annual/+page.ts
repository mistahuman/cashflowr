import type { PageLoad } from './$types';
import { createSummaryApi, createMonthsApi } from '$lib/api/client';

export const prerender = false;

export const load: PageLoad = async ({ url, fetch }) => {
	const year = parseInt(url.searchParams.get('year') ?? String(new Date().getFullYear()));
	const [summary, months] = await Promise.all([
		createSummaryApi(fetch).annual(year),
		createMonthsApi(fetch).list()
	]);
	const availableYears = [...new Set(months.map((m) => m.year))].sort((a, b) => b - a);
	return { summary, year, availableYears };
};
