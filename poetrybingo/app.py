# app.py
from flask import Flask
from flask import render_template
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db':'poetrybingo',
    'host':'localhost',
    'port':'27017'
}

db = MongoEngine(app)

class Headline(db.Document):
    headline = db.StringField(required=True)
    tags = db.StringField()
    timestamp = db.TimeStampField()
    year = db.NumberField()
    month = db.NumberField()
    day = db.NumberField()
    hour = db.NumberField()
    minute = db.NumberField()


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///headlines.sqlite3'
# db = SQLAlchemy(app)

# db.Model.metadata.reflect(db.engine)

# class Headline(db.Model):
#     __tablename__ = 'headlines'
#     __table_args__ = { 'extend_existing': True }
# # It's defining a column in the database.
#     LOC_CODE = db.Column(db.Integer, primary_key=True)

@app.route("/")
def hello():
    # print(f"Total number of headlines is {Headline.query.count()}")
    return render_template("index.html")

@app.route("/shoelaces")
def shoelaces():
    return "This works now!"

@app.route("/about")
def about():
    return "All about my website!"

if __name__ == '__main__':
    app.run(debug=True)