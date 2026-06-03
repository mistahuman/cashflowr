<script lang="ts">
	import { Menu, X } from 'lucide-svelte';
	import type { ResolvedPathname } from '$app/types';

	interface NavLink {
		href: ResolvedPathname;
		label: string;
		target?: string;
	}

	let { title = '', navigation = [] }: { title: string; navigation?: NavLink[] } = $props();
	let open = $state(false);

	function toggle() {
		open = !open;
	}
</script>

<!-- Hamburger Menu -->
<button class="btn-icon xl:hidden" onclick={toggle}>
	<Menu size={20} />
</button>

<!-- Drawer Panel -->
<div
	class="fixed top-0 bottom-0 left-0 z-50 h-screen w-[320px] space-y-10 overflow-y-auto preset-filled-surface-100-900 p-4 pb-24 shadow-xl transition-transform duration-100 xl:hidden"
	class:-translate-x-[320px]={!open}
	class:translate-x-0={open}
>
	<!-- Header -->
	<header class="flex items-center justify-between">
		<h2 class="h3">{title}</h2>
		<button class="btn-icon" onclick={toggle}>
			<X size={20} />
		</button>
	</header>
	<!-- Navigation -->
	<nav class="flex flex-col gap-2">
		{#each navigation as link (link.href)}
			<a class="anchor hover:underline" href={link.href} target={link.target} onclick={toggle}>
				{link.label}
			</a>
		{/each}
	</nav>
</div>
