"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Business, Visit, Visitor, Device
from admin import setup_admin

from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'leisy' 
jwt = JWTManager(app)
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/token', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    user= Business.query.filter_by(email=email, password= password).first()
    if user is None:
        return jsonify({"msg": "Bad email or password"}), 401
    print (user)

    ret = {
        'jwt': create_jwt(identity=user.id),
        "business_id": user.id,
        
        
        }
    return jsonify(ret), 200



# if __name__ == '__main__':
#     app.run()
@app.route('/render-bar-chart', methods=['GET'])
def get_bar_chart():
    payload = []
    # age sets for loop, tuples with min age and max age for each set
    age_sets = [(18, 29), (30, 39), (40, 49), (50, 59), (60, 64), (65, 69), (70,79), (80,120)]
    # loop to append to payload object with name for age range and data for positives count
    for [min_age, max_age] in age_sets:
        # joined query on Visit table to get has_covid visits
        # first filters by has covid and then applies distinct on visitor_id to
        # count many true visitors visits as one
        # then joins visitors table to filter based on age range
        # then turns base query object to list object through .all()
        positives = db.session.query(Visit.visitor_id.distinct()).filter_by(
            has_covid=True
        ).join(Visit.visitor).filter(
            Visitor.age > min_age,
            Visitor.age <= max_age
        ).all()
        # creates object data for age range
        data = {
            "name": f"{min_age}{'-' if min_age != 85 else '+'}{max_age if min_age != 85 else ''}",
            "positive": len(positives)
        }
        # appends to payload
        payload.append(data)
    return jsonify(payload), 200

@app.route('/business', methods=['GET'])
def get_all_business():
        businessList = Business.query.all()
        payload = list(map(lambda biz: biz.serialize(), businessList))
        return jsonify(payload), 200

@app.route('/visit', methods=['GET'])
def get_all_visit():
        visitList = Visit.query.all()
        payload = list(map(lambda biz: biz.serialize(), visitList))
        return jsonify(payload), 200

@app.route('/visitor/<email>', methods=['GET'])
def get_single_visitor(email):
        visitor_1 = Visitor.query.filter_by(email=email).first()
        if visitor_1 is None:
            return "Not found", 404
        return jsonify(visitor_1.serialize()), 200

@app.route('/visitor', methods=['GET'])
def get_all_visitors():
        visitorsList = Visitor.query.all()
        payload = list(map(lambda biz: biz.serialize(), visitorsList))
        return jsonify(payload), 200

@app.route('/business', methods=['POST'])
def signup_business():
    request_body= request.get_json()
    print(request_body)

    business1 = Business(
        business_name=request_body["business_name"],
        address=request_body["address"],
        phone_number=request_body["phone_number"],
        email=request_body["email"],
        password=request_body["password"],
    )
    db.session.add(business1)
    db.session.commit()
    return jsonify(request_body),200


@app.route('/visit', methods=['POST'])
def signup_visit():
    request_body= request.get_json()
    print(request_body)

    visit1 = Visit(
        temperature=request_body["temperature"],
        business_id=request_body["business_id"],
        visitor_id=request_body["visitor_id"],
        entry_date=datetime.strptime(request_body["entry_date"], "%a, %d %b %Y %H:%M:%S %Z"),
        has_fever=request_body["has_fever"],
        has_covid=request_body["has_covid"],
    )
    db.session.add(visit1)
    db.session.commit()
    return jsonify(visit1.serialize()),200


@app.route('/visitor', methods=['POST'])
def create_new_visitor():
    request_body= request.get_json()
    print(request_body)

    visitor1 = Visitor(
        first_name=request_body["first_name"],
        last_name=request_body["last_name"],
        age=request_body["age"],
        address=request_body["address"],
        phone_number=request_body["phone_number"],
        email=request_body["email"],
    )
    db.session.add(visitor1)
    db.session.commit()
    return jsonify(request_body),200

@app.route('/visitor/<int:visitor_id>', methods=['PUT'])
def update_visitor_info(visitor_id):
        request_body= request.get_json()
        print(request_body)
        visitor_1 = Visitor.query.get(visitor_id)
        visitor_1.email = request_body["email"]
        visitor_1.address=request_body["address"]
        visitor_1.age=request_body["age"]
        db.session.commit()
        return jsonify(visitor_1.serialize()), 200  

@app.route('/business/<int:business_id>', methods=['PUT'])
def update_info(business_id):
        request_body= request.get_json()
        print(request_body)
        business_1 = Business.query.get(business_id)
        business_1.email = request_body["email"]
        db.session.commit()
        return jsonify(business_1.serialize()), 200    
        

@app.route('/business/<int:business_id>', methods=['DELETE'])
def delete_info(business_id):
        request_body= request.get_json()
        print(request_body)
        business_to_delete = Business.query.get(business_id)
        if business_to_delete is None:
            raise APIException('User not found', status_code=404)
        else:
            db.session.delete(business_to_delete)
            db.session.commit()
            return jsonify(business_to_delete.serialize()), 204

@app.route('/temperature', methods=['GET'])
@jwt_required
def get_temperature():
    business_id = get_jwt_identity()
    device = Device.query.filter_by(
        business_id = business_id
    ).one_or_none()
    if device is None:
        return "There is not device for the business", 404 
    else:  
        #here is what we request our raspberry pi in order to take temperature
        temperature = {"temperature":107}
        return jsonify(temperature), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
