import os

import click
from flask import Flask
from flask import render_template, flash, redirect, url_for, abort
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "i am secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///" + os.path.join(app.root_path, "data.db"))
db = SQLAlchemy(app)


# CRUD
class NotesForm(FlaskForm):
    body = TextAreaField("Message", validators=[DataRequired(), ])
    submit = SubmitField("Submit")


class EditForm(FlaskForm):
    body = TextAreaField("Edit", validators=[DataRequired(), ])
    submit = SubmitField("Submit")


class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")


class NotesDatabase(db.Model):
    note_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)


# 一对多
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    passages = db.relationship("Passages")


class Passages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    post_time = db.Column(db.Time)

    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))


# 一对多双向
class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    books = db.relationship("Books", back_populates="writer")


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    content = db.Column(db.Text)

    writer_id = db.Column(db.Integer, db.ForeignKey("writer.id"))
    writer = db.relationship("Writer", back_populates="books")


# 多对一
class Objects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    object_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    objects = db.relationship("Person")


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))


# 一对一
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    capital = db.relationship("Capital", use_list=False)


class Capital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    city = db.relationship("City")


# 多对多
association_table = db.Table(
    "association",
    db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
    db.Column("teacher_id", db.Integer, db.ForeignKey("teacher_id")),
)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    office = db.Column(db.String(20))

    students = db.relationship(
        "Student",
        secondary=association_table,
        back_populates="teachers"
    )


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    grade = db.Column(db.String(20))
    teachers = db.relationship(
        "Teacher",
        secondary=association_table,
        back_populates="students"
    )


@app.cli.command()
def init_database():
    db.create_all()
    click.echo("Database had initialized")


@app.before_first_request
def initdb():
    db.create_all()


@app.route("/")
def index():
    form = DeleteForm()
    notes = NotesDatabase.query.all()
    return render_template("index.html", notes=notes, form=form)


@app.route("/NewNotes", methods=["GET", "POST"])
def new_notes():
    note_form = NotesForm()
    if note_form.validate_on_submit():
        body = note_form.body.data
        note = NotesDatabase(body=body)
        db.session.add(note)
        db.session.commit()
        flash("create success!!!")
        return redirect(url_for("index"))
    return render_template("submit.html", note_form=note_form)


@app.route("/update/<int:note_id>", methods=["GET", "POST"])
def update(note_id):
    form = EditForm()
    note = NotesDatabase.query.get(note_id)
    if form.validate_on_submit():
        note.body = form.body.data
        db.session.commit()
        flash("Update success")
        return redirect(url_for("index"))
    form.body.data = note.body
    return render_template("edit.html", form=form)


@app.route("/delete/<int:note_id>", methods=["POST"])
def delete(note_id):
    form = DeleteForm()
    if form.validate_on_submit():
        note = NotesDatabase.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        flash("Your note is deleted")
    else:
        abort(404)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
