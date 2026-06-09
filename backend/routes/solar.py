from flask import Blueprint, request, jsonify

solar_bp = Blueprint('solar', __name__)
import json

# ==========================
# Solar Recommendation
# ==========================

def recommend_solar(roof_size, monthly_usage):
    required_kw = monthly_usage / 120
    max_kw = roof_size / 100

    return round(min(required_kw, max_kw), 2)


# ==========================
# City Factors
# ==========================

CITY_FACTOR = {
    "Delhi": 1.00,
    "Chandigarh": 0.95,
    "Jaipur": 1.10,
    "Mumbai": 0.90,
    "Bengaluru": 0.92
}


# ==========================
# Solar Price Lookup
# ==========================

def get_system_cost(solar_size):

    try:

        with open("database/solar_prices.json", "r") as file:
            prices = json.load(file)

        closest_price = prices[-1]["price"]

        for item in prices:

            if solar_size <= item["size_kw"]:
                closest_price = item["price"]
                break

        return closest_price

    except Exception:

        return solar_size * 50000


# ==========================
# Generation Prediction
# ==========================

def predict_generation(solar_size, city):

    factor = CITY_FACTOR.get(city, 1.0)

    generation = solar_size * 120 * factor

    return round(generation, 2)


# ==========================
# Savings Calculation
# ==========================

def calculate_savings(generation, rate):

    monthly = generation * rate

    annual = monthly * 12

    return {
        "monthly": round(monthly, 2),
        "annual": round(annual, 2)
    }


# ==========================
# Payback Calculation
# ==========================

def calculate_payback(system_cost, annual_savings):

    if annual_savings == 0:
        return 0

    return round(system_cost / annual_savings, 2)


# ==========================
# Sustainability Score
# ==========================

def sustainability_score(solar_size, roof_size):

    return min(
        100,
        round(
            (solar_size * 15)
            + (roof_size / 50)
        )
    )


# ==========================
# Sustainability Grade
# ==========================

def get_grade(score):

    if score >= 80:
        return "Excellent"

    elif score >= 60:
        return "Good"

    elif score >= 40:
        return "Average"

    return "Poor"


# ==========================
# Recommendations
# ==========================

def generate_recommendations(monthly_usage):

    recommendations = []

    if monthly_usage > 500:
        recommendations.append(
            "Shift heavy appliances to daytime"
        )

    recommendations.append(
        "Run washing machine between 11 AM and 3 PM"
    )

    recommendations.append(
        "Avoid peak usage from 6 PM to 10 PM"
    )

    recommendations.append(
        "Charge EV during daylight hours"
    )

    return recommendations

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