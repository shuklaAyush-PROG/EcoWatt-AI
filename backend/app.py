
from flask import Flask, jsonify, request
from flask_cors import CORS


from db import db

from routes.energy import energy_bp
from routes.solar import solar_bp
from routes.carbon import carbon_bp
from routes.analyze import analyze_bp

from routes.solar import (
    recommend_solar,
    predict_generation,
    calculate_savings,
    calculate_payback,
    sustainability_score,
    get_grade,
    generate_recommendations,
    get_system_cost
)
app = Flask(__name__)
CORS(app)
app.register_blueprint(energy_bp)
app.register_blueprint(solar_bp)
app.register_blueprint(carbon_bp)
app.register_blueprint(analyze_bp)
import os


@app.route('/')
def home():
    return "EcoWatt Backend Running"

@app.route('/status')
def status():
    return jsonify({
        "status": "success",
        "message": "Backend working"
    })
@app.route('/appliances')
def appliances():

    data = list(
        db.appliances.find({}, {"_id": 0})
    )

    return jsonify(data)

@app.route('/calculate_by_appliance', methods=['POST'])
def calculate_by_appliance():

    data = request.get_json()

    appliance_name = data['appliance']
    quantity = data['quantity']
    hours = data['hours']

    appliance = db.appliances.find_one(
        {"name": appliance_name},
        {"_id": 0}
    )

    if appliance is None:

        return jsonify({
            "error": "Appliance not found"
        }), 404

    power = appliance["power"]

    daily_units = (power * quantity * hours) / 1000
    monthly_units = daily_units * 30

    return jsonify({
        "appliance": appliance_name,
        "power": power,
        "daily_units": daily_units,
        "monthly_units": monthly_units
    })

@app.route('/bill', methods=['POST'])
def bill():

    data = request.get_json()

    units = data['monthly_units']
    rate = data['rate']

    bill_amount = units * rate

    return jsonify({
        "monthly_bill": bill_amount
    })
@app.route('/solar-analysis', methods=['POST'])
def solar_analysis():

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
@app.route('/carbon', methods=['POST'])
def carbon():

    data = request.get_json()

    monthly_units = data['monthly_units']

    carbon_kg = round(monthly_units * 0.82, 2)

    return jsonify({
        "monthly_units": monthly_units,
        "carbon_kg": carbon_kg
    })

@app.route('/eco_score', methods=['POST'])
def eco_score():

    data = request.get_json()

    monthly_units = data['monthly_units']
    solar_installed = data['solar_installed']

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
        "eco_score": score
    })

@app.route('/business_recommendation', methods=['POST'])
def business_recommendation():

    data = request.get_json()

    business_type = data['type']

    business = db.business_types.find_one(
        {"type": business_type},
        {"_id": 0}
    )

    if business is None:

        return jsonify({
            "error": "Business type not found"
        }), 404

    return jsonify({

        "business_type": business_type,

        "recommended_appliances":
        business["recommended_appliances"]

    })

@app.route('/upload', methods=['POST'])
def upload():

    if 'file' not in request.files:
        return jsonify({
            "error": "No file uploaded"
        }), 400

    file = request.files['file']

    upload_folder = 'uploads'

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filepath = os.path.join(upload_folder, file.filename)

    file.save(filepath)

    return jsonify({
        "message": "File uploaded successfully",
        "filename": file.filename
    })
if __name__ == '__main__':
    app.run(debug=True)
