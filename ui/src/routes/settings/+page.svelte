<script lang="ts">
	import { settingsApi } from '$lib/api/client';
	import { uiStore } from '$lib/stores/ui.svelte';
	import { formatEur } from '$lib/utils/format';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let initialNetWorth = $state(data.settings.initial_net_worth.toString());
	let loading = $state(false);
	let error = $state<string | null>(null);

	const preview = $derived(parseFloat(initialNetWorth) || 0);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		const value = parseFloat(initialNetWorth);
		if (isNaN(value)) { error = 'Enter a valid number.'; return; }
		error = null;
		loading = true;
		try {
			await settingsApi.update({ initial_net_worth: value });
			uiStore.toast('Settings saved!', 'success');
		} catch (err: unknown) {
			error = err instanceof Error ? err.message : 'An error occurred.';
		} finally {
			loading = false;
		}
	}
</script>

<div class="container mx-auto max-w-screen-sm px-4 py-8 space-y-6">
	<div class="space-y-1">
		<h1 class="h2 font-bold">Settings</h1>
		<p class="text-surface-500 text-sm">Global configuration for your account.</p>
	</div>

	<div class="card p-6 space-y-6">
		<div class="space-y-1">
			<h2 class="font-semibold">Initial net worth</h2>
			<p class="text-surface-500 text-sm">
				Your net worth before the first month you tracked. This is the baseline from which all calculations start.
			</p>
		</div>

		<form onsubmit={handleSubmit} class="space-y-4">
			<label class="label">
				<span class="label-text">Amount (€)</span>
				<input
					type="number"
					class="input"
					bind:value={initialNetWorth}
					step="0.01"
					placeholder="0.00"
					required
				/>
			</label>

			<div class="card preset-tonal p-4">
				<div class="flex justify-between text-sm">
					<span class="text-surface-600 dark:text-surface-400">Starting net worth</span>
					<span class="font-mono font-bold">{formatEur(preview)}</span>
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
</div>
