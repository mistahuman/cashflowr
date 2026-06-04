<script lang="ts">
	import { resolve } from '$app/paths';
	import { formatEur, formatRate, monthLabel } from '$lib/utils/format';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	const { settings, months } = $derived(data);
	const current  = $derived(months[0] ?? null);
	const allChron = $derived([...months].reverse());

	const isConfigured = $derived(
		settings.tax_rate > 0 || settings.life_target > 0 || settings.investment_target > 0
	);

	// Income to simulate — default to current month, user can override
	let incomeInput = $state('');
	const baseIncome = $derived(
		current?.income
		?? (allChron.length > 0 ? allChron.reduce((s, m) => s + m.income, 0) / allChron.length : 0)
	);
	const income = $derived(incomeInput !== '' ? (parseFloat(incomeInput) || 0) : baseIncome);

	// Core allocation
	const taxes      = $derived(income * settings.tax_rate / 100);
	const netIncome  = $derived(income - taxes);
	const life       = $derived(settings.life_target);
	const invest     = $derived(settings.investment_target);
	const buffer     = $derived(netIncome - life - invest);

	// All percentages relative to gross income → bar slices add up to 100%
	const taxPct    = $derived(income > 0 ? taxes              / income * 100 : 0);
	const lifePct   = $derived(income > 0 ? life               / income * 100 : 0);
	const investPct = $derived(income > 0 ? invest             / income * 100 : 0);
	const bufferPct = $derived(income > 0 ? Math.max(buffer, 0) / income * 100 : 0);
	// Rates vs net income (for insight cards)
	const lifeOfNet   = $derived(netIncome > 0 ? life   / netIncome * 100 : 0);
	const investOfNet = $derived(netIncome > 0 ? invest / netIncome * 100 : 0);
	const bufferOfNet = $derived(netIncome > 0 ? Math.max(buffer, 0) / netIncome * 100 : 0);

	// Historical averages
	const n = $derived(allChron.length);
	const avgIncome   = $derived(n > 0 ? allChron.reduce((s, m) => s + m.income,      0) / n : 0);
	const avgInvested = $derived(n > 0 ? allChron.reduce((s, m) => s + m.investments, 0) / n : 0);
	const avgIncomeDiff   = $derived(avgIncome  - baseIncome);
	const avgInvestedDiff = $derived(avgInvested - invest);

	// Suggestion: potential extra investment if buffer fully invested
	const potentialInvest = $derived(Math.max(buffer, 0) + invest);
	const potentialPct    = $derived(netIncome > 0 ? potentialInvest / netIncome * 100 : 0);
</script>

<div class="container mx-auto max-w-screen-md px-4 py-8 space-y-8">

	<div class="flex items-center justify-between flex-wrap gap-3">
		<div>
			<h1 class="h2 font-bold">Planner</h1>
			<p class="text-surface-500 text-sm">Monthly income allocation</p>
		</div>
		<a href={resolve('/settings')} class="btn preset-tonal text-sm">Edit targets</a>
	</div>

	{#if !isConfigured}
		<div class="card p-6 text-center space-y-3">
			<p class="text-surface-500">No allocation targets configured yet.</p>
			<a href={resolve('/settings')} class="btn preset-filled-primary-500">Go to Settings</a>
		</div>
	{:else}

		<!-- Income input -->
		<div class="card p-5 space-y-3">
			<p class="text-xs font-semibold uppercase tracking-widest text-surface-500">Income to simulate</p>
			<div class="flex items-center gap-3">
				<input
					type="number"
					class="input flex-1"
					bind:value={incomeInput}
					min="0"
					step="0.01"
					placeholder="{baseIncome.toFixed(2)} ({current ? monthLabel(current.year, current.month) : 'historical avg'})"
				/>
				{#if incomeInput !== ''}
					<button class="btn preset-tonal text-sm" onclick={() => incomeInput = ''}>Reset</button>
				{/if}
			</div>
		</div>

		<!-- Stacked allocation bar -->
		<div class="space-y-3">
			<p class="text-xs font-semibold uppercase tracking-widest text-surface-500">Allocation of {formatEur(income)}</p>

			<div class="h-7 rounded-lg overflow-hidden flex w-full gap-px">
				{#if taxPct > 0}
					<div class="h-full bg-error-400 dark:bg-error-600" style="width:{taxPct}%"></div>
				{/if}
				{#if lifePct > 0}
					<div class="h-full bg-primary-500" style="width:{lifePct}%"></div>
				{/if}
				{#if investPct > 0}
					<div class="h-full bg-success-500" style="width:{investPct}%"></div>
				{/if}
				{#if bufferPct > 0}
					<div class="h-full bg-surface-300 dark:bg-surface-600 flex-shrink-0" style="width:{bufferPct}%"></div>
				{/if}
				{#if buffer < 0}
					<div class="h-full bg-error-500 flex-1"></div>
				{/if}
			</div>

			<div class="grid grid-cols-2 gap-3 sm:grid-cols-4">
				<div class="card p-3 space-y-0.5 border-l-4 border-error-400">
					<p class="text-xs text-surface-500 uppercase tracking-widest">Taxes</p>
					<p class="font-mono font-bold">{formatEur(taxes)}</p>
					<p class="text-xs text-surface-400">{settings.tax_rate}% of gross</p>
				</div>
				<div class="card p-3 space-y-0.5 border-l-4 border-primary-500">
					<p class="text-xs text-surface-500 uppercase tracking-widest">Life</p>
					<p class="font-mono font-bold">{formatEur(life)}</p>
					<p class="text-xs text-surface-400">{lifePct.toFixed(1)}% gross · {lifeOfNet.toFixed(1)}% net</p>
				</div>
				<div class="card p-3 space-y-0.5 border-l-4 border-success-500">
					<p class="text-xs text-surface-500 uppercase tracking-widest">Investments</p>
					<p class="font-mono font-bold">{formatEur(invest)}</p>
					<p class="text-xs text-surface-400">{investPct.toFixed(1)}% gross · {investOfNet.toFixed(1)}% net</p>
				</div>
				<div class="card p-3 space-y-0.5 border-l-4 {buffer >= 0 ? 'border-surface-400' : 'border-error-500'}">
					<p class="text-xs text-surface-500 uppercase tracking-widest">Buffer</p>
					<p class="font-mono font-bold {buffer < 0 ? 'text-error-600 dark:text-error-400' : ''}">{formatEur(buffer)}</p>
					<p class="text-xs text-surface-400">{buffer >= 0 ? `${bufferPct.toFixed(1)}% gross · ${bufferOfNet.toFixed(1)}% net` : 'deficit'}</p>
				</div>
			</div>

			{#if buffer < 0}
				<p class="text-sm text-error-600 dark:text-error-400">
					Targets exceed net income by <span class="font-mono font-bold">{formatEur(Math.abs(buffer))}</span>. Reduce Life or Investments in Settings.
				</p>
			{/if}
		</div>

		<hr class="border-surface-200/70 dark:border-surface-700/70" />

		<!-- Insights -->
		<div class="space-y-4">
			<div class="flex items-center gap-3">
				<span class="w-1 h-5 rounded-full bg-success-500"></span>
				<h2 class="font-semibold">Insights</h2>
			</div>

			<div class="grid grid-cols-1 gap-3 sm:grid-cols-2">

				<!-- Net income -->
				<div class="card p-4 space-y-1">
					<p class="text-xs text-surface-500 uppercase tracking-widest">Net income after taxes</p>
					<p class="font-mono font-bold text-xl">{formatEur(netIncome)}</p>
					<p class="text-xs text-surface-400">
						{formatEur(income)} gross − {formatEur(taxes)} taxes ({settings.tax_rate}%)
					</p>
				</div>

				<!-- Investment rate -->
				<div class="card p-4 space-y-1">
					<p class="text-xs text-surface-500 uppercase tracking-widest">Investment rate</p>
					<p class="font-mono font-bold text-xl">{formatRate(investOfNet)}</p>
					<p class="text-xs text-surface-400">of net income · {formatEur(invest)}/mo</p>
				</div>

				<!-- If buffer fully invested -->
				{#if buffer > 0}
					<div class="card p-4 space-y-1 col-span-full border border-success-400/30">
						<p class="text-xs text-surface-500 uppercase tracking-widest">If buffer fully invested</p>
						<p class="font-mono font-bold text-xl text-success-600 dark:text-success-400">
							{formatRate(potentialPct)} of net income
						</p>
						<p class="text-xs text-surface-400">
							{formatEur(potentialInvest)}/mo — {formatEur(buffer)} extra on top of current target
						</p>
					</div>
				{/if}

			</div>
		</div>

		<!-- Historical comparison (only if data exists) -->
		{#if n > 0}
			<hr class="border-surface-200/70 dark:border-surface-700/70" />

			<div class="space-y-4">
				<div class="flex items-center gap-3">
					<span class="w-1 h-5 rounded-full bg-tertiary-500"></span>
					<h2 class="font-semibold">
						Historical averages
						<span class="text-surface-400 font-normal text-sm ml-1">{n} months</span>
					</h2>
				</div>

				<div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
					<div class="card p-4 space-y-1">
						<p class="text-xs text-surface-500 uppercase tracking-widest">Avg monthly income</p>
						<p class="font-mono font-bold text-xl">{formatEur(avgIncome)}</p>
						<p class="text-xs {avgIncomeDiff >= 0 ? 'text-success-500' : 'text-error-500'}">
							{avgIncomeDiff >= 0 ? '+' : ''}{formatEur(avgIncomeDiff)} vs simulated income
						</p>
					</div>

					<div class="card p-4 space-y-1">
						<p class="text-xs text-surface-500 uppercase tracking-widest">Avg monthly invested</p>
						<p class="font-mono font-bold text-xl">{formatEur(avgInvested)}</p>
						<p class="text-xs {avgInvestedDiff >= 0 ? 'text-success-500' : 'text-error-500'}">
							{avgInvestedDiff >= 0 ? '+' : ''}{formatEur(avgInvestedDiff)} vs target
						</p>
					</div>
				</div>
			</div>
		{/if}

	{/if}
</div>
