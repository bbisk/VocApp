import os
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random

project_dir = os.path.dirname(os.path.abspath(__file__))
# Set you SQLite database file path
database_file = "sqlite:///{}".format(os.path.join(project_dir, "vocab.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class vocabAdd(db.Model):
    __tablename__ = "vocab"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(80), unique=True, nullable=False)
    translation = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return self.word

# Check a word if exists in the database and adding on  POST method
@app.route('/', methods=['GET', 'POST'])
def index_page():
    exist = vocabAdd.query.filter_by(word=request.form.get("word")).first()
    if exist:
        err = "This word already exists in the database."
        items = vocabAdd.query.all()
        return render_template('index.html', items=items, err=err, warning="danger")
    else:
        if request.method == 'POST':
            item = vocabAdd(word=request.form.get("word").lower(), translation=request.form.get("translation").lower())
            db.session.add(item)
            db.session.commit()
        items = vocabAdd.query.all()
        return render_template('index.html', items=items)

# Displaying the word for modification or removal
@app.route('/<word>')
def index_edit(word):
    items = vocabAdd.query.all()
    query = vocabAdd.query.filter_by(word=word).first()
    return render_template('index.html', items=items, word=word, query=query)

# Saving updated word in the database
@app.route('/<word>/update', methods=['POST'])
def update(word):
    newword = request.form.get("newword")
    oldword = request.form.get("oldword")
    newtrans = request.form.get("newtrans")
    oldtrans = request.form.get("oldtrans")
    item = vocabAdd.query.filter_by(word=oldword).first()
    item.word = newword.lower()
    item.translation = newtrans.lower()
    db.session.commit()
    return redirect('/')

# Deleteing the word
@app.route('/<word>/delete', methods=['POST'])
def delete(word):
    word = request.form.get("word")
    item = vocabAdd.query.filter_by(word=word).first()
    db.session.delete(item)
    db.session.commit()
    return redirect('/')

# Exam function. Draw a random item from a database and checks for correct translation.
@app.route('/exam/start', methods=['GET', 'POST'])
def exam():
    items = vocabAdd.query.all()
    list = [i.id for i in items]
    # for i in items:
    #     list.append(i.id)
    item = vocabAdd.query.filter_by(id=random.choice(list)).first()
    if request.method == 'POST':
        wordcheck = request.form.get("wordcheck").lower()
        item_check = vocabAdd.query.filter_by(id=request.form.get("newid")).first()
        print(item_check.translation)
        if wordcheck not in item_check.translation:
            err = "Try again!"
            return render_template('index.html', item=item, err=err, warning="danger")
        else:
            err = "Correct!"
            return render_template('index.html', item=item, err=err, warning="success")
    return render_template('index.html', item=item)



if __name__ == '__main__':
    app.run(debug=True)

