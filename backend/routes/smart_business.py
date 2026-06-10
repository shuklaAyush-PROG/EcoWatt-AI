from flask import Blueprint, request, jsonify
from db import db

smart_business_bp = Blueprint('smart_business', __name__)

@smart_business_bp.route('/smart-business-energy', methods=['POST'])
def smart_business_energy():

    print("SMART BUSINESS ROUTE HIT")

    data = request.get_json()
    rate = data.get('rate', 8)
    print("INPUT DATA:", data)

    business_type = data['type']

    # 1. Get business recommendation
    business = db.business_types.find_one({"type": business_type})

    if not business:
        return jsonify({"error": "Business type not found"}), 404

    appliances = business.get("recommended_appliances", [])

    # 2. Fetch power for each appliance
    total_power = 0
    detailed_appliances = []

    for name in appliances:
        appliance = db.appliances.find_one({"name": name})

        if appliance:
            power = appliance.get("power", 0)
            total_power += power

            detailed_appliances.append({
                "name": name,
                "power": power
            })

    # Assume average usage = 4 hours/day
    daily_units = (total_power * 4) / 1000
    monthly_units = daily_units * 30
    monthly_bill = round(monthly_units * rate, 2)
    # Solar recommendation logic
    solar_kw = round(monthly_units / 120, 2)
    response = {
        "type": business_type,
        "appliances": detailed_appliances,
        "total_power_watts": total_power,
        "monthly_units": round(monthly_units, 2),
        "monthly_bill": monthly_bill,
        "recommended_solar_kw": solar_kw
    }

    print(response)  # debug
    print("TOTAL POWER =", total_power)  # debug

    return jsonify(response)