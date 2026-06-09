from flask import Blueprint, request, jsonify

energy_bp = Blueprint('energy', __name__)

@energy_bp.route('/calculate', methods=['POST'])
def calculate():

    data = request.get_json()

    power = data['power']
    quantity = data['quantity']
    hours = data['hours']

    daily_units = (power * quantity * hours) / 1000
    monthly_units = daily_units * 30
    yearly_units = monthly_units * 12

    return jsonify({
        "daily_units": daily_units,
        "monthly_units": monthly_units,
        "yearly_units": yearly_units
    })