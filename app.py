# app.py
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poetrybingo.sqlite3'
db = SQLAlchemy(app)

db.Model.metadata.reflect(db.engine)

class Headline(db.Model):
    __tablename__ = 'headlines'
    __table_args__ = { 'extend_existing': True }
    LOC_CODE = db.Column(db.Text, primary_key=True)



@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print(request.form.get('hallo'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)