from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

#imports sql database
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#telling app where database is located
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
db = SQLAlchemy(app)# initialize database with setting from app
app.app_context().push()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

#route from server
@app.route("/", methods=['POST', 'GET'])

#function end point
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return " There was a problem deleting that task"


# setting local host to 50100, use localhost:50100
if __name__ == '__main__':
    app.run(port=50100, debug=True)