from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample tasks list, no database required
tasks = [
    {'id': 1, 'title': 'Todo List App', 'category': 'Flask', 'completed': False},
]

# Routes
@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        new_task = {'id': len(tasks) + 1, 'title': title, 'category': category, 'completed': False}
        tasks.append(new_task)
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        task['completed'] = not task['completed']
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        tasks.remove(task)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
