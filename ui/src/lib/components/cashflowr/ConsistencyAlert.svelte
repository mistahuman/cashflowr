<script lang="ts">
	import { AlertTriangle } from 'lucide-svelte';
	import { formatEur, monthLabel } from '$lib/utils/format';
	import type { MonthEntry } from '$lib/api/client';

	interface Props {
		month: MonthEntry;
	}

	let { month }: Props = $props();
</script>

{#if month.consistency_check !== 0}
	<div
		class="flex items-start gap-3 rounded border border-warning-400/40 bg-warning-50 px-4 py-3 text-warning-950 dark:bg-warning-950/20 dark:text-warning-200"
	>
		<AlertTriangle size={18} class="mt-0.5 shrink-0 text-warning-500" />
		<div>
			<p class="font-semibold text-sm">Consistency check failed for {monthLabel(month.year, month.month)}</p>
			<p class="text-xs mt-0.5">
				Net worth delta differs from savings + investments by
				<span class="font-mono font-bold">{formatEur(Math.abs(month.consistency_check))}</span>.
				There may be an unregistered transaction.
			</p>
		</div>
	</div>
{/if}
