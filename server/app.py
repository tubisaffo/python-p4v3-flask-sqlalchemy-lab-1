# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthuake = Earthquake.query.filter(Earthquake.id == id).first()

    if earthuake:
        body = earthuake.to_dict()
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404

    return make_response(body, status)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    earthquake_list = [earthquake.to_dict() for earthquake in earthquakes]
    
    body = {
        'count': len(earthquake_list),
        'quakes': earthquake_list
    }
    
    return make_response(body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
