# app.py
from flask import Flask, render_template
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
    headline_count = Headline.query.count()
    all_headlines = Headline.query.all()
    return render_template("index.html", count=headline_count, headlines=all_headlines)

@app.route("/headlines/<slug>")
def detail(slug):
    headline = Headline.query.filter_by(LOC_CODE=slug).first()
    return render_template("detail.html", headline=headline)


if __name__ == '__main__':
    app.run(debug=True)