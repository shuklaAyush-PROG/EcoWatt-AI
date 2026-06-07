from flask import Flask, jsonify, request

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
@app.route('/bill', methods=['POST'])
def bill():

    data = request.get_json()

    units = data['monthly_units']
    rate = data['rate']

    bill_amount = units * rate

    return jsonify({
        "monthly_bill": bill_amount
    })
if __name__ == '__main__':
    app.run(debug=True)