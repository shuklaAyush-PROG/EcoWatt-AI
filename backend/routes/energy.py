from flask import Blueprint, request, jsonify
from db import db

energy_bp = Blueprint('energy', __name__)


# Route to get all appliances
@energy_bp.route('/appliances', methods=['GET'])
def appliances():

    appliances_data = list(
        db.appliances.find({}, {"_id": 0})
    )

    return jsonify(appliances_data)


# Route to calculate electricity usage
@energy_bp.route('/calculate', methods=['POST'])
def calculate():

    data = request.get_json()

    appliance_name = data['appliance']
    quantity = data['quantity']
    hours = data['hours']

    # Fetch appliance from MongoDB
    appliance_data = db.appliances.find_one({
        "name": appliance_name
    })

    # If appliance not found
    if not appliance_data:
        return jsonify({
            "error": "Appliance not found"
        }), 404

    power = appliance_data['power']

    # Calculate units
    daily_units = (power * quantity * hours) / 1000

    monthly_units = daily_units * 30

    yearly_units = monthly_units * 12

    return jsonify({

        "appliance": appliance_name,
        "power": power,

        "daily_units": round(daily_units, 2),

        "monthly_units": round(monthly_units, 2),

        "yearly_units": round(yearly_units, 2)

    })