<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import type { MonthEntry } from '$lib/api/client';
	import { monthName } from '$lib/utils/format';

	interface Props {
		months: MonthEntry[];
	}

	let { months }: Props = $props();

	let canvas: HTMLCanvasElement;
	let chart: import('chart.js').Chart | null = null;

	onMount(async () => {
		const { Chart, BarElement, LinearScale, CategoryScale, Tooltip, Legend } =
			await import('chart.js');
		Chart.register(BarElement, LinearScale, CategoryScale, Tooltip, Legend);

		chart = new Chart(canvas, {
			type: 'bar',
			data: {
				labels: months.map((m) => `${monthName(m.month).slice(0, 3)} ${m.year}`),
				datasets: [
					{
						label: 'Income',
						data: months.map((m) => m.income),
						backgroundColor: 'oklch(88.68% 0.2 140.7deg / 0.7)'
					},
					{
						label: 'Expenses',
						data: months.map((m) => m.expenses),
						backgroundColor: 'oklch(64.84% 0.24 33.01deg / 0.7)'
					}
				]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: { tooltip: { mode: 'index', intersect: false } },
				scales: {
					y: {
						ticks: {
							callback: (v) =>
								new Intl.NumberFormat('de-DE', {
									style: 'currency',
									currency: 'EUR',
									maximumFractionDigits: 0
								}).format(v as number)
						}
					}
				}
			}
		});
	});

	onDestroy(() => chart?.destroy());

	$effect(() => {
		if (!chart) return;
		chart.data.labels = months.map((m) => `${monthName(m.month).slice(0, 3)} ${m.year}`);
		chart.data.datasets[0].data = months.map((m) => m.income);
		chart.data.datasets[1].data = months.map((m) => m.expenses);
		chart.update();
	});
</script>

<div class="relative h-64">
	<canvas bind:this={canvas}></canvas>
</div>
