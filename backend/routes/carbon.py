from flask import Blueprint, request, jsonify

carbon_bp = Blueprint('carbon', __name__)

@carbon_bp.route('/carbon', methods=['POST'])
def carbon():

    data = request.get_json()

    monthly_units = data['monthly_units']

    carbon_kg = round(monthly_units * 0.82, 2)

    return jsonify({
        "monthly_units": monthly_units,
        "carbon_kg": carbon_kg
    })