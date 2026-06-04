<script lang="ts">
	import type { MonthCreate, MonthUpdate } from '$lib/api/client';
	import { formatEur, formatRate } from '$lib/utils/format';

	interface Props {
		initial?: {
			year: number;
			month: number;
			income: number;
			expenses: number;
			investments: number;
			portfolio_value?: number | null;
			notes?: string | null;
		};
		isEdit?: boolean;
		onSubmit: (data: MonthCreate | MonthUpdate) => Promise<void>;
	}

	const now = new Date();

	let { initial, isEdit = false, onSubmit }: Props = $props();

	let year = $state(initial?.year ?? now.getFullYear());
	let month = $state(initial?.month ?? now.getMonth() + 1);
	let income = $state<string>(initial?.income?.toString() ?? '');
	let expenses = $state<string>(initial?.expenses?.toString() ?? '');
	let investments = $state<string>(initial?.investments !== 0 ? (initial?.investments?.toString() ?? '') : '');
	let portfolioValue = $state<string>(initial?.portfolio_value?.toString() ?? '');
	let notes = $state<string>(initial?.notes ?? '');
	let loading = $state(false);
	let error = $state<string | null>(null);

	const incomeVal = $derived(parseFloat(income) || 0);
	const expensesVal = $derived(parseFloat(expenses) || 0);
	const investmentsVal = $derived(parseFloat(investments) || 0);

	const savings = $derived(incomeVal - expensesVal - investmentsVal);
	const wealthBuildingRate = $derived(
		incomeVal > 0 ? ((incomeVal - expensesVal) / incomeVal) * 100 : null
	);

	const savingsHighlight = $derived(savings < 0 ? 'text-error-600' : 'text-success-600');

	function validate(): string | null {
		if (parseFloat(income) < 0) return 'Income cannot be negative.';
		if (income !== '' && isNaN(parseFloat(income))) return 'Invalid income value.';
		if (parseFloat(expenses) < 0) return 'Expenses cannot be negative.';
		if (portfolioValue !== '' && parseFloat(portfolioValue) < 0) return 'Portfolio value cannot be negative.';
		return null;
	}

	async function handleSubmit(e: Event) {
		e.preventDefault();
		const err = validate();
		if (err) { error = err; return; }
		error = null;
		loading = true;
		try {
			const portfolioVal = portfolioValue !== '' ? parseFloat(portfolioValue) : null;
			const payload: MonthCreate | MonthUpdate = isEdit
				? {
						income: parseFloat(income),
						expenses: parseFloat(expenses),
						investments: parseFloat(investments) || 0,
						portfolio_value: portfolioVal,
						notes: notes.trim() || null
					}
				: {
						year,
						month,
						income: parseFloat(income) || 0,
						expenses: parseFloat(expenses) || 0,
						investments: parseFloat(investments) || 0,
						portfolio_value: portfolioVal,
						notes: notes.trim() || null
					};
			await onSubmit(payload);
		} catch (e: unknown) {
			error = e instanceof Error ? e.message : 'An error occurred.';
		} finally {
			loading = false;
		}
	}
</script>

<form onsubmit={handleSubmit} class="space-y-6 max-w-md">
	{#if !isEdit}
		<div class="grid grid-cols-2 gap-4">
			<label class="label">
				<span class="label-text">Year</span>
				<input type="number" class="input" bind:value={year} min="2000" max="2100" required />
			</label>
			<label class="label">
				<span class="label-text">Month</span>
				<select class="select" bind:value={month}>
					{#each Array.from({ length: 12 }, (_, i) => i + 1) as m}
						<option value={m}>{new Date(2000, m - 1).toLocaleString('default', { month: 'long' })}</option>
					{/each}
				</select>
			</label>
		</div>
	{/if}

	<label class="label">
		<span class="label-text">Income (€)</span>
		<input type="number" class="input" bind:value={income} min="0" step="0.01" placeholder="0.00" />
	</label>

	<label class="label">
		<span class="label-text">Expenses (€)</span>
		<input type="number" class="input" bind:value={expenses} min="0" step="0.01" placeholder="0.00" required />
	</label>

	<label class="label">
		<span class="label-text">
			Cash moved to/from investments (€)
			<span class="text-surface-400 text-xs">— positive = bought, negative = sold/received</span>
		</span>
		<input type="number" class="input" bind:value={investments} step="0.01" placeholder="0.00" />
	</label>

	<label class="label">
		<span class="label-text">
			Portfolio market value (€)
			<span class="text-surface-400 text-xs">— total current value of your investment portfolio</span>
		</span>
		<input type="number" class="input" bind:value={portfolioValue} min="0" step="0.01" placeholder="Leave blank if unchanged from last month" />
	</label>

	<label class="label">
		<span class="label-text">Notes <span class="text-surface-400 text-xs">— optional</span></span>
		<textarea class="textarea" bind:value={notes} rows="2" placeholder="Anything worth remembering about this month…"></textarea>
	</label>

	<!-- Live preview -->
	<div class="card preset-tonal p-4 space-y-2">
		<p class="text-xs font-semibold uppercase tracking-widest text-surface-500">Live preview</p>
		<div class="flex justify-between text-sm">
			<span class="text-surface-600 dark:text-surface-400">Savings</span>
			<span class="font-mono font-bold {savingsHighlight}">{formatEur(savings)}</span>
		</div>
		<div class="flex justify-between text-sm">
			<span class="text-surface-600 dark:text-surface-400">Wealth-building rate</span>
			<span class="font-mono font-bold">{formatRate(wealthBuildingRate)}</span>
		</div>
	</div>

	{#if error}
		<p class="text-error-600 text-sm">{error}</p>
	{/if}

	<button type="submit" class="btn preset-filled-primary-500 w-full" disabled={loading}>
		{loading ? 'Saving…' : isEdit ? 'Update month' : 'Save month'}
	</button>
</form>
