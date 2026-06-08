# EcoWatt AI - Solar Recommendation Logic

---

# 1. Solar Capacity Recommendation

Formula:

Solar Size (kW) =
Monthly Units / (30 × 4)

Assumption:
Average sunlight = 4 peak hours/day

---

# Example

Monthly Consumption = 600 units

Solar Size =
600 / 120

= 5 kW

---

# 2. Solar Installation Cost

Approximate Indian Market Rates:

1 kW  → ₹70,000
2 kW  → ₹1,40,000
3 kW  → ₹2,10,000
5 kW  → ₹3,50,000
10 kW → ₹7,00,000

Formula:

Solar Cost =
Solar Size × ₹70,000

---

# Example

5 kW × ₹70,000

= ₹3,50,000

---

# 3. Annual Electricity Cost Without Solar

Formula:

Annual Electricity Cost =
Monthly Bill × 12

Example:

₹5000 × 12

= ₹60,000/year

---

# 4. Estimated Annual Savings With Solar

Assumption:
Solar reduces 85% electricity bill.

Formula:

Annual Savings =
Annual Electricity Cost × 0.85

Example:

₹60,000 × 0.85

= ₹51,000/year

---

# 5. Solar Payback Period

Formula:

Payback Period =
Solar Installation Cost / Annual Savings

Example:

₹3,50,000 / ₹51,000

≈ 6.8 years

---

# 6. 5-Year Savings Estimation

Formula:

5-Year Savings =
Annual Savings × 5

Example:

₹51,000 × 5

= ₹2,55,000

---

# 7. Recommendation Rules

If Monthly Units < 150
→ Solar Optional

If Monthly Units between 150–400
→ Recommend 2–3 kW Solar

If Monthly Units between 400–800
→ Recommend 3–5 kW Solar

If Monthly Units > 800
→ Strongly Recommend Solar

---

# 8. Sustainability Impact

Approximation:

1 unit electricity =
0.82 kg CO₂

Solar reduces CO₂ emission significantly.

Example:

600 units/month

600 × 0.82

= 492 kg CO₂/month
