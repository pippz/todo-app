from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import datetime

app = Flask(__name__)
app.jinja_env.globals['enumerate'] = enumerate

def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)

@app.route('/')
def index():
    tasks = load_tasks()
    notes = load_notes()
    return render_template('index.html', tasks=tasks, notes=notes)

@app.route('/add', methods=['POST'])
def add():
    tasks = load_tasks()
    task = request.form.get('task').strip()
    priority = request.form.get('priority').lower()
    due_date = request.form.get('due_date') or None
    if task and priority in ['low', 'medium', 'high']:
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
        new_task = request.form.get('task').strip()
        if new_task:
            tasks[index]['task'] = new_task
            tasks[index]['done'] = False
            save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/edit_priority/<int:index>', methods=['POST'])
def edit_priority(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        new_priority = request.form.get('priority').lower()
        if new_priority in ['low', 'medium', 'high']:
            tasks[index]['priority'] = new_priority
            save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/clear')
def clear():
    save_tasks([])
    return redirect(url_for('index'))

def load_notes():
    try:
        with open('notes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_notes(notes):
    with open('notes.json', 'w') as f:
        json.dump(notes, f)

@app.route('/notes/add', methods=['POST'])
def add_note():
    notes = load_notes()
    title = request.form.get('title').strip()
    body = request.form.get('body').strip()
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
        notes[index]['title'] = request.form.get('title').strip()
        notes[index]['body'] = request.form.get('body').strip()
        save_notes(notes)
    return redirect(url_for('index') + '#notes')

@app.route('/tasks/json')
def tasks_json():
    tasks = load_tasks()
    events = []
    for task in tasks:
        if task.get('due_date'):
            events.append({
                'title': task['task'],
                'start': task['due_date'],
                'color': '#f56a6a' if task['priority'] == 'high' else '#f5c26a' if task['priority'] == 'medium' else '#6ab4f5'
            })
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)