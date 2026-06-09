# EcoWatt AI - Calculation Logic

---

# 1. Daily Electricity Consumption

Formula:

Units (kWh/day) =
(Power × Quantity × Hours Used) / 1000

Where:

* Power = Appliance watt rating
* Quantity = Number of appliances
* Hours Used = Daily usage hours

Example:

2 Air Conditioners
Power = 1500W
Hours = 8

Calculation:

(1500 × 2 × 8) / 1000

= 24 kWh/day

---

# 2. Monthly Electricity Consumption

Formula:

Monthly Units =
Daily Units × 30

Example:

24 × 30

= 720 kWh/month

---

# 3. Yearly Electricity Consumption

Formula:

Yearly Units =
Monthly Units × 12

Example:

720 × 12

= 8640 kWh/year

---

# 4. Electricity Bill Calculation

Formula:

Electricity Bill =
Monthly Units × Electricity Rate

Example:

720 units
Rate = ₹7/unit

720 × 7

= ₹5040/month

---

# 5. Solar System Recommendation

Formula:

Required Solar Capacity (kW) =
Monthly Units / (30 × 4)

Assumption:
Average 4 sunlight hours/day.

Example:

720 / 120

= 6 kW Solar System

---

# 6. Solar Installation Cost

Approximate Formula:

Solar Cost =
Solar Size × ₹70,000

Example:

6 × 70,000

= ₹4,20,000

---

# 7. Annual Savings With Solar

Formula:

Annual Savings =
Monthly Bill × 12

Example:

₹5040 × 12

= ₹60,480/year

---

# 8. Solar Payback Period

Formula:

Payback Period =
Solar Installation Cost / Annual Savings

Example:

₹4,20,000 / ₹60,480

≈ 7 years

---

# 9. Carbon Footprint Calculation

Formula:

CO₂ Emission =
Monthly Units × 0.82

Assumption:
1 kWh ≈ 0.82 kg CO₂

Example:

720 × 0.82

= 590.4 kg CO₂/month

---

# 10. Sustainability Score Logic

Scoring Rules:

+20 → LED Lighting
+20 → BLDC Fans
+20 → Inverter AC
+30 → Solar Installed
-20 → High Consumption (>1000 units)

Maximum Score:
100

Example:

LED + BLDC + Solar

20 + 20 + 30

= 70/100
