<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import type { MonthEntry } from '$lib/api/client';
	import { monthName } from '$lib/utils/format';

	interface Props { months: MonthEntry[] }
	let { months }: Props = $props();

	let canvas: HTMLCanvasElement;
	let chart: import('chart.js').Chart | null = null;
	let chartReady = $state(false);

	const eur = (v: number) => new Intl.NumberFormat('de-DE', {
		style: 'currency', currency: 'EUR', maximumFractionDigits: 0
	}).format(v);

	onMount(async () => {
		const { Chart, LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend, Filler } =
			await import('chart.js');
		Chart.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend, Filler);

		chart = new Chart(canvas, {
			type: 'line',
			data: {
				labels: months.map((m) => `${monthName(m.month).slice(0, 3)} ${m.year}`),
				datasets: [
					{
						label: 'Liquid',
						data: months.map((m) => m.liquid_balance),
						fill: 'origin',
						tension: 0.3,
						borderColor: 'oklch(48.65% 0.3 279.02deg)',
						backgroundColor: 'oklch(48.65% 0.3 279.02deg / 0.35)',
						pointRadius: 3,
						pointHoverRadius: 5
					},
					{
						label: 'Net worth (liquid + portfolio)',
						data: months.map((m) => m.net_worth),
						fill: '-1',   // fills between this line and the liquid line
						tension: 0.3,
						borderColor: 'oklch(88.68% 0.2 140.7deg)',
						backgroundColor: 'oklch(88.68% 0.2 140.7deg / 0.4)',
						pointRadius: 3,
						pointHoverRadius: 5
					}
				]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					tooltip: {
						mode: 'index', intersect: false,
						callbacks: { label: (ctx) => ctx.parsed.y != null ? `${ctx.dataset.label}: ${eur(ctx.parsed.y)}` : '' }
					},
					legend: { position: 'bottom' }
				},
				scales: {
					y: {
						ticks: { callback: (v) => eur(v as number) }
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
		chart.data.datasets[0].data = months.map((m) => m.liquid_balance);
		chart.data.datasets[1].data = months.map((m) => m.net_worth);
		chart.update();
	});
</script>

<div class="relative h-64"><canvas bind:this={canvas}></canvas></div>
