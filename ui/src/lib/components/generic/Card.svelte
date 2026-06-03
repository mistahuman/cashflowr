<script lang="ts">
	import type { Snippet } from 'svelte';

	let {
		title = '',
		children
	}: {
		title?: string;
		children?: Snippet;
	} = $props();
</script>

<div class="w-full card border-[1px] border-surface-200-800 preset-filled-surface-100-900 p-4">
	<header class="h3">
		{title}
	</header>
	<hr class="divider" />
	<article class="p-4">
		{@render children?.()}
	</article>
</div>
