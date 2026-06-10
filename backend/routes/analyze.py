from flask import Blueprint, request, jsonify
from db import db
analyze_bp = Blueprint('analyze', __name__)

@analyze_bp.route('/analyze', methods=['POST'])
def analyze():

    data = request.get_json()

    appliance_name = data['appliance']
    quantity = data['quantity']
    hours = data['hours']
    rate = data['rate']
    solar_installed = data['solar_installed']

    appliance = db.appliances.find_one({
        "name": appliance_name
    })

    if not appliance:
        return jsonify({
            "error": "Appliance not found"
        }), 404

    power = appliance['power']

    # Energy calculation
    daily_units = (power * quantity * hours) / 1000
    monthly_units = daily_units * 30

    # Bill calculation
    monthly_bill = round(monthly_units * rate, 2)

    # Solar recommendation
    recommended_solar_kw = round(monthly_units / 120, 2)

    # Carbon footprint
    carbon_kg = round(monthly_units * 0.82, 2)

    # Eco score
    score = 100

    if monthly_units > 1000:
        score -= 30
    elif monthly_units > 500:
        score -= 15

    if solar_installed:
        score += 20

    score = min(score, 100)
    score = max(score, 0)

    return jsonify({
        "appliance": appliance_name,
        "power": power,
        "daily_units": daily_units,
        "monthly_units": monthly_units,
        "monthly_bill": monthly_bill,
        "recommended_solar_kw": recommended_solar_kw,
        "carbon_kg": carbon_kg,
        "eco_score": score
    })