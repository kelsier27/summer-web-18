import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir,"bookdatabase.db"))

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=database_file

db=SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

@app.route("/", methods=["GET","POST"])
def home():
	books=None
	if request.form:
		try:
			book = Book(title=request.form.get("title"))
			db.session.add(book)
			db.session.commit()
		except Exception as err:
			print("ERROR: Failed to add book --> Book already in Database")
			print(err)
		# print(request.form)
	books=Book.query.all()
	return render_template("home.html", books=books)

@app.route("/update", methods=["POST"])
def update():
	try:
		newtitle = request.form.get("newtitle")
		oldtitle = request.form.get("oldtitle")
		book = Book.query.filter_by(title=oldtitle).first()
		book.title=newtitle
		db.session.commit()
	except Exception as err:
		print("ERROR: Couldn't update book title --> No change detected")
		print(err)
	return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
	title = request.form.get("title")
	book = Book.query.filter_by(title=title).first()
	db.session.delete(book)
	db.session.commit()
	return redirect("/")


if __name__ == '__main__':
	app.run(debug=True)