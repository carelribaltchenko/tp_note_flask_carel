from .app import app
from flask import render_template
from .models import get_sample, get_author
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired
from flask import url_for, redirect
from .app import db

class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators=[DataRequired()])

@app.route ("/")
def home():
    return render_template(
        "home.html",
        title="Hello World")
    
    
@app.route ("/name")
def show_name():
    return render_template(
        "home.html",
        title="name",
        names=["Carel"])
    
    
@app.route ("/sample")
def sample():
    return render_template(
        "home.html",
        title="My Books !",
        books=get_sample())
    
    
@app.route("/detail/<id>")
def detail(id):
    books = get_sample()
    book = books[int(id)]
    return render_template(
    "detail.html",
    b=book)
    
@app.route("/edit-author/<int:id>")
def edit_author(id):
    a = get_author(id)
    f = AuthorForm(id=a.id, name=a.name)
    return render_template(
        "edit-author.html",
        author=a, form = f)
    
@app.route("/save/author/", methods =("POST" ,))
def save_author():
        a = None
        f = AuthorForm()
        if f.validate_on_submit():
            id = int(f.id.data)
            a = get_author(id)
            a.name = f.name.data
            db.session.commit()
            return redirect(url_for('sample', id=a.id))
        a = get_author(int(f.id.data))
        return render_template(
            "edit-author.html",
            author =a, form=f)