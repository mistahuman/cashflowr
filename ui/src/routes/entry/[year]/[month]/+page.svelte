<script lang="ts">
	import { goto, invalidateAll } from '$app/navigation';
	import { resolve } from '$app/paths';
	import EntryForm from '$lib/components/cashflowr/EntryForm.svelte';
	import { monthsApi } from '$lib/api/client';
	import { uiStore } from '$lib/stores/ui.svelte';
	import { monthLabel } from '$lib/utils/format';
	import type { PageData } from './$types';
	import type { MonthUpdate } from '$lib/api/client';

	let { data }: { data: PageData } = $props();
	const { entry } = data;

	async function handleDelete() {
		if (!confirm(`Delete ${monthLabel(entry.year, entry.month)}? This cannot be undone.`)) return;
		await monthsApi.delete(entry.year, entry.month);
		uiStore.toast('Month deleted.', 'info');
		goto(resolve('/history'));
	}

	async function handleSubmit(payload: MonthUpdate) {
		await monthsApi.update(entry.year, entry.month, payload as MonthUpdate);
		uiStore.toast('Month updated!', 'success');
		await invalidateAll();
		goto(resolve('/dashboard'));
	}
</script>

<div class="container mx-auto max-w-screen-sm px-4 py-8 space-y-6">
	<div class="flex items-center justify-between">
		<div class="space-y-1">
			<h1 class="h2 font-bold">Edit month</h1>
			<p class="text-surface-500 text-sm">{monthLabel(entry.year, entry.month)}</p>
		</div>
		<button class="btn preset-tonal-error text-sm" onclick={handleDelete}>Delete</button>
	</div>
	<EntryForm
		initial={entry}
		isEdit
		onSubmit={handleSubmit}
	/>
</div>
