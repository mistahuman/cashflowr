<script lang="ts">
	import { SunMoon } from 'lucide-svelte';
	import { browser } from '$app/environment';

	function toggleMode() {
		if (!browser) return;
		const current = document.documentElement.getAttribute('data-mode') || 'dark';
		const next = current === 'dark' ? 'light' : 'dark';
		document.documentElement.setAttribute('data-mode', next);
		localStorage.setItem('mode', next);
	}
</script>

<nav>
	<button class="btn-icon hover:preset-tonal" title="Toggle dark mode." onclick={toggleMode}>
		<SunMoon size={20} />
	</button>
</nav>
