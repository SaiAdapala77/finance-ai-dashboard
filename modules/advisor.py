import pandas as pd

def generate_advice(df):

    advice = []

    # Remove transfers (not real spending)
    spend_df = df[~df["category"].str.lower().isin(["transfer"])]

    total_spend = spend_df["amount"].sum()

    category_spend = spend_df.groupby("category")["amount"].sum().sort_values(ascending=False)

    top_category = category_spend.index[0]
    top_amount = category_spend.iloc[0]

    advice.append(f"Your highest spending category is {top_category} with ?{round(top_amount,2)}")

    if top_category.lower() == "dining":
        advice.append("Dining expenses are high. Reducing by 30% could save significant money yearly.")

    if top_category.lower() == "shopping":
        advice.append("Shopping appears to be your biggest expense. Consider limiting impulse purchases.")

    if top_category.lower() == "entertainment":
        advice.append("Entertainment spending is high. Try setting a monthly limit.")

    savings_estimate = total_spend * 0.15

    advice.append(f"If you reduce discretionary spending by 15%, you could save ?{round(savings_estimate,2)}")

    return advice