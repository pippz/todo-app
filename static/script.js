window.addEventListener('load', () => {
    const hash = window.location.hash;
    if (hash === '#notes') {
        document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.getElementById('section-notes').style.display = 'block';
        document.querySelector('.tab:nth-child(2)').classList.add('active');
    }
});

function switchTab(tab) {
    document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById('section-' + tab).style.display = 'block';
    event.target.classList.add('active');
    if (tab === 'calendar') initCalendar();
}

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

let calendarInitialized = false;

function initCalendar() {
    if (calendarInitialized) return;
    calendarInitialized = true;

    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: '/tasks/json',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek'
        }
    });
    calendar.render();
}

function toggleEdit(index) {
    const form = document.getElementById('edit-form-' + index);
    form.style.display = form.style.display === 'none' ? 'inline-flex' : 'none';
}

// MODAL
function openModal(message, url) {
    document.getElementById('modal-message').textContent = message;
    document.getElementById('modal-confirm').onclick = () => window.location.href = url;
    document.getElementById('modal-overlay').style.display = 'flex';
}

function closeModal() {
    document.getElementById('modal-overlay').style.display = 'none';
}

// SORTING
function sortTasks(value) {
    const list = document.getElementById('task-list');
    const cards = Array.from(list.querySelectorAll('.task-card'));
    const priorityOrder = { 'high': 0, 'medium': 1, 'low': 2 };

    cards.sort((a, b) => {
        if (value === 'priority') {
            const pa = a.dataset.priority;
            const pb = b.dataset.priority;
            return priorityOrder[pa] - priorityOrder[pb];
        }
        if (value === 'due_date') {
            const da = a.dataset.dueDate || '9999';
            const db = b.dataset.dueDate || '9999';
            return da.localeCompare(db);
        }
        if (value === 'status') {
            return a.dataset.done - b.dataset.done;
        }
        return 0;
    });

    cards.forEach(card => list.appendChild(card));
}