import pandas as pd

def build_financial_summary(df):

    total_spend = df["amount"].sum()

    category = df.groupby("category")["amount"].sum().sort_values(ascending=False)

    top_categories = category.head(5).to_dict()

    summary = f"""
    Total Spending: ?{round(total_spend,2)}

    Top Categories:
    """

    for k,v in top_categories.items():
        summary += f"{k}: ?{round(v,2)}\n"

    return summary