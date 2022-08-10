# app.py
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poetrybingo.sqlite3'
db = SQLAlchemy(app)

db.Model.metadata.reflect(db.engine)

class Headline(db.Model):
    __tablename__ = 'headlines'
    __table_args__ = { 'extend_existing': True }
    LOC_CODE = db.Column(db.Text, primary_key=True)


@app.route("/")
def hello():
    print("Total number of headlines is", Headline.query.count())
    return render_template("index.html")

@app.route("/shoelaces")
def shoelaces():
    return "This works now!"

@app.route("/about")
def about():
    return "All about my website!"

if __name__ == '__main__':
    app.run(debug=True)