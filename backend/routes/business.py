from flask import Blueprint, request, jsonify
from db import db

business_bp = Blueprint('business', __name__)

@business_bp.route('/business-recommendation', methods=['POST'])
def business_recommendation():

    data = request.get_json()

    business_type = data['type']

    business = db.business_types.find_one({
        "type": business_type
    })

    if not business:
        return jsonify({
            "error": "Business type not found"
        }), 404

    return jsonify({
        "type": business["type"],
        "recommended_appliances": business["recommended_appliances"]
    })