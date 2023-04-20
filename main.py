from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, distinct

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(100))

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    artist = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    duration = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@app.route('/names/')
def unique_names():
    count = db.session.query(func.count(distinct(Customer.first_name))).scalar()
    return f'Маємо {count} унікальних імен в таблиці клієнтів'

@app.route('/tracks/')
def total_tracks():
    count = db.session.query(func.count(Track.id)).scalar()
    return f'Маємо {count} треків таблиці треків'

@app.route('/tracks-sec/')
def tracks_duration():
    tracks = Track.query.all()
    output = ""
    for track in tracks:
        output += f"{track.title} ({track.duration} sec)\n"
    return output

if __name__ == '__main__':
    app.run()


