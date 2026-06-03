<script lang="ts">
	interface Props {
		label: string;
		value: string;
		sub?: string;
		highlight?: 'positive' | 'negative' | 'neutral';
	}

	let { label, value, sub, highlight = 'neutral' }: Props = $props();

	const valueClass = $derived(
		highlight === 'positive'
			? 'text-success-600 dark:text-success-400'
			: highlight === 'negative'
				? 'text-error-600 dark:text-error-400'
				: 'text-surface-900 dark:text-surface-50'
	);
</script>

<div class="card p-4 space-y-1">
	<p class="text-xs font-medium uppercase tracking-widest text-surface-500">{label}</p>
	<p class="text-2xl font-bold font-mono {valueClass}">{value}</p>
	{#if sub}
		<p class="text-xs text-surface-500">{sub}</p>
	{/if}
</div>
