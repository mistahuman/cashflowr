<script lang="ts">
	interface Props {
		label: string;
		value: string;
		sub?: string;
		highlight?: 'positive' | 'negative' | 'neutral';
		delta?: string;
		deltaPositive?: boolean | null;
	}

	let { label, value, sub, highlight = 'neutral', delta, deltaPositive }: Props = $props();

	const valueClass = $derived(
		highlight === 'positive'
			? 'text-success-600 dark:text-success-400'
			: highlight === 'negative'
				? 'text-error-600 dark:text-error-400'
				: 'text-surface-900 dark:text-surface-50'
	);

	const deltaClass = $derived(
		deltaPositive === true
			? 'text-success-600 dark:text-success-400'
			: deltaPositive === false
				? 'text-error-600 dark:text-error-400'
				: 'text-surface-400'
	);
</script>

<div class="card p-4 space-y-1">
	<p class="text-xs font-medium uppercase tracking-widest text-surface-500">{label}</p>
	<p class="text-2xl font-bold font-mono {valueClass}">{value}</p>
	{#if delta}
		<p class="text-xs font-mono {deltaClass}">{delta}</p>
	{/if}
	{#if sub}
		<p class="text-xs text-surface-500">{sub}</p>
	{/if}
</div>
