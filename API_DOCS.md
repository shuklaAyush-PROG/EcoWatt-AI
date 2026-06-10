# EcoWatt AI APIs

## 1. Appliances API

GET /appliances

Returns appliance list.


## 2. Bill API

POST /bill

Body:
{
  "monthly_units": 500,
  "rate": 7
}

Response:
{
  "monthly_bill": 3500
}