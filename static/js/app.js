/* 3-Gate Stock Analysis Dashboard - Shared JS */

// ── API Helper ──────────────────────────────────────────────────────────────

async function apiCall(url, options = {}) {
    try {
        const resp = await fetch(url, options);
        const data = await resp.json();
        if (data.error && resp.status >= 400) {
            showError(data.message || data.error);
            return null;
        }
        return data;
    } catch (e) {
        console.error('API call failed:', e);
        return null;
    }
}

// ── UI Helpers ──────────────────────────────────────────────────────────────

function show(id) {
    const el = document.getElementById(id);
    if (el) el.classList.remove('d-none');
}

function hide(id) {
    const el = document.getElementById(id);
    if (el) el.classList.add('d-none');
}

function showError(msg) {
    const alert = document.getElementById('global-alert');
    const text = document.getElementById('global-alert-text');
    if (alert && text) {
        text.textContent = msg;
        alert.classList.remove('d-none');
        alert.classList.add('show');
        setTimeout(() => {
            alert.classList.remove('show');
            alert.classList.add('d-none');
        }, 8000);
    }
}

// ── Formatters ──────────────────────────────────────────────────────────────

function formatINR(val) {
    if (val === null || val === undefined) return '--';
    const num = Number(val);
    if (isNaN(num)) return '--';
    if (Math.abs(num) >= 1e7) {
        return '\u20B9' + (num / 1e7).toFixed(2) + ' Cr';
    }
    if (Math.abs(num) >= 1e5) {
        return '\u20B9' + (num / 1e5).toFixed(2) + ' L';
    }
    return '\u20B9' + num.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// ── Verdict Colors ──────────────────────────────────────────────────────────

function verdictColor(verdict) {
    const map = {
        'BUY': 'bg-success',
        'ACCUMULATE': 'bg-primary',
        'WAIT': 'bg-warning text-dark',
        'AVOID': 'bg-danger',
        'SKIP': 'bg-secondary',
    };
    return map[verdict] || 'bg-secondary';
}

function verdictBorder(verdict) {
    const map = {
        'BUY': 'verdict-buy bg-dark border-secondary',
        'ACCUMULATE': 'verdict-accumulate bg-dark border-secondary',
        'WAIT': 'verdict-wait bg-dark border-secondary',
        'AVOID': 'verdict-avoid bg-dark border-secondary',
        'SKIP': 'verdict-skip bg-dark border-secondary',
    };
    return map[verdict] || 'bg-dark border-secondary';
}

function valColor(verdict) {
    const map = {
        'CHEAP': 'bg-success',
        'FAIR': 'bg-info',
        'RICH': 'bg-warning text-dark',
        'EXTREME': 'bg-danger',
    };
    return map[verdict] || 'bg-secondary';
}

// ── Kite Status Badge (navbar) ──────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    apiCall('/api/kite/status').then(d => {
        const el = document.getElementById('kite-status-badge');
        if (!el || !d) return;
        if (d.connected) {
            el.innerHTML = '<i class="bi bi-circle-fill text-success me-1" style="font-size:0.5rem"></i>Kite';
        } else if (d.configured) {
            el.innerHTML = '<i class="bi bi-circle-fill text-warning me-1" style="font-size:0.5rem"></i>Kite';
        }
    });
});
