<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import type { MonthEntry } from '$lib/api/client';
	import { monthName } from '$lib/utils/format';

	interface Props {
		months: MonthEntry[];
		yMin?: number;
		yMax?: number;
	}

	let { months, yMin, yMax }: Props = $props();

	let canvas: HTMLCanvasElement;
	let chart: import('chart.js').Chart | null = null;
	let chartReady = $state(false);

	onMount(async () => {
		const { Chart, LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Filler } =
			await import('chart.js');
		Chart.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Filler);

		chart = new Chart(canvas, {
			type: 'line',
			data: {
				labels: months.map((m) => `${monthName(m.month).slice(0, 3)} ${m.year}`),
				datasets: [
					{
						label: 'Net Worth',
						data: months.map((m) => m.net_worth),
						fill: true,
						tension: 0.3,
						borderColor: 'oklch(48.65% 0.3 279.02deg)',
						backgroundColor: 'oklch(48.65% 0.3 279.02deg / 0.1)',
						pointRadius: 4,
						pointHoverRadius: 6
					}
				]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: { tooltip: { mode: 'index', intersect: false } },
				scales: {
					y: {
						min: yMin,
						max: yMax,
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
		chartReady = true;
	});

	onDestroy(() => chart?.destroy());

	$effect(() => {
		if (!chartReady || !chart) return;
		chart.data.labels = months.map((m) => `${monthName(m.month).slice(0, 3)} ${m.year}`);
		chart.data.datasets[0].data = months.map((m) => m.net_worth);
		if (chart.options.scales?.y) {
			chart.options.scales.y.min = yMin;
			chart.options.scales.y.max = yMax;
		}
		chart.update();
	});
</script>

<div class="relative h-64">
	<canvas bind:this={canvas}></canvas>
</div>
