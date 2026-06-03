export function formatDate(date: Date | string, locale = 'en-US'): string {
	return new Date(date).toLocaleDateString(locale, {
		day: '2-digit',
		month: 'long',
		year: 'numeric'
	});
}

export function truncate(str: string, maxLength: number): string {
	return str.length > maxLength ? str.slice(0, maxLength - 1) + '…' : str;
}

export function slugify(str: string): string {
	return str
		.toLowerCase()
		.trim()
		.replace(/\s+/g, '-')
		.replace(/[^\w-]/g, '');
}

export function formatEur(n: number): string {
	return new Intl.NumberFormat('de-DE', {
		style: 'currency',
		currency: 'EUR',
		minimumFractionDigits: 2,
		maximumFractionDigits: 2
	}).format(n);
}

export function formatRate(n: number | null | undefined): string {
	if (n == null) return '—';
	return n.toFixed(1) + '%';
}

export function monthName(month: number): string {
	return new Date(2000, month - 1, 1).toLocaleString('default', { month: 'long' });
}

export function monthLabel(year: number, month: number): string {
	return `${monthName(month)} ${year}`;
}
