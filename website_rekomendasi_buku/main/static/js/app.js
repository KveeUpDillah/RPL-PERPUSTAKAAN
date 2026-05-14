/* ── BookAI — app.js ─────────────────────────────────────────── */

// ── CSRF helper ────────────────────────────────────────────────
function getCsrf() {
  return document.cookie.split(';')
    .map(c => c.trim()).find(c => c.startsWith('csrftoken='))
    ?.split('=')[1] || '';
}

// ── Fetch wrapper ───────────────────────────────────────────────
async function apiFetch(url, opts = {}) {

  try {

    const res = await fetch(url, {

      credentials: 'same-origin',

      headers: {
        'X-CSRFToken': getCsrf(),
        'Content-Type': 'application/json',
        ...opts.headers
      },

      ...opts,
    });

    if (!res.ok) return null;

    return await res.json();

  } catch {

    return null;
  }
}

// ── Modal state ─────────────────────────────────────────────────
let _currentBook = null;

function openBookModal(book) {
  _currentBook = book;
  const el = id => document.getElementById(id);

  el('modalTitle').textContent = book.title || '';
  el('modalAuthor').textContent = book.author || '—';
  el('modalYear').textContent = book.year || '—';
  el('modalLanguage').textContent = capitalise(book.language) || '—';
  el('modalDescription').textContent = book.description || 'Tidak ada deskripsi tersedia.';

const img = el('modalCoverImg');

const fallback = el('modalCoverFallback');

if (book.cover_url) {

  img.src = book.cover_url;

  img.style.display = 'block';

  fallback.style.display = 'none';

} else {

  img.style.display = 'none';

  fallback.style.display = 'flex';
}

  updateFavBtn(book.is_favorite);
  document.getElementById('bookModal').hidden = false;
  document.body.style.overflow = 'hidden';
}

function closeBookModal() {
  document.getElementById('bookModal').hidden = true;
  document.body.style.overflow = '';
}

function openLoginModal() {
  document.getElementById('loginRequiredModal').hidden = false;
  document.body.style.overflow = 'hidden';
}

function closeLoginModal() {
  document.getElementById('loginRequiredModal').hidden = true;
  document.body.style.overflow = '';
}

// Close modals on overlay click
document.addEventListener('click', e => {
  if (e.target.id === 'bookModal') closeBookModal();
  if (e.target.id === 'loginRequiredModal') closeLoginModal();
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') { closeBookModal(); closeLoginModal(); }
});

// ── Favourite toggle ────────────────────────────────────────────
function updateFavBtn(isFav) {
  const btn = document.getElementById('modalFavBtn');
  const text = document.getElementById('modalFavText');
  if (!btn) return;
  btn.classList.toggle('active', isFav);
  text.textContent = isFav ? 'Hapus dari Favorit' : 'Tambah ke Favorit';
}

async function toggleFavoriteFromModal() {
  if (!_currentBook) return;

  // Check if logged in — backend returns 401 if not
  const data = await apiFetch('/api/favorite/toggle/', {
    method: 'POST',
    body: JSON.stringify(_currentBook),
  });

  if (!data) {
    // 401 → show login modal
    closeBookModal();
    openLoginModal();
    return;
  }

  const isFav = data.status === 'added';
  _currentBook.is_favorite = isFav;
  updateFavBtn(isFav);

  // Sync card in grid if present
  document.querySelectorAll(`[data-book-key="${_currentBook.key}"]`).forEach(card => {
    card.dataset.isFavorite = isFav ? '1' : '0';
  });
}

// ── Render books ────────────────────────────────────────────────
function renderBooks(container, books, showRank = false) {
  container.innerHTML = '';
  books.forEach((book, i) => {
    const card = document.createElement('div');
    card.className = 'book-card';
    card.dataset.bookKey = book.key;
    card.dataset.isFavorite = book.is_favorite ? '1' : '0';
    card.onclick = () => openBookModal(book);

    const coverHtml = book.cover_url
      ? `<img src="${book.cover_url}" alt="${esc(book.title)}" loading="lazy" />`
      : `<div class="cover-fallback">
           <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
             <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
             <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
           </svg>
         </div>`;

    const rankBadge = showRank
      ? `<span class="rank-badge">${i + 1}</span>` : '';

    card.innerHTML = `
      <div class="book-cover">
        ${rankBadge}
        ${coverHtml}
        <div class="book-cover-overlay">
          <span class="book-title-overlay">${esc(book.title)}</span>
          <span class="book-author-overlay">${esc(book.author)}</span>
        </div>
      </div>
      <div class="book-info">
        <p class="book-title">${esc(book.title)}</p>
        <p class="book-author">${esc(book.author)}</p>
      </div>`;

    container.appendChild(card);
  });
}

// ── Utils ───────────────────────────────────────────────────────
function esc(str) {
  return String(str || '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

function capitalise(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}
