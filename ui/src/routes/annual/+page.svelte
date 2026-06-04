<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import type { PageData } from './$types';
	import KpiCard from '$lib/components/cashflowr/KpiCard.svelte';
	import NetWorthChart from '$lib/components/cashflowr/NetWorthChart.svelte';
	import IncomeExpensesChart from '$lib/components/cashflowr/IncomeExpensesChart.svelte';
	import { formatEur, formatRate, monthLabel } from '$lib/utils/format';

	let { data }: { data: PageData } = $props();
	const { summary, year, availableYears, yearMonths, allMonthsChron } = $derived(data);

	// Global bounds across ALL months so scale stays fixed when switching year
	const nwMin = $derived(
		allMonthsChron.length > 0
			? Math.floor(Math.min(...allMonthsChron.map((m) => m.net_worth)) * 0.97)
			: 0
	);
	const nwMax = $derived(
		allMonthsChron.length > 0
			? Math.ceil(Math.max(...allMonthsChron.map((m) => m.net_worth)) * 1.03)
			: undefined
	);
	const ieMax = $derived(
		allMonthsChron.length > 0
			? Math.ceil(Math.max(...allMonthsChron.map((m) => Math.max(m.income, m.expenses))) * 1.1)
			: undefined
	);

	function changeYear(y: number) {
		goto(`${resolve('/annual')}?year=${y}`);
	}
</script>

<div class="container mx-auto max-w-screen-lg px-4 py-8 space-y-8">
	<div class="flex items-center justify-between flex-wrap gap-4">
		<h1 class="h2 font-bold">Annual summary</h1>
		<div class="flex items-center gap-2">
			{#each availableYears as y (y)}
				<button
					class="btn text-sm {y === year ? 'preset-filled-primary-500' : 'preset-tonal'}"
					onclick={() => changeYear(y)}
				>
					{y}
				</button>
			{/each}
		</div>
	</div>

	<section class="space-y-3">
		<h2 class="text-xs font-semibold uppercase tracking-widest text-surface-500">{year} totals</h2>
		<div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
			<KpiCard label="Total income" value={formatEur(summary.total_income)} />
			<KpiCard label="Total expenses" value={formatEur(summary.total_expenses)} />
			<KpiCard label="Total investments" value={formatEur(summary.total_investments)} />
			<KpiCard
				label="Total savings"
				value={formatEur(summary.total_savings)}
				highlight={summary.total_savings >= 0 ? 'positive' : 'negative'}
			/>
		</div>
		<div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
			<KpiCard
				label="Avg savings rate"
				value={formatRate(summary.avg_savings_rate)}
				sub="Excludes zero-income months"
			/>
			{#if summary.best_month}
				<KpiCard
					label="Best month"
					value={monthLabel(summary.best_month.year, summary.best_month.month)}
					sub={`Savings: ${formatEur(summary.best_month.savings)}`}
					highlight="positive"
				/>
			{/if}
			{#if summary.worst_month}
				<KpiCard
					label="Worst month"
					value={monthLabel(summary.worst_month.year, summary.worst_month.month)}
					sub={`Savings: ${formatEur(summary.worst_month.savings)}`}
					highlight={summary.worst_month.savings < 0 ? 'negative' : 'neutral'}
				/>
			{/if}
		</div>
	</section>

	{#if yearMonths.length > 0}
		<section class="space-y-3">
			<h2 class="text-xs font-semibold uppercase tracking-widest text-surface-500">
				Net worth — {year}
			</h2>
			<div class="card p-4">
				<NetWorthChart months={yearMonths} yMin={nwMin} yMax={nwMax} />
			</div>
		</section>

		<section class="space-y-3">
			<h2 class="text-xs font-semibold uppercase tracking-widest text-surface-500">
				Income vs expenses — {year}
			</h2>
			<div class="card p-4">
				<IncomeExpensesChart months={yearMonths} yMin={0} yMax={ieMax} />
			</div>
		</section>
	{/if}
</div>
