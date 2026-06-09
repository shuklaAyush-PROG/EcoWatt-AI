from flask import Flask, jsonify, request
from routes.energy import energy_bp
from routes.solar import solar_bp
from routes.carbon import carbon_bp
from routes.analyze import analyze_bp
from flask_cors import CORS
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

    with open('../data/appliances.json', 'r') as file:
        data = json.load(file)

    return jsonify(data)

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
