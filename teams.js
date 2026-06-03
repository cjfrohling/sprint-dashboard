// Sprint Status Dashboard — persistent client-side enhancements
// This file is loaded by index.html and must not be deleted by the auto-refresh routine.

(function () {
  // ── Last refreshed timestamp ──────────────────────────────────────────────
  const el = document.getElementById('last-refreshed');
  if (el) {
    const now = new Date();
    el.textContent = now.toLocaleString('en-CA', {
      year: 'numeric', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit', second: '2-digit',
      hour12: false, timeZoneName: 'short'
    });
  }

  // ── Team grouping with coloured dividers ──────────────────────────────────
  const TEAM_MAP = {
    'Nick Karch': 'Frontend', 'Chris Schultz': 'Frontend', 'Gustavo Polo': 'Frontend',
    'Ganesh Abothula': 'Backend', 'Nageswara Rao Recharla': 'Backend', 'Krishna Kodicherla': 'Backend',
    'Lenin johnson': 'Apps', 'Lenin Johnson': 'Apps',
    'Patrick Galego': 'UX',
    'Swetha Kalluri': 'QA', 'Srinivas Jayaram Rao': 'QA',
  };
  const TEAM_COLORS = {
    Frontend: '#2a6aac', Backend: '#2a7a48',
    Apps: '#6a3e90', UX: '#b06020', QA: '#9b5a20',
  };
  const TEAM_ORDER = ['Frontend', 'Backend', 'Apps', 'UX', 'QA', 'Other'];

  function makeDivider(team) {
    const d = document.createElement('div');
    d.style.cssText = 'display:flex;align-items:center;gap:5px;font-size:.63rem;font-weight:700;' +
      'text-transform:uppercase;letter-spacing:.8px;color:#8b9ba8;padding:6px 4px 3px;' +
      'border-bottom:1px solid rgba(255,255,255,.1);margin-top:8px';
    const dot = document.createElement('span');
    dot.style.cssText = 'width:7px;height:7px;border-radius:50%;flex-shrink:0;background:' +
      (TEAM_COLORS[team] || '#555');
    d.appendChild(dot);
    d.appendChild(document.createTextNode(team));
    return d;
  }

  document.querySelectorAll('.col-body').forEach(col => {
    const tickets = Array.from(col.querySelectorAll('.ticket, .card'));
    if (!tickets.length) return;

    const groups = {};
    tickets.forEach(t => {
      const avatar = t.querySelector('[title]');
      const assignee = avatar ? avatar.getAttribute('title') : '';
      const team = TEAM_MAP[assignee] || 'Other';
      (groups[team] = groups[team] || []).push(t);
    });

    col.innerHTML = '';
    TEAM_ORDER.forEach(team => {
      if (!groups[team]) return;
      col.appendChild(makeDivider(team));
      groups[team].forEach(t => col.appendChild(t));
    });
  });
})();
