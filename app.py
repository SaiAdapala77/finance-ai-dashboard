import streamlit as st
import pandas as pd
import plotly.express as px

from modules.data_loader import load_transactions
from modules.advisor import generate_advice
from modules.finance_chat import build_financial_summary
from db import engine

st.set_page_config(page_title="Finance AI Dashboard", layout="wide")

st.title("?? Personal Finance AI Dashboard")

menu = st.sidebar.selectbox(
    "Select Option",
    ["Upload Transactions", "Dashboard"]
)

# ------------------------------------------------
# Upload Section
# ------------------------------------------------

if menu == "Upload Transactions":

    st.subheader("Upload Transaction Excel")

    uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])

    if uploaded_file:

        excel = pd.ExcelFile(uploaded_file)

        all_data = []

        for sheet in excel.sheet_names:
            df_sheet = pd.read_excel(uploaded_file, sheet_name=sheet)
            df_sheet["source"] = sheet
            all_data.append(df_sheet)

        combined = pd.concat(all_data)

        mapped_df = pd.DataFrame()

        mapped_df["transaction_date"] = pd.to_datetime(combined["Date"])
        mapped_df["description"] = combined["Description"]
        mapped_df["amount"] = combined["Amount"]
        mapped_df["category"] = combined["Category"]
        mapped_df["source"] = combined["source"]

        st.subheader("Preview Data")
        st.dataframe(mapped_df)

        if st.button("Save to Database"):

            mapped_df.to_sql(
                "transactions",
                engine,
                if_exists="append",
                index=False
            )

            st.success("Data inserted successfully")


# ------------------------------------------------
# Dashboard
# ------------------------------------------------

if menu == "Dashboard":

    st.subheader("?? Spending Dashboard")

    df = load_transactions()

    if df.empty:
        st.warning("No transactions found. Please upload data first.")
        st.stop()

    df["month"] = pd.to_datetime(df["transaction_date"]).dt.to_period("M").astype(str)

    col1, col2 = st.columns(2)

    # Monthly spending
    monthly = df.groupby("month")["amount"].sum().reset_index()

    fig1 = px.bar(
        monthly,
        x="month",
        y="amount",
        title="Monthly Spending"
    )

    col1.plotly_chart(fig1, use_container_width=True)

    # Category spending
    category = df.groupby("category")["amount"].sum().reset_index()

    fig2 = px.pie(
        category,
        names="category",
        values="amount",
        title="Spending by Category"
    )

    col2.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Top merchants
    merchants = df.groupby("description")["amount"].sum().reset_index()
    merchants = merchants.sort_values("amount", ascending=False).head(10)

    fig3 = px.bar(
        merchants,
        x="amount",
        y="description",
        orientation="h",
        title="Top Spending Merchants"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # AI Spending Advisor
    st.subheader("?? AI Spending Advisor")

    advice = generate_advice(df)

    for a in advice:
        st.info(a)

    st.divider()

    # AI Finance Chat
    st.subheader("?? Ask AI About Your Spending")

    summary = build_financial_summary(df)

    user_question = st.text_input("Ask a question about your spending")

    if user_question:

        response = f"""
Spending Summary:

{summary}

Question: {user_question}

Suggestion:
Try reducing spending in your top categories to improve savings.
"""

        st.success(response)