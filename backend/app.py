from flask import Flask, jsonify, request
import json
app = Flask(__name__)

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

    with open('../data/appliances.json', 'r') as file:
        data = json.load(file)

    return jsonify(data)
@app.route('/calculate', methods=['POST'])
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
@app.route('/calculate_by_appliance', methods=['POST'])
def calculate_by_appliance():

    data = request.get_json()

    appliance_name = data['appliance']
    quantity = data['quantity']
    hours = data['hours']

    with open('../data/appliances.json', 'r') as file:
        appliances = json.load(file)

    power = None

    for appliance in appliances:
        if appliance['name'].lower() == appliance_name.lower():
            power = appliance['power']
            break

    if power is None:
        return jsonify({
            "error": "Appliance not found"
        }), 404

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
@app.route('/solar', methods=['POST'])
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
if __name__ == '__main__':
    app.run(debug=True)
