from profile import profile

def calculate_financial_health():

    income = profile["monthly_income"]

    car_emi = profile["car_emi"]
    rent = profile["house_rent"]

    health_insurance = profile["health_insurance_6m"] / 6
    car_insurance = profile["car_insurance_year"] / 12

    fixed_expenses = car_emi + rent + health_insurance + car_insurance

    remaining = income - fixed_expenses

    emi_ratio = car_emi / income
    savings_ratio = remaining / income

    score = 10

    if emi_ratio > 0.4:
        score -= 3
    elif emi_ratio > 0.3:
        score -= 2

    if savings_ratio < 0.2:
        score -= 3
    elif savings_ratio < 0.3:
        score -= 1

    return {
        "income": income,
        "fixed": fixed_expenses,
        "remaining": remaining,
        "emi_ratio": round(emi_ratio * 100,2),
        "savings_ratio": round(savings_ratio * 100,2),
        "score": round(score,1)
    }