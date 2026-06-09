def calculate_carbon(units):
    return units * 0.82


def sustainability_score(has_led, has_solar, efficient_ac, high_consumption):
    score = 50

    if has_led:
        score += 20

    if has_solar:
        score += 30

    if efficient_ac:
        score += 20

    if high_consumption:
        score -= 20

    return score