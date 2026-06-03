<script lang="ts">
	let { classList = 'p-4' }: { classList?: string } = $props();
</script>

<footer class="border-t-[1px] border-surface-500/20 {classList}">
	<div class="container mx-auto flex flex-col items-center justify-between gap-4 xl:flex-row">
		<div class="flex items-center gap-4">
			<p class="text-xs opacity-60">
				built by <a class="underline" href="https://www.github.com/mistahuman" target="_blank"
					>mistahuman</a
				>.
				<!-- built with <a class="underline" href="https://skeleton.dev" target="_blank">Skeleton UI</a>
				+
				<a class="underline" href="https://kit.svelte.dev" target="_blank">SvelteKit</a>. -->
			</p>
		</div>
		<!-- Social -->
		<nav class="flex items-center"></nav>
	</div>
</footer>
