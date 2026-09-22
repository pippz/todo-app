from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import datetime

app = Flask(__name__)
app.jinja_env.globals['enumerate'] = enumerate

VALID_PRIORITIES = ('low', 'medium', 'high')


def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)


def load_notes():
    try:
        with open('notes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_notes(notes):
    with open('notes.json', 'w') as f:
        json.dump(notes, f)


@app.route('/')
def index():
    tasks = load_tasks()
    notes = load_notes()
    return render_template('index.html', tasks=tasks, notes=notes)


@app.route('/add', methods=['POST'])
def add():
    tasks = load_tasks()
    task = request.form.get('task', '').strip()
    priority = request.form.get('priority', '').lower()
    due_date = request.form.get('due_date') or None
    if task and priority in VALID_PRIORITIES:
        date = datetime.date.today().strftime('%d/%m/%Y')
        tasks.append({'task': task, 'priority': priority, 'done': False, 'date': date, 'due_date': due_date})
        save_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/delete/<int:index>')
def delete(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/toggle/<int:index>')
def toggle(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]['done'] = not tasks[index]['done']
        save_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/edit/<int:index>', methods=['POST'])
def edit(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        new_task = request.form.get('task', '').strip()
        if new_task:
            tasks[index]['task'] = new_task
            save_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/edit_priority/<int:index>', methods=['POST'])
def edit_priority(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        new_priority = request.form.get('priority', '').lower()
        if new_priority in VALID_PRIORITIES:
            tasks[index]['priority'] = new_priority
            save_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/clear')
def clear():
    save_tasks([])
    return redirect(url_for('index'))


@app.route('/notes/add', methods=['POST'])
def add_note():
    notes = load_notes()
    title = request.form.get('title', '').strip()
    body = request.form.get('body', '').strip()
    if title:
        date = datetime.date.today().strftime('%d/%m/%Y')
        notes.append({'title': title, 'body': body, 'date': date})
        save_notes(notes)
    return redirect(url_for('index') + '#notes')


@app.route('/notes/delete/<int:index>')
def delete_note(index):
    notes = load_notes()
    if 0 <= index < len(notes):
        notes.pop(index)
        save_notes(notes)
    return redirect(url_for('index') + '#notes')


@app.route('/notes/edit/<int:index>', methods=['POST'])
def edit_note(index):
    notes = load_notes()
    if 0 <= index < len(notes):
        title = request.form.get('title', '').strip()
        if title:
            notes[index]['title'] = title
            notes[index]['body'] = request.form.get('body', '').strip()
            save_notes(notes)
    return redirect(url_for('index') + '#notes')


@app.route('/tasks/json')
def tasks_json():
    tasks = load_tasks()
    colors = {'high': '#e2573b', 'medium': '#d69a2d', 'low': '#6a7fd6'}
    events = [
        {'title': t['task'], 'start': t['due_date'], 'color': colors.get(t['priority'], colors['low'])}
        for t in tasks if t.get('due_date')
    ]
    return jsonify(events)


if __name__ == '__main__':
    app.run(debug=True)
