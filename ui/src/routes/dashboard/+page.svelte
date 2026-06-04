<script lang="ts">
	import type { PageData } from './$types';
	import KpiCard from '$lib/components/cashflowr/KpiCard.svelte';
	import NetWorthChart from '$lib/components/cashflowr/NetWorthChart.svelte';
	import NetWorthDeltaChart from '$lib/components/cashflowr/NetWorthDeltaChart.svelte';
	import NetWorthCompositionChart from '$lib/components/cashflowr/NetWorthCompositionChart.svelte';
	import IncomeExpensesChart from '$lib/components/cashflowr/IncomeExpensesChart.svelte';
	import SavingsRateChart from '$lib/components/cashflowr/SavingsRateChart.svelte';
	import ExpenseRatioChart from '$lib/components/cashflowr/ExpenseRatioChart.svelte';
	import { formatEur, formatDeltaEur, formatRate, monthLabel } from '$lib/utils/format';
	import { resolve } from '$app/paths';

	let { data }: { data: PageData } = $props();

	const current  = $derived(data.months[0] ?? null);
	const prev     = $derived(data.months[1] ?? null);
	const allChron = $derived([...data.months].reverse());

	// ── Deltas ───────────────────────────────────────────────────────────────
	const prevLabel = $derived(prev ? `vs ${monthLabel(prev.year, prev.month)}` : null);
	const dIncome   = $derived(current && prev ? current.income    - prev.income    : null);
	const dExpenses = $derived(current && prev ? current.expenses  - prev.expenses  : null);
	const dSavings  = $derived(current && prev ? current.savings   - prev.savings   : null);
	const dNetWorth = $derived(current && prev ? current.net_worth - prev.net_worth : null);

	// ── YTD ──────────────────────────────────────────────────────────────────
	const ytdMonths   = $derived(current ? allChron.filter((m) => m.year === current.year) : []);
	const ytdIncome   = $derived(ytdMonths.reduce((s, m) => s + m.income,   0));
	const ytdExpenses = $derived(ytdMonths.reduce((s, m) => s + m.expenses, 0));
	const ytdSavings  = $derived(ytdMonths.reduce((s, m) => s + m.savings,  0));
	const ytdRates    = $derived(ytdMonths.map((m) => m.savings_rate).filter((r): r is number => r != null));
	const ytdAvgRate  = $derived(ytdRates.length > 0 ? ytdRates.reduce((s, r) => s + r, 0) / ytdRates.length : null);

	// ── Historical ───────────────────────────────────────────────────────────
	const n           = $derived(allChron.length);
	const avgIncome   = $derived(n > 0 ? allChron.reduce((s, m) => s + m.income,   0) / n : 0);
	const avgExpenses = $derived(n > 0 ? allChron.reduce((s, m) => s + m.expenses, 0) / n : 0);
	const avgSavings  = $derived(n > 0 ? allChron.reduce((s, m) => s + m.savings,  0) / n : 0);
	const avgNwDelta  = $derived(n > 0 ? allChron.reduce((s, m) => s + m.net_worth_delta, 0) / n : 0);
	const allRates    = $derived(allChron.map((m) => m.savings_rate).filter((r): r is number => r != null));
	const avgRate     = $derived(allRates.length > 0 ? allRates.reduce((s, r) => s + r, 0) / allRates.length : null);
	const runway      = $derived(current && avgExpenses > 0 ? current.liquid_balance / avgExpenses : null);

	// ── Streak ───────────────────────────────────────────────────────────────
	const streak = $derived(() => {
		let count = 0;
		for (const m of data.months) { if (m.savings >= 0) count++; else break; }
		return count;
	});
	const streakLabel = $derived(
		streak() === 0 ? 'No current streak'
		: streak() === 1 ? '1 month in a row'
		: `${streak()} months in a row`
	);

	// ── Chart bounds ─────────────────────────────────────────────────────────
	const hasPortfolio = $derived(allChron.some((m) => m.portfolio_value_effective > 0));
	const nwMin = $derived(n > 0 ? Math.floor(Math.min(...allChron.map((m) => m.net_worth)) * 0.97) : 0);
	const nwMax = $derived(n > 0 ? Math.ceil( Math.max(...allChron.map((m) => m.net_worth)) * 1.03) : undefined);
	const ieMax = $derived(n > 0 ? Math.ceil( Math.max(...allChron.map((m) => Math.max(m.income, m.expenses))) * 1.1) : undefined);
</script>

<div class="container mx-auto max-w-screen-xl px-4 py-8 space-y-10">

	<!-- Header -->
	<div class="flex items-center justify-between">
		<h1 class="h2 font-bold">Dashboard</h1>
		<a href={resolve('/entry')} class="btn preset-filled-primary-500 text-sm">+ Add month</a>
	</div>

	{#if !current}
		<div class="card p-8 text-center space-y-3">
			<p class="text-surface-500">No data yet.</p>
			<a href={resolve('/entry')} class="btn preset-filled-primary-500">Add your first month</a>
		</div>
	{:else}

		<!-- ── Current month ──────────────────────────────────────────────────── -->
		<section class="space-y-4">
			<div class="flex items-center gap-3">
				<span class="w-1 h-5 rounded-full bg-primary-500"></span>
				<h2 class="font-semibold text-surface-900 dark:text-surface-50">
					{monthLabel(current.year, current.month)}
					<span class="text-surface-400 font-normal text-sm ml-1">current month</span>
				</h2>
			</div>

			<div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
				<KpiCard label="Income"    value={formatEur(current.income)}
					delta={dIncome   != null ? `${formatDeltaEur(dIncome)}   ${prevLabel}` : undefined}
					deltaPositive={dIncome   != null ? dIncome   >= 0 : null} />
				<KpiCard label="Expenses"  value={formatEur(current.expenses)}
					delta={dExpenses != null ? `${formatDeltaEur(dExpenses)} ${prevLabel}` : undefined}
					deltaPositive={dExpenses != null ? dExpenses <= 0 : null} />
				<KpiCard label="Savings"   value={formatEur(current.savings)}
					highlight={current.savings >= 0 ? 'positive' : 'negative'}
					delta={dSavings  != null ? `${formatDeltaEur(dSavings)}  ${prevLabel}` : undefined}
					deltaPositive={dSavings  != null ? dSavings  >= 0 : null} />
				<KpiCard label="Net worth" value={formatEur(current.net_worth)}
					delta={dNetWorth != null ? `${formatDeltaEur(dNetWorth)} ${prevLabel}` : undefined}
					deltaPositive={dNetWorth != null ? dNetWorth >= 0 : null} />
			</div>

			{#if hasPortfolio}
				<div class="grid grid-cols-2 gap-4">
					<KpiCard label="Liquid cash" value={formatEur(current.liquid_balance)}          sub="Cash savings" />
					<KpiCard label="Portfolio"   value={formatEur(current.portfolio_value_effective)} sub="Investment portfolio value" />
				</div>
			{/if}

			<div class="grid grid-cols-2 gap-4 sm:grid-cols-3">
				<KpiCard label="Savings rate"         value={formatRate(current.savings_rate)}
					highlight={current.savings_rate != null && current.savings_rate >= 0 ? 'positive' : 'neutral'}
					sub={avgRate != null ? `ø ${formatRate(avgRate)} historical avg` : undefined} />
				<KpiCard label="Investment rate"       value={formatRate(current.investment_rate)} />
				<KpiCard label="Wealth-building rate"  value={formatRate(current.wealth_building_rate)} />
			</div>

			{#if current.notes}
				<div class="card preset-tonal p-4 text-sm text-surface-600 dark:text-surface-400 italic">
					{current.notes}
				</div>
			{/if}
		</section>

		<hr class="border-surface-200/70 dark:border-surface-700/70" />

		<!-- ── Year-to-date ───────────────────────────────────────────────────── -->
		{#if ytdMonths.length > 0}
			<section class="space-y-4">
				<div class="flex items-center gap-3">
					<span class="w-1 h-5 rounded-full bg-secondary-500"></span>
					<h2 class="font-semibold text-surface-900 dark:text-surface-50">
						{current.year} year-to-date
						<span class="text-surface-400 font-normal text-sm ml-1">{ytdMonths.length} {ytdMonths.length === 1 ? 'month' : 'months'}</span>
					</h2>
				</div>
				<div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
					<KpiCard label="YTD income"           value={formatEur(ytdIncome)} />
					<KpiCard label="YTD expenses"         value={formatEur(ytdExpenses)} />
					<KpiCard label="YTD savings"          value={formatEur(ytdSavings)}
						highlight={ytdSavings >= 0 ? 'positive' : 'negative'} />
					<KpiCard label="YTD avg savings rate" value={formatRate(ytdAvgRate)}
						highlight={ytdAvgRate != null && ytdAvgRate >= 0 ? 'positive' : 'neutral'} />
				</div>
			</section>

			<hr class="border-surface-200/70 dark:border-surface-700/70" />
		{/if}

		<!-- ── Historical averages ────────────────────────────────────────────── -->
		{#if n > 1}
			<section class="space-y-4">
				<div class="flex items-center gap-3">
					<span class="w-1 h-5 rounded-full bg-tertiary-500"></span>
					<h2 class="font-semibold text-surface-900 dark:text-surface-50">
						Historical averages
						<span class="text-surface-400 font-normal text-sm ml-1">{n} months</span>
					</h2>
				</div>
				<div class="grid grid-cols-2 gap-4 sm:grid-cols-3">
					<KpiCard label="Avg monthly income"    value={formatEur(avgIncome)} />
					<KpiCard label="Avg monthly expenses"  value={formatEur(avgExpenses)} />
					<KpiCard label="Avg monthly savings"   value={formatEur(avgSavings)}
						highlight={avgSavings >= 0 ? 'positive' : 'negative'} />
					<KpiCard label="Avg net worth growth"  value={formatEur(avgNwDelta)}
						highlight={avgNwDelta >= 0 ? 'positive' : 'negative'}
						sub="Monthly net worth change" />
					<KpiCard label="Expense runway"
						value={runway != null ? `${runway.toFixed(1)} mo` : '—'}
						sub="Months covered by liquid savings"
						highlight={runway != null && runway >= 6 ? 'positive' : runway != null && runway >= 3 ? 'neutral' : 'negative'} />
					<KpiCard label="Positive savings streak" value={streak().toString()}
						sub={streakLabel}
						highlight={streak() >= 3 ? 'positive' : streak() > 0 ? 'neutral' : 'negative'} />
				</div>
			</section>

			<hr class="border-surface-200/70 dark:border-surface-700/70" />
		{/if}

		<!-- ── Charts ────────────────────────────────────────────────────────── -->
		{#if n > 0}
			<section class="space-y-4">
				<div class="flex items-center gap-3">
					<span class="w-1 h-5 rounded-full bg-success-500"></span>
					<h2 class="font-semibold text-surface-900 dark:text-surface-50">Charts</h2>
				</div>

				<div class="space-y-6">
					<div class="space-y-2">
						<p class="text-xs font-medium uppercase tracking-widest text-surface-500">Net worth — all time</p>
						<div class="card p-4"><NetWorthChart months={allChron} yMin={nwMin} yMax={nwMax} /></div>
					</div>

					<div class="space-y-2">
						<p class="text-xs font-medium uppercase tracking-widest text-surface-500">Net worth monthly change — all time</p>
						<div class="card p-4"><NetWorthDeltaChart months={allChron} /></div>
					</div>

					{#if hasPortfolio}
						<div class="space-y-2">
							<p class="text-xs font-medium uppercase tracking-widest text-surface-500">Net worth composition — liquid vs portfolio</p>
							<div class="card p-4"><NetWorthCompositionChart months={allChron} /></div>
						</div>
					{/if}

					<div class="space-y-2">
						<p class="text-xs font-medium uppercase tracking-widest text-surface-500">Income vs expenses — all time</p>
						<div class="card p-4"><IncomeExpensesChart months={allChron} yMin={0} yMax={ieMax} /></div>
					</div>

					<div class="space-y-2">
						<p class="text-xs font-medium uppercase tracking-widest text-surface-500">Expense ratio — all time</p>
						<div class="card p-4"><ExpenseRatioChart months={allChron} /></div>
					</div>

					<div class="space-y-2">
						<p class="text-xs font-medium uppercase tracking-widest text-surface-500">Savings rate — all time</p>
						<div class="card p-4"><SavingsRateChart months={allChron} /></div>
					</div>
				</div>
			</section>
		{/if}

	{/if}
</div>
