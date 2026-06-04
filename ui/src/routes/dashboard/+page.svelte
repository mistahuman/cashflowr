<script lang="ts">
	import type { PageData } from './$types';
	import KpiCard from '$lib/components/cashflowr/KpiCard.svelte';
	import NetWorthChart from '$lib/components/cashflowr/NetWorthChart.svelte';
	import IncomeExpensesChart from '$lib/components/cashflowr/IncomeExpensesChart.svelte';
	import SavingsChart from '$lib/components/cashflowr/SavingsChart.svelte';
	import SavingsRateChart from '$lib/components/cashflowr/SavingsRateChart.svelte';
	import { formatEur, formatRate, monthLabel } from '$lib/utils/format';
	import { resolve } from '$app/paths';

	let { data }: { data: PageData } = $props();

	const current = $derived(data.months[0] ?? null);
	// data.months is most-recent-first; charts need chronological order
	const allChron = $derived([...data.months].reverse());

	const hasPortfolio = $derived(current ? current.portfolio_value_effective > 0 : false);

	// Global bounds across entire history
	const nwMin = $derived(
		allChron.length > 0
			? Math.floor(Math.min(...allChron.map((m) => m.net_worth)) * 0.97)
			: 0
	);
	const nwMax = $derived(
		allChron.length > 0
			? Math.ceil(Math.max(...allChron.map((m) => m.net_worth)) * 1.03)
			: undefined
	);
	const ieMax = $derived(
		allChron.length > 0
			? Math.ceil(Math.max(...allChron.map((m) => Math.max(m.income, m.expenses))) * 1.1)
			: undefined
	);
</script>

<div class="container mx-auto max-w-screen-xl px-4 py-8 space-y-8">
	<div class="flex items-center justify-between">
		<h1 class="h2 font-bold">Dashboard</h1>
		<a href={resolve('/entry')} class="btn preset-filled-primary-500 text-sm">+ Add month</a>
	</div>

	{#if current}
		<section class="space-y-3">
			<h2 class="text-xs font-semibold uppercase tracking-widest text-surface-500">
				{monthLabel(current.year, current.month)} — current month
			</h2>
			<div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
				<KpiCard label="Income" value={formatEur(current.income)} />
				<KpiCard label="Expenses" value={formatEur(current.expenses)} />
				<KpiCard
					label="Savings"
					value={formatEur(current.savings)}
					highlight={current.savings >= 0 ? 'positive' : 'negative'}
				/>
				<KpiCard label="Net worth" value={formatEur(current.net_worth)} />
			</div>

			{#if hasPortfolio}
				<div class="grid grid-cols-2 gap-4">
					<KpiCard label="Liquid cash" value={formatEur(current.liquid_balance)} sub="Cash savings" />
					<KpiCard label="Portfolio" value={formatEur(current.portfolio_value_effective)} sub="Investment portfolio value" />
				</div>
			{/if}

			<div class="grid grid-cols-2 gap-4 sm:grid-cols-3">
				<KpiCard
					label="Savings rate"
					value={formatRate(current.savings_rate)}
					highlight={current.savings_rate != null && current.savings_rate >= 0 ? 'positive' : 'neutral'}
				/>
				<KpiCard label="Investment rate" value={formatRate(current.investment_rate)} />
				<KpiCard label="Wealth-building rate" value={formatRate(current.wealth_building_rate)} />
			</div>

			{#if current.notes}
				<div class="card preset-tonal p-4 text-sm text-surface-600 dark:text-surface-400 italic">
					{current.notes}
				</div>
			{/if}
		</section>
	{:else}
		<div class="card p-8 text-center space-y-3">
			<p class="text-surface-500">No data yet.</p>
			<a href={resolve('/entry')} class="btn preset-filled-primary-500">Add your first month</a>
		</div>
	{/if}

	{#if allChron.length > 0}
		<section class="space-y-3">
			<h2 class="text-xs font-semibold uppercase tracking-widest text-surface-500">
				Net worth — all time
			</h2>
			<div class="card p-4">
				<NetWorthChart months={allChron} yMin={nwMin} yMax={nwMax} />
			</div>
		</section>

		<section class="space-y-3">
			<h2 class="text-xs font-semibold uppercase tracking-widest text-surface-500">
				Income vs expenses — all time
			</h2>
			<div class="card p-4">
				<IncomeExpensesChart months={allChron} yMin={0} yMax={ieMax} />
			</div>
		</section>

		<section class="space-y-3">
			<h2 class="text-xs font-semibold uppercase tracking-widest text-surface-500">
				Savings & investments — all time
			</h2>
			<div class="card p-4">
				<SavingsChart months={allChron} />
			</div>
		</section>

		<section class="space-y-3">
			<h2 class="text-xs font-semibold uppercase tracking-widest text-surface-500">
				Savings rate — all time
			</h2>
			<div class="card p-4">
				<SavingsRateChart months={allChron} />
			</div>
		</section>
	{/if}
</div>
