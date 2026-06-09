from sustainability import calculate_carbon, sustainability_score

units = 650

carbon = calculate_carbon(units)

score = sustainability_score(
    has_led=True,
    has_solar=True,
    efficient_ac=False,
    high_consumption=False
)

print("Carbon Footprint:", carbon, "kg CO2")
print("Sustainability Score:", score)