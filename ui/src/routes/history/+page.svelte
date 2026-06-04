<script lang="ts">
	import type { PageData } from './$types';
	import type { MonthEntry } from '$lib/api/client';
	import HistoryTable from '$lib/components/cashflowr/HistoryTable.svelte';
	import { resolve } from '$app/paths';

	let { data }: { data: PageData } = $props();

	function exportCsv(months: MonthEntry[]) {
		const headers = [
			'Year', 'Month', 'Income', 'Expenses', 'Investments',
			'Portfolio Value', 'Savings', 'Liquid Balance', 'Net Worth', 'Net Worth Delta',
			'Savings Rate %', 'Investment Rate %', 'Wealth-Building Rate %',
			'Rolling Avg 3m Income', 'Notes'
		];

		const rows = [...months].reverse().map((m) => [
			m.year,
			m.month,
			m.income,
			m.expenses,
			m.investments,
			m.portfolio_value ?? '',
			m.savings,
			m.liquid_balance,
			m.net_worth,
			m.net_worth_delta,
			m.savings_rate ?? '',
			m.investment_rate ?? '',
			m.wealth_building_rate ?? '',
			m.rolling_avg_3m,
			m.notes ? `"${m.notes.replace(/"/g, '""')}"` : ''
		]);

		const csv = [headers, ...rows].map((r) => r.join(',')).join('\n');
		const blob = new Blob([csv], { type: 'text/csv' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `cashflowr-export-${new Date().toISOString().slice(0, 10)}.csv`;
		a.click();
		URL.revokeObjectURL(url);
	}
</script>

<div class="container mx-auto max-w-screen-xl px-4 py-8 space-y-6">
	<div class="flex items-center justify-between flex-wrap gap-3">
		<h1 class="h2 font-bold">History</h1>
		<div class="flex gap-2">
			<button
				class="btn preset-tonal text-sm"
				onclick={() => exportCsv(data.months)}
				disabled={data.months.length === 0}
			>
				Export CSV
			</button>
			<a href={resolve('/entry')} class="btn preset-filled-primary-500 text-sm">+ Add month</a>
		</div>
	</div>
	<div class="card p-4">
		<HistoryTable months={data.months} />
	</div>
</div>
