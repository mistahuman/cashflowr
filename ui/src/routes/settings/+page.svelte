<script lang="ts">
	import { settingsApi, monthsApi } from '$lib/api/client';
	import type { MonthEntry, ImportResult } from '$lib/api/client';
	import { uiStore } from '$lib/stores/ui.svelte';
	import { formatEur } from '$lib/utils/format';
	import { invalidateAll } from '$app/navigation';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let initialNetWorth  = $state(data.settings.initial_net_worth.toString());
	let lifeTarget       = $state(data.settings.life_target.toString());
	let investmentTarget = $state(data.settings.investment_target.toString());
	let taxRate          = $state(data.settings.tax_rate.toString());
	let loading = $state(false);
	let error   = $state<string | null>(null);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = null;
		loading = true;
		try {
			await settingsApi.update({
				initial_net_worth: parseFloat(initialNetWorth)  || 0,
				life_target:       parseFloat(lifeTarget)       || 0,
				investment_target: parseFloat(investmentTarget) || 0,
				tax_rate:          parseFloat(taxRate)          || 0,
			});
			uiStore.toast('Settings saved!', 'success');
		} catch (err: unknown) {
			error = err instanceof Error ? err.message : 'An error occurred.';
		} finally {
			loading = false;
		}
	}

	// — Data management —
	function exportCsv(months: MonthEntry[]) {
		const headers = [
			'Year', 'Month', 'Income', 'Expenses', 'Investments',
			'Portfolio Value', 'Savings', 'Liquid Balance', 'Net Worth', 'Net Worth Delta',
			'Savings Rate %', 'Investment Rate %', 'Wealth-Building Rate %',
			'Rolling Avg 3m Income', 'Notes'
		];
		const rows = [...months].reverse().map((m) => [
			m.year, m.month, m.income, m.expenses, m.investments,
			m.portfolio_value ?? '',
			m.savings, m.liquid_balance, m.net_worth, m.net_worth_delta,
			m.savings_rate ?? '', m.investment_rate ?? '', m.wealth_building_rate ?? '',
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

	let importFiles  = $state<FileList | undefined>(undefined);
	let importing    = $state(false);
	let importResult = $state<ImportResult | null>(null);
	let importError  = $state<string | null>(null);
	let applyingInw  = $state(false);

	async function handleImport() {
		const file = importFiles?.[0];
		if (!file) return;
		importing = true;
		importResult = null;
		importError = null;
		try {
			const result = await monthsApi.importCsv(file, 'upsert');
			importResult = result;
			await invalidateAll();
			uiStore.toast(
				`Imported ${result.imported}, updated ${result.updated}${result.skipped ? `, skipped ${result.skipped}` : ''}.`,
				result.errors.length ? 'info' : 'success'
			);
		} catch (err: unknown) {
			importError = err instanceof Error ? err.message : 'Import failed.';
		} finally {
			importing = false;
			importFiles = undefined;
		}
	}

	async function applyDerivedInw(value: number) {
		applyingInw = true;
		try {
			await settingsApi.update({
				initial_net_worth: value,
				life_target:       parseFloat(lifeTarget)       || 0,
				investment_target: parseFloat(investmentTarget) || 0,
				tax_rate:          parseFloat(taxRate)          || 0,
			});
			initialNetWorth = value.toString();
			await invalidateAll();
			uiStore.toast('Initial net worth updated.', 'success');
			if (importResult) importResult = { ...importResult, derived_initial_net_worth: null };
		} catch (err: unknown) {
			uiStore.toast(err instanceof Error ? err.message : 'Failed to update.', 'error');
		} finally {
			applyingInw = false;
		}
	}
</script>

<div class="container mx-auto max-w-screen-sm px-4 py-8 space-y-8">
	<div class="space-y-1">
		<h1 class="h2 font-bold">Settings</h1>
		<p class="text-surface-500 text-sm">Global configuration for your account.</p>
	</div>

	<form onsubmit={handleSubmit} class="space-y-6">

		<!-- Net worth -->
		<div class="card p-6 space-y-4">
			<div class="space-y-1">
				<h2 class="font-semibold">Initial net worth</h2>
				<p class="text-surface-500 text-sm">Your net worth before the first tracked month.</p>
			</div>
			<label class="label">
				<span class="label-text">Amount (€)</span>
				<input type="number" class="input" bind:value={initialNetWorth} step="0.01" placeholder="0.00" />
			</label>
		</div>

		<!-- Planner targets -->
		<div class="card p-6 space-y-4">
			<div class="space-y-1">
				<h2 class="font-semibold">Monthly allocation targets</h2>
				<p class="text-surface-500 text-sm">Used by the Planner to simulate how your income should be split each month.</p>
			</div>

			<label class="label">
				<span class="label-text">Tax rate <span class="text-surface-400 text-xs">— % applied to gross income (e.g. 15 for forfettario)</span></span>
				<div class="input-group grid-cols-[1fr_auto]">
					<input type="number" class="input" bind:value={taxRate} min="0" max="100" step="0.1" placeholder="0.0" />
					<span class="input-group-cell flex items-center px-3 text-surface-500">%</span>
				</div>
			</label>

			<label class="label">
				<span class="label-text">Life <span class="text-surface-400 text-xs">— fixed monthly amount for living expenses</span></span>
				<input type="number" class="input" bind:value={lifeTarget} min="0" step="0.01" placeholder="0.00" />
			</label>

			<label class="label">
				<span class="label-text">Investments <span class="text-surface-400 text-xs">— fixed monthly amount to invest</span></span>
				<input type="number" class="input" bind:value={investmentTarget} min="0" step="0.01" placeholder="0.00" />
			</label>

			<div class="card preset-tonal p-3 space-y-1 text-sm">
				<div class="flex justify-between">
					<span class="text-surface-500">Taxes on {parseFloat(lifeTarget) || 0 > 0 ? 'avg income' : 'income'}</span>
					<span class="font-mono">{parseFloat(taxRate) || 0}%</span>
				</div>
				<div class="flex justify-between">
					<span class="text-surface-500">Life (fixed)</span>
					<span class="font-mono">{formatEur(parseFloat(lifeTarget) || 0)}</span>
				</div>
				<div class="flex justify-between">
					<span class="text-surface-500">Investments (fixed)</span>
					<span class="font-mono">{formatEur(parseFloat(investmentTarget) || 0)}</span>
				</div>
			</div>
		</div>

		{#if error}
			<p class="text-error-600 text-sm">{error}</p>
		{/if}

		<button type="submit" class="btn preset-filled-primary-500 w-full" disabled={loading}>
			{loading ? 'Saving…' : 'Save settings'}
		</button>
	</form>

	<!-- Data management -->
	<div class="card p-6 space-y-6">
		<div class="space-y-1">
			<h2 class="font-semibold">Data</h2>
			<p class="text-surface-500 text-sm">Export or import your financial data as CSV.</p>
		</div>

		<!-- Export -->
		<div class="space-y-2">
			<p class="text-sm font-medium">Export</p>
			<button
				class="btn preset-tonal text-sm"
				onclick={() => exportCsv(data.months)}
				disabled={data.months.length === 0}
			>
				Export CSV
			</button>
		</div>

		<hr class="hr" />

		<!-- Import -->
		<div class="space-y-3">
			<p class="text-sm font-medium">Import</p>

			<aside class="card preset-tonal-warning-500 p-4 space-y-1 text-sm">
				<p class="font-semibold">Destructive operation</p>
				<p>
					Importing will overwrite existing entries for matching months. This cannot be undone.
					Export a backup first.
				</p>
			</aside>

			<div class="flex flex-wrap gap-3 items-center">
				<input
					type="file"
					accept=".csv"
					class="input text-sm max-w-xs"
					onchange={(e) => { importFiles = (e.currentTarget as HTMLInputElement).files ?? undefined; importResult = null; importError = null; }}
				/>
				<button
					class="btn preset-filled-warning-500 text-sm"
					onclick={handleImport}
					disabled={!importFiles?.length || importing}
				>
					{importing ? 'Importing…' : 'Import CSV'}
				</button>
			</div>

			{#if importResult}
				<div class="card preset-tonal p-4 text-sm space-y-3">
					<p class="font-semibold">Import result</p>
					<p>New: <span class="font-mono">{importResult.imported}</span> &nbsp;|&nbsp; Updated: <span class="font-mono">{importResult.updated}</span> &nbsp;|&nbsp; Skipped: <span class="font-mono">{importResult.skipped}</span></p>
					{#if importResult.errors.length}
						<details>
							<summary class="cursor-pointer text-error-600">{importResult.errors.length} error{importResult.errors.length === 1 ? '' : 's'}</summary>
							<ul class="mt-1 space-y-1 text-error-600 font-mono text-xs">
								{#each importResult.errors as e}
									<li>{e}</li>
								{/each}
							</ul>
						</details>
					{/if}
					{#if importResult.derived_initial_net_worth !== null}
						<aside class="card preset-tonal-secondary-500 p-3 space-y-2">
							<p class="font-semibold">Suggested initial net worth</p>
							<p>
								Derived from the earliest month in the CSV:
								<span class="font-mono font-semibold">{formatEur(importResult.derived_initial_net_worth)}</span>
								<span class="text-surface-500">(current: {formatEur(parseFloat(initialNetWorth) || 0)})</span>
							</p>
							<button
								class="btn preset-tonal-secondary-500 btn-sm text-sm"
								onclick={() => applyDerivedInw(importResult!.derived_initial_net_worth!)}
								disabled={applyingInw}
							>
								{applyingInw ? 'Applying…' : 'Apply'}
							</button>
						</aside>
					{/if}
				</div>
			{/if}

			{#if importError}
				<p class="text-error-600 text-sm">{importError}</p>
			{/if}
		</div>
	</div>

</div>
