<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import EntryForm from '$lib/components/cashflowr/EntryForm.svelte';
	import { monthsApi } from '$lib/api/client';
	import { uiStore } from '$lib/stores/ui.svelte';
	import type { MonthCreate, MonthUpdate } from '$lib/api/client';

	async function handleSubmit(data: MonthCreate | MonthUpdate) {
		await monthsApi.create(data as MonthCreate);
		uiStore.toast('Month saved!', 'success');
		goto(resolve('/dashboard'));
	}
</script>

<div class="container mx-auto max-w-screen-sm px-4 py-8 space-y-6">
	<div class="space-y-1">
		<h1 class="h2 font-bold">Add month</h1>
		<p class="text-surface-500 text-sm">Enter your monthly cash flow data.</p>
	</div>
	<EntryForm onSubmit={handleSubmit} />
</div>
