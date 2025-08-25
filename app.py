from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Mytask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f'<Task {self.id}>'


#HOME ROUTE
@app.route('/',methods=['POST','GET'])
def index():
    #add task
    if request.method == 'POST':
        current_task = request.form['content']
        new_task = Mytask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
        
        
    #see all tasks
    
    else:
        tasks = Mytask.query.order_by(Mytask.created).all()
        return render_template('index.html', tasks=tasks)


#Delete Route
@app.route('/delete/<int:id>')
def delete(id:int):
    delete_task = Mytask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


#Update Route
@app.route('/update/<int:id>', methods=['GET','POST'])
def edit(id: int):
    task = Mytask.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)