from fastapi import APIRouter

router = APIRouter()

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

def sustainability_score(
    solar_size,
    roof_size
):

    score = min(
        100,
        round(
            (solar_size * 15)
            + (roof_size / 50)
        )
    )

    return score


# ==========================
# Recommendations
# ==========================

def generate_recommendations(
    monthly_usage
):

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
# API Route
# ==========================

@router.post("/solar-analysis")
def solar_analysis(data: dict):

    city = data["city"]

    roof = data["roofSize"]

    usage = data["monthlyUsage"]

    rate = data["electricityRate"]


    # Solar Size
    solar = recommend_solar(
        roof,
        usage
    )


    # Generation
    generation = predict_generation(
        solar,
        city
    )


    # Savings
    savings = calculate_savings(
        generation,
        rate
    )


    # System Cost
    system_cost = solar * 50000


    # Payback
    payback = calculate_payback(
        system_cost,
        savings["annual"]
    )


    # Sustainability Score
    score = sustainability_score(
        solar,
        roof
    )


    # Recommendations
    recommendations = generate_recommendations(
        usage
    )


    return {

        "solarSize": solar,

        "monthlyGeneration": generation,

        "monthlySavings":
            savings["monthly"],

        "annualSavings":
            savings["annual"],

        "paybackYears":
            payback,

        "score":
            score,

        "recommendations":
            recommendations
    }

