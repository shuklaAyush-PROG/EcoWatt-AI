from flask import Blueprint, request, jsonify
from db import db

solar_bp = Blueprint('solar', __name__)

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

    # Find closest larger/equal system
    solar_data = db.solar_pricing.find().sort("size_kw", 1)

    for item in solar_data:

        if round(solar_size) == item["size_kw"]:
            return item["price"]

    # Fallback if larger than available DB sizes
    return round(solar_size * 65000)


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

    score = (
        (solar_size * 15)
        + (roof_size / 50)
    )

    return min(100, round(score))


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


# ==========================
# Solar Route
# ==========================

@solar_bp.route('/solar', methods=['POST'])
def solar():

    data = request.get_json()

    city = data['city']
    roof = data['roofSize']
    usage = data['monthlyUsage']
    rate = data['electricityRate']

    solar_size = recommend_solar(
        roof,
        usage
    )

    generation = predict_generation(
        solar_size,
        city
    )

    savings = calculate_savings(
        generation,
        rate
    )

    system_cost = get_system_cost(
        solar_size
    )

    payback = calculate_payback(
        system_cost,
        savings["annual"]
    )

    score = sustainability_score(
        solar_size,
        roof
    )

    grade = get_grade(score)

    recommendations = generate_recommendations(
        usage
    )

    return jsonify({

        "solarSize": solar_size,

        "monthlyGeneration": generation,

        "monthlySavings": savings["monthly"],

        "annualSavings": savings["annual"],

        "systemCost": system_cost,

        "paybackYears": payback,

        "score": score,

        "grade": grade,

        "recommendations": recommendations

    })