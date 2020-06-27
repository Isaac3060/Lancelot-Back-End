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

app = Flask(__name__)
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


#  @app.route('/visit', methods=['GET'])
#  def visit_info():

#     request_body= request.get_json()
#     print(request_body)
#     return jsonify(request_body),200


@app.route('/business', methods=['POST'])
def signup():
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