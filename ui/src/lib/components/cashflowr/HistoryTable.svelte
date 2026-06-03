<script lang="ts">
	import { goto } from '$app/navigation';
	import { AlertTriangle } from 'lucide-svelte';
	import type { MonthEntry } from '$lib/api/client';
	import { formatEur, formatRate, monthName } from '$lib/utils/format';

	interface Props {
		months: MonthEntry[];
	}

	let { months }: Props = $props();
</script>

{#if months.length === 0}
	<p class="text-surface-500 text-sm py-8 text-center">No entries yet. Add your first month.</p>
{:else}
	<div class="overflow-x-auto">
		<table class="table w-full text-sm">
			<thead>
				<tr class="text-xs uppercase tracking-widest text-surface-500">
					<th class="text-left py-2 px-3">Month</th>
					<th class="text-right py-2 px-3">Income</th>
					<th class="text-right py-2 px-3">Expenses</th>
					<th class="text-right py-2 px-3">Investments</th>
					<th class="text-right py-2 px-3">Savings</th>
					<th class="text-right py-2 px-3">Rate</th>
					<th class="text-right py-2 px-3">Net worth</th>
					<th class="text-right py-2 px-3">Δ NW</th>
					<th class="py-2 px-3"></th>
				</tr>
			</thead>
			<tbody>
				{#each months as m (m.id)}
					<tr
						class="border-t border-surface-200/50 dark:border-surface-800/50 hover:bg-surface-100/50 dark:hover:bg-surface-800/30 cursor-pointer transition-colors"
						onclick={() => goto(`/entry/${m.year}/${m.month}`)}
					>
						<td class="py-2 px-3 font-medium whitespace-nowrap">
							{monthName(m.month)} {m.year}
						</td>
						<td class="py-2 px-3 text-right font-mono">{formatEur(m.income)}</td>
						<td class="py-2 px-3 text-right font-mono">{formatEur(m.expenses)}</td>
						<td class="py-2 px-3 text-right font-mono">{formatEur(m.investments)}</td>
						<td
							class="py-2 px-3 text-right font-mono font-semibold {m.savings < 0
								? 'text-error-600 dark:text-error-400'
								: ''}"
						>
							{formatEur(m.savings)}
						</td>
						<td class="py-2 px-3 text-right font-mono">{formatRate(m.savings_rate)}</td>
						<td class="py-2 px-3 text-right font-mono">{formatEur(m.net_worth)}</td>
						<td
							class="py-2 px-3 text-right font-mono {m.net_worth_delta < 0
								? 'text-error-600 dark:text-error-400'
								: 'text-success-600 dark:text-success-400'}"
						>
							{m.net_worth_delta >= 0 ? '+' : ''}{formatEur(m.net_worth_delta)}
						</td>
						<td class="py-2 px-3">
							{#if m.consistency_check !== 0}
								<AlertTriangle size={14} class="text-warning-500" />
							{/if}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}
