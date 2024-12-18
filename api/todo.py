from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Vercel doesn't persist SQLite databases, so we use a cloud database in production.
# For local development, you can use SQLite with this URI:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/todo.db'
# You can replace this with a cloud database URI (PostgreSQL or MySQL) in production.
# Example for PostgreSQL: 'postgresql://username:password@hostname/dbname'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Routes
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        new_task = Task(title=title, category=category)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# Initialize the database
with app.app_context():
    db.create_all()

# The handler function for serverless function on Vercel
def handler(request):
    return app(request)
