"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask_admin.contrib.sqla import ModelView
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Business, Visit, Visitor
from admin import setup_admin
<<<<<<< HEAD
from flask_jwt_simple import JWTManager, jwt_required, create_jwt, get_jwt_identity
=======
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)
app.config['JWT_SECRET_KEY'] = 'super-secret'  
jwt = JWTManager(app)
>>>>>>> 080089702edf8ea0d036a67a1e4813f3d33c1b1e
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get ('jwt_secret_key')  
jwt = JWTManager(app)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

<<<<<<< HEAD
@app.route('/token', methods=['POST'])    
=======
@app.route('/login', methods=['POST'])
>>>>>>> 080089702edf8ea0d036a67a1e4813f3d33c1b1e
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

    ret = {
        'jwt': create_jwt(identity=user.id),
        "business_id": user.id
        }
    return jsonify(ret), 200

<<<<<<< HEAD
# @app.route('/protected', methods=['GET'])
# @jwt_required
# def protected():
#     Access the identity of the current user with get_jwt_identity
#     return jsonify({'hello_from': get_jwt_identity()}), 200
=======
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    return jsonify({'hello_from': get_jwt_identity()}), 200
>>>>>>> 080089702edf8ea0d036a67a1e4813f3d33c1b1e

# if __name__ == '__main__':
#     app.run()


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

@app.route('/visitor', methods=['GET'])
def get_all_visitor():
        visitorList = Visitor.query.all()
        payload = list(map(lambda biz: biz.serialize(), visitorList))
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
        image=request_body["image"],
        business_id=request_body["business_id"],
        visitor_id=request_body["visitor_id"],
        entry_date=request_body["entry_date"],
        has_fever=request_body["has_fever"],
        has_covid=request_body["has_covid"],
    )
    db.session.add(visit1)
    db.session.commit()
    return jsonify(request_body),200


@app.route('/visitor', methods=['POST'])
def signup_visitor():
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

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)