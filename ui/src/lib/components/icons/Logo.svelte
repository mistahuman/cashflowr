<script lang="ts">
	let { width = '32', height = '32' }: { width?: string; height?: string } = $props();
</script>

<!--
  Coin with milled/reeded edge (dashed circle, round linecap = bumps)
  + stonks chart inside (upward zigzag with arrowhead)
-->
<svg
	{width}
	{height}
	viewBox="0 0 32 32"
	fill="none"
	xmlns="http://www.w3.org/2000/svg"
>
	<!-- Milled coin edge: dashed strokes with round caps = reeded bumps -->
	<circle
		cx="16" cy="16" r="13"
		stroke="currentColor"
		stroke-width="2"
		stroke-dasharray="3 2.1"
		stroke-linecap="round"
	/>

	<!-- Stonks trend line: down, up, dip, spike -->
	<polyline
		points="7,22 10,17 14,20 17,13 21,16 24,9"
		stroke="currentColor"
		stroke-width="2"
		stroke-linecap="round"
		stroke-linejoin="round"
	/>

	<!-- Arrowhead at trend line end -->
	<polyline
		points="24,14 24,9 20,11"
		stroke="currentColor"
		stroke-width="2"
		stroke-linecap="round"
		stroke-linejoin="round"
	/>
</svg>
