let toasts = $state<{ id: number; message: string; type: 'success' | 'error' | 'info' }[]>([]);
let _nextId = 0;

export const uiStore = {
	get toasts() {
		return toasts;
	},
	toast(message: string, type: 'success' | 'error' | 'info' = 'info', duration = 3000) {
		const id = _nextId++;
		toasts.push({ id, message, type });
		setTimeout(() => {
			toasts = toasts.filter((t) => t.id !== id);
		}, duration);
	}
};
