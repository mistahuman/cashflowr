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

	const labels = $derived(months.map((m) => `${monthName(m.month).slice(0, 3)} ${m.year}`));
	const savingsRates = $derived(months.map((m) => m.savings_rate ?? null));
	const wealthRates = $derived(months.map((m) => m.wealth_building_rate ?? null));

	onMount(async () => {
		const { Chart, LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend, Filler } =
			await import('chart.js');
		Chart.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend, Filler);

		chart = new Chart(canvas, {
			type: 'line',
			data: {
				labels,
				datasets: [
					{
						label: 'Savings rate',
						data: savingsRates,
						tension: 0.3,
						borderColor: 'oklch(88.68% 0.2 140.7deg)',
						backgroundColor: 'oklch(88.68% 0.2 140.7deg / 0.1)',
						fill: true,
						pointRadius: 4,
						pointHoverRadius: 6,
						spanGaps: true
					},
					{
						label: 'Wealth-building rate',
						data: wealthRates,
						tension: 0.3,
						borderColor: 'oklch(48.65% 0.3 279.02deg)',
						backgroundColor: 'transparent',
						pointRadius: 4,
						pointHoverRadius: 6,
						spanGaps: true
					}
				]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					tooltip: {
						mode: 'index',
						intersect: false,
						callbacks: {
							label: (ctx) => {
								const v = ctx.parsed.y;
								return v != null ? `${ctx.dataset.label}: ${v.toFixed(1)}%` : '';
							}
						}
					},
					legend: { position: 'bottom' }
				},
				scales: {
					y: {
						ticks: { callback: (v) => `${v}%` }
					}
				}
			}
		});
	});

	onDestroy(() => chart?.destroy());

	$effect(() => {
		if (!chart) return;
		chart.data.labels = months.map((m) => `${monthName(m.month).slice(0, 3)} ${m.year}`);
		chart.data.datasets[0].data = months.map((m) => m.savings_rate ?? null);
		chart.data.datasets[1].data = months.map((m) => m.wealth_building_rate ?? null);
		chart.update();
	});
</script>

<div class="relative h-64">
	<canvas bind:this={canvas}></canvas>
</div>
