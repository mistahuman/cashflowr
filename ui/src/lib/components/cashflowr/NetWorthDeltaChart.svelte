<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import type { MonthEntry } from '$lib/api/client';
	import { monthName } from '$lib/utils/format';

	interface Props { months: MonthEntry[] }
	let { months }: Props = $props();

	let canvas: HTMLCanvasElement;
	let chart: import('chart.js').Chart | null = null;
	let chartReady = $state(false);

	const positiveColor = 'oklch(88.68% 0.2 140.7deg / 0.8)';
	const negativeColor = 'oklch(64.84% 0.24 33.01deg / 0.8)';

	onMount(async () => {
		const { Chart, BarController, BarElement, LinearScale, CategoryScale, Tooltip } =
			await import('chart.js');
		Chart.register(BarController, BarElement, LinearScale, CategoryScale, Tooltip);

		chart = new Chart(canvas, {
			type: 'bar',
			data: {
				labels: months.map((m) => `${monthName(m.month).slice(0, 3)} ${m.year}`),
				datasets: [{
					label: 'Net worth change',
					data: months.map((m) => m.net_worth_delta),
					backgroundColor: months.map((m) => m.net_worth_delta >= 0 ? positiveColor : negativeColor)
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: { tooltip: { mode: 'index', intersect: false } },
				scales: {
					y: {
						ticks: {
							callback: (v) => new Intl.NumberFormat('de-DE', {
								style: 'currency', currency: 'EUR', maximumFractionDigits: 0
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
		chart.data.datasets[0].data = months.map((m) => m.net_worth_delta);
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		(chart.data.datasets[0] as any).backgroundColor = months.map((m) =>
			m.net_worth_delta >= 0 ? positiveColor : negativeColor
		);
		chart.update();
	});
</script>

<div class="relative h-64"><canvas bind:this={canvas}></canvas></div>
