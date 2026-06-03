<script lang="ts">
	import type { PageData } from './$types';
	import HistoryTable from '$lib/components/cashflowr/HistoryTable.svelte';
	import { resolve } from '$app/paths';

	let { data }: { data: PageData } = $props();
</script>

<div class="container mx-auto max-w-screen-xl px-4 py-8 space-y-6">
	<div class="flex items-center justify-between">
		<h1 class="h2 font-bold">History</h1>
		<a href={resolve('/entry')} class="btn preset-filled-primary-500 text-sm">+ Add month</a>
	</div>
	<div class="card p-4">
		<HistoryTable months={data.months} />
	</div>
</div>
