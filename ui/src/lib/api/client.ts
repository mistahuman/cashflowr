const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

export interface MonthEntry {
	id: string;
	year: number;
	month: number;
	income: number;
	expenses: number;
	investments: number;
	initial_net_worth: number | null;
	savings: number;
	net_worth: number;
	net_worth_delta: number;
	savings_rate: number | null;
	investment_rate: number | null;
	wealth_building_rate: number | null;
	consistency_check: number;
	rolling_avg_3m: number;
}

export interface MonthCreate {
	year: number;
	month: number;
	income: number;
	expenses: number;
	investments: number;
	initial_net_worth?: number | null;
}

export interface MonthUpdate {
	income?: number;
	expenses?: number;
	investments?: number;
	initial_net_worth?: number | null;
}

export interface AnnualSummary {
	year: number;
	total_income: number;
	total_expenses: number;
	total_investments: number;
	total_savings: number;
	avg_savings_rate: number | null;
	best_month: MonthEntry | null;
	worst_month: MonthEntry | null;
}

export interface TrendsResponse {
	months: MonthEntry[];
}

type FetchFn = typeof fetch;

async function request<T>(path: string, init?: RequestInit, fetchFn: FetchFn = fetch): Promise<T> {
	const res = await fetchFn(`${BASE_URL}${path}`, {
		headers: { 'Content-Type': 'application/json', ...init?.headers },
		...init
	});
	if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
	if (res.status === 204) return undefined as T;
	return res.json();
}

export function createMonthsApi(fetchFn?: FetchFn) {
	return {
		list: () => request<MonthEntry[]>('/months/', undefined, fetchFn),
		get: (year: number, month: number) =>
			request<MonthEntry>(`/months/${year}/${month}`, undefined, fetchFn),
		create: (payload: MonthCreate) =>
			request<MonthEntry>('/months/', { method: 'POST', body: JSON.stringify(payload) }, fetchFn),
		update: (year: number, month: number, payload: MonthUpdate) =>
			request<MonthEntry>(`/months/${year}/${month}`, {
				method: 'PUT',
				body: JSON.stringify(payload)
			}, fetchFn),
		delete: (year: number, month: number) =>
			request<void>(`/months/${year}/${month}`, { method: 'DELETE' }, fetchFn)
	};
}

export function createSummaryApi(fetchFn?: FetchFn) {
	return {
		annual: (year: number) =>
			request<AnnualSummary>(`/summary/annual/${year}`, undefined, fetchFn),
		trends: () => request<TrendsResponse>('/summary/trends', undefined, fetchFn)
	};
}

export const monthsApi = createMonthsApi();
export const summaryApi = createSummaryApi();
