<script lang="ts">
	import { resolve } from '$app/paths';
	import { Settings } from 'lucide-svelte';
	import GitHubIcon from '$lib/components/icons/GitHubIcon.svelte';
	import Drawer from './Drawer.svelte';
	import Lightswitch from './Lightswitch.svelte';
	import ThemeSwitch from './ThemeSwitch.svelte';
	import Logo from '../icons/Logo.svelte';

	let titleDrawer = 'menu';
	const coreLinks = [
		{ href: resolve('/dashboard'), label: 'dashboard', target: '_self' },
		{ href: resolve('/history'), label: 'history', target: '_self' },
		{ href: resolve('/annual'), label: 'annual', target: '_self' },
		{ href: resolve('/planner'), label: 'planner', target: '_self' },
		{ href: resolve('/settings'), label: 'settings', target: '_self' }
	];

	const navLinks = coreLinks.filter((l) => l.href !== resolve('/settings'));
</script>

<header
	class="sticky top-0 z-50 flex h-[70px] w-full items-center border-b-[1px] border-surface-500/20 bg-surface-50/90 backdrop-blur dark:bg-surface-950/90"
>
	<div
		class="container mx-auto grid max-w-screen-2xl grid-cols-[auto_1fr_auto] items-center gap-4 px-4 xl:grid-cols-[1fr_auto_1fr] xl:px-10"
	>
		<!-- Left -->
		<div class="flex items-stretch justify-start gap-4">
			<!-- Mobile Nav Drawer -->
			<Drawer title={titleDrawer} navigation={coreLinks} />
			<!-- Logo -->
			<a class="hidden xl:inline-block" href={resolve('/')} title="cashflowr">
				<Logo width="32" height="32" />
			</a>
			<div class="hidden items-center xl:flex">
				<!-- Navigation -->
				{#each navLinks as link (link.href)}
					<a class="btn hover:preset-tonal" href={link.href} target={link.target}>
						{link.label}
					</a>
				{/each}
			</div>
		</div>
		<!-- Middle -->
		<div class="flex items-center gap-2"></div>
		<!-- Right -->
		<div class="flex items-stretch justify-end gap-2">
			<!-- Settings -->
			<a class="btn-icon hover:preset-tonal hidden xl:inline-flex" href={resolve('/settings')} title="settings">
				<Settings size={20} />
			</a>
			<!-- Mode and Theme -->
			<Lightswitch />
			<ThemeSwitch />
			<!-- Divider -->
			<span class="border-r border-surface-200-800"></span>
			<!-- Social -->
			<nav class="flex items-center gap-1">
				<a class="btn-icon hover:preset-tonal" href="https://github.com/mistahuman" rel="external">
					<GitHubIcon size={20} />
				</a>
			</nav>
		</div>
	</div>
</header>
