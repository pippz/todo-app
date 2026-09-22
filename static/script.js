/* ── Theme toggle ── */
document.getElementById('theme').addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (e) {}
});

/* ── Segmented tab control ── */
const thumb = document.querySelector('.tab-thumb');

function moveThumb(el) {
    thumb.style.width = el.offsetWidth + 'px';
    thumb.style.transform = `translateX(${el.offsetLeft - 3}px)`;
}

function switchTab(tab, el) {
    document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById('section-' + tab).style.display = 'block';
    el.classList.add('active');
    moveThumb(el);
    if (tab === 'calendar') initCalendar();
}

window.addEventListener('load', () => {
    moveThumb(document.querySelector('.tab.active'));
    if (window.location.hash === '#notes') {
        switchTab('notes', document.querySelectorAll('.tab')[1]);
    }
});
window.addEventListener('resize', () => moveThumb(document.querySelector('.tab.active')));

/* ── Notes editor ── */
function openEditor(index, card) {
    const title = card.querySelector('.note-title').textContent;
    const body = card.querySelector('.note-body').textContent;
    document.getElementById('notes-grid').style.display = 'none';
    document.getElementById('note-editor').style.display = 'block';
    document.getElementById('editor-title').value = title;
    document.getElementById('editor-body').value = body;
    document.getElementById('editor-form').action = '/notes/edit/' + index;
    document.getElementById('editor-delete').href = '/notes/delete/' + index;
}

function closeEditor() {
    document.getElementById('note-editor').style.display = 'none';
    document.getElementById('notes-grid').style.display = 'grid';
}

/* ── Calendar ── */
let calendarInitialized = false;

function initCalendar() {
    if (calendarInitialized) return;
    calendarInitialized = true;

    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: '/tasks/json',
        height: 'auto',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek'
        }
    });
    calendar.render();
}

/* ── Inline task editing ── */
function toggleEdit(index) {
    document.getElementById('edit-form-' + index).classList.toggle('open');
}

/* ── Confirm modal ── */
function openModal(message, url) {
    document.getElementById('modal-message').textContent = message;
    document.getElementById('modal-confirm').onclick = () => window.location.href = url;
    document.getElementById('modal-overlay').style.display = 'flex';
}

function closeModal() {
    document.getElementById('modal-overlay').style.display = 'none';
}

/* ── Sorting ── */
function sortTasks(value) {
    const list = document.getElementById('task-list');
    const cards = Array.from(list.querySelectorAll('.task'));
    const priorityOrder = { high: 0, medium: 1, low: 2 };

    cards.sort((a, b) => {
        if (value === 'priority') {
            return priorityOrder[a.dataset.priority] - priorityOrder[b.dataset.priority];
        }
        if (value === 'due_date') {
            return (a.dataset.dueDate || '9999').localeCompare(b.dataset.dueDate || '9999');
        }
        if (value === 'status') {
            return a.dataset.done - b.dataset.done;
        }
        return 0;
    });

    cards.forEach(card => list.appendChild(card));
}
