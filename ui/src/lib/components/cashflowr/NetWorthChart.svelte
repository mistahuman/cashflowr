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
	const data = $derived(months.map((m) => m.net_worth));

	onMount(async () => {
		const { Chart, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Filler } =
			await import('chart.js');
		Chart.register(LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Filler);

		chart = new Chart(canvas, {
			type: 'line',
			data: {
				labels,
				datasets: [
					{
						label: 'Net Worth',
						data,
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
		chart.data.datasets[0].data = months.map((m) => m.net_worth);
		chart.update();
	});
</script>

<div class="relative h-64">
	<canvas bind:this={canvas}></canvas>
</div>
