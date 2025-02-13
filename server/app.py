from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>Earthquake API</h1>'

@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    
    if earthquake:
        return jsonify({
            "id": earthquake.id,
            "magnitude": earthquake.magnitude,
            "location": earthquake.location,
            "year": earthquake.year
        }), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(
        Earthquake.magnitude >= magnitude
    ).all()
    
    earthquake_list = []
    for quake in earthquakes:
        quake_dict = {
            "id": quake.id,
            "magnitude": quake.magnitude,
            "location": quake.location,
            "year": quake.year
        }
        earthquake_list.append(quake_dict)
    
    response_body = {
        "count": len(earthquake_list),
        "quakes": earthquake_list
    }
    
    return jsonify(response_body), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)