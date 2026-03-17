// ch-shared.js — shared logic for all Tunarr channel pages

// ── Sub-tab switching ────────────────────────────────────────────────────────
function switchTab(id, btn) {
  document.querySelectorAll('.subtab-pane').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.subtab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('pane-' + id).classList.add('active');
  btn.classList.add('active');
}

// ── Expandable schedule slots ─────────────────────────────────────────────────
// SLOT_KEY is set per-page before this script runs
function toggleSlot(id) {
  const body  = document.getElementById('body-' + id);
  const arrow = document.getElementById('arrow-' + id);
  if (!body) return;
  const isOpen = body.classList.toggle('open');
  if (arrow) arrow.classList.toggle('open', isOpen);
  // persist
  const saved = JSON.parse(localStorage.getItem(SLOT_KEY) || '{}');
  saved[id] = isOpen;
  localStorage.setItem(SLOT_KEY, JSON.stringify(saved));
}

function restoreSlots() {
  const saved = JSON.parse(localStorage.getItem(SLOT_KEY) || '{}');
  Object.entries(saved).forEach(([id, open]) => {
    if (!open) return;
    const body  = document.getElementById('body-' + id);
    const arrow = document.getElementById('arrow-' + id);
    if (body)  body.classList.add('open');
    if (arrow) arrow.classList.add('open');
  });
}

// ── Acquire checklist ────────────────────────────────────────────────────────
// ACQ_KEY is set per-page before this script runs
function toggleAcq(id) {
  const item = document.getElementById('acq-' + id);
  if (!item) return;
  const isDone = item.classList.toggle('done');
  const cb = item.querySelector('.acq-cb');
  if (cb) cb.textContent = isDone ? '✓' : '';
  // persist
  const saved = JSON.parse(localStorage.getItem(ACQ_KEY) || '{}');
  saved[id] = isDone;
  localStorage.setItem(ACQ_KEY, JSON.stringify(saved));
  updateProgress();
}

function restoreAcq() {
  const saved = JSON.parse(localStorage.getItem(ACQ_KEY) || '{}');
  Object.entries(saved).forEach(([id, done]) => {
    if (!done) return;
    const item = document.getElementById('acq-' + id);
    if (!item) return;
    item.classList.add('done');
    const cb = item.querySelector('.acq-cb');
    if (cb) cb.textContent = '✓';
  });
  updateProgress();
}

function updateProgress() {
  document.querySelectorAll('.acquire-group').forEach(group => {
    const items = group.querySelectorAll('.acq-item');
    const done  = group.querySelectorAll('.acq-item.done');
    const bar   = group.querySelector('.progress-bar-fill');
    const count = group.querySelector('.acquire-count');
    const pct   = items.length ? (done.length / items.length) * 100 : 0;
    if (bar)   bar.style.width = pct + '%';
    if (count) count.textContent = done.length + ' / ' + items.length;
  });
  // overall total
  const allItems = document.querySelectorAll('.acq-item');
  const allDone  = document.querySelectorAll('.acq-item.done');
  const totalEl  = document.getElementById('acq-total');
  if (totalEl) totalEl.textContent = allDone.length + ' / ' + allItems.length + ' acquired';
}

function resetAcq() {
  if (!confirm('Reset all checkboxes for this channel?')) return;
  localStorage.removeItem(ACQ_KEY);
  document.querySelectorAll('.acq-item').forEach(item => {
    item.classList.remove('done');
    const cb = item.querySelector('.acq-cb');
    if (cb) cb.textContent = '';
  });
  updateProgress();
}

function markAllDone() {
  document.querySelectorAll('.acq-item').forEach(item => {
    item.classList.add('done');
    const cb = item.querySelector('.acq-cb');
    if (cb) cb.textContent = '✓';
  });
  const saved = {};
  document.querySelectorAll('.acq-item').forEach(item => { saved[item.id.replace('acq-', '')] = true; });
  localStorage.setItem(ACQ_KEY, JSON.stringify(saved));
  updateProgress();
}

// ── Init ────────────────────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
  restoreSlots();
  restoreAcq();
  updateProgress();
});
