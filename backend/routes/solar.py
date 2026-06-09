from flask import Blueprint, request, jsonify

solar_bp = Blueprint('solar', __name__)

@solar_bp.route('/solar', methods=['POST'])
def solar():

    data = request.get_json()

    monthly_units = data['monthly_units']

    recommended_kw = round(monthly_units / 120, 2)

    monthly_savings = round(monthly_units * 7, 2)
    annual_savings = round(monthly_savings * 12, 2)

    return jsonify({
        "monthly_units": monthly_units,
        "recommended_solar_kw": recommended_kw,
        "estimated_monthly_savings": monthly_savings,
        "estimated_annual_savings": annual_savings
    })