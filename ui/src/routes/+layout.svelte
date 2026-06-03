<script lang="ts">
	import './layout.css';
	import Header from '$lib/components/generic/Header.svelte';
	import Footer from '$lib/components/generic/Footer.svelte';
	import { uiStore } from '$lib/stores/ui.svelte';

	let { children } = $props();

	const toastClass: Record<string, string> = {
		success: 'preset-filled-success-500',
		error: 'preset-filled-error-500',
		info: 'preset-filled-primary-500'
	};
</script>

<div class="flex min-h-screen flex-col">
	<Header />
	<main class="flex min-h-0 flex-1 flex-col">
		{@render children()}
	</main>
	<Footer />
</div>

<!-- Toast overlay -->
<div class="pointer-events-none fixed bottom-6 right-6 z-50 flex flex-col gap-2">
	{#each uiStore.toasts as toast (toast.id)}
		<div class="card px-4 py-3 text-sm shadow-lg {toastClass[toast.type] ?? toastClass.info}">
			{toast.message}
		</div>
	{/each}
</div>
