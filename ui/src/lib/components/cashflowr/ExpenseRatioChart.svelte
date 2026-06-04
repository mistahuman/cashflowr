<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import type { MonthEntry } from '$lib/api/client';
	import { monthName } from '$lib/utils/format';

	interface Props { months: MonthEntry[] }
	let { months }: Props = $props();

	let canvas: HTMLCanvasElement;
	let chart: import('chart.js').Chart | null = null;
	let chartReady = $state(false);

	const ratio = (m: MonthEntry) => m.income > 0 ? Math.round(m.expenses / m.income * 1000) / 10 : null;

	onMount(async () => {
		const { Chart, LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip } =
			await import('chart.js');
		Chart.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip);

		chart = new Chart(canvas, {
			type: 'line',
			data: {
				labels: months.map((m) => `${monthName(m.month).slice(0, 3)} ${m.year}`),
				datasets: [{
					label: 'Expense ratio',
					data: months.map(ratio),
					tension: 0.3,
					borderColor: 'oklch(64.84% 0.24 33.01deg)',
					backgroundColor: 'oklch(64.84% 0.24 33.01deg / 0.1)',
					fill: true,
					pointRadius: 4,
					pointHoverRadius: 6,
					spanGaps: true
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					tooltip: {
						mode: 'index', intersect: false,
						callbacks: { label: (ctx) => `Expense ratio: ${ctx.parsed.y?.toFixed(1)}%` }
					}
				},
				scales: {
					y: {
						ticks: { callback: (v) => `${v}%` }
					}
				}
			}
		});
		chartReady = true;
	});

	onDestroy(() => chart?.destroy());

	$effect(() => {
		if (!chartReady || !chart) return;
		chart.data.labels = months.map((m) => `${monthName(m.month).slice(0, 3)} ${m.year}`);
		chart.data.datasets[0].data = months.map(ratio);
		chart.update();
	});
</script>

<div class="relative h-64"><canvas bind:this={canvas}></canvas></div>
