from flask import Flask, render_template, redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Todo.db"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    prof = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno}--{self.name}"


@app.route('/', methods=['GET', 'POST'])
def mpage():
    if request.method == 'POST':
        name = request.form['name']
        profession = request.form['prof']     
        data = Todo(name=name, prof=profession)
        db.session.add(data)
        db.session.commit()
        
    alldata = Todo.query.all()
    return render_template('index.html',allTodo = alldata)

@app.route('/delete/<int:sno>')
def delete(sno):
    data = Todo.query.filter_by(sno=sno).first()
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        name = request.form['name']
        prof = request.form['prof']     
        data = Todo.query.filter_by(sno=sno).first()
        data.name = name
        data.prof = prof
        db.session.add(data)
        db.session.commit()
        return redirect('/')
    data= Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', data=data)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        req_search = Todo.query.filter(Todo.prof.contains(query)).all()
    else:
        req_search = []
    return render_template('search.html', req_search=req_search)

@app.route('/prof', methods=['GET'])
def prof():
    prof = db.session.query(Todo.prof).distinct().all()
    return render_template('professions.html', prof = prof)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=1357)