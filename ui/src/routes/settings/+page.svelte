<script lang="ts">
	import { settingsApi } from '$lib/api/client';
	import { uiStore } from '$lib/stores/ui.svelte';
	import { formatEur } from '$lib/utils/format';
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
</div>
