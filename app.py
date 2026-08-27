import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Financial Health Coach",
    page_icon="🏦",
    layout="wide"
)

# -----------------------------
# CUSTOM STYLING
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f8fc;
}

div[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #e6e6e6;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

h1 {
    color: #003366;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# CUSTOMER PROFILES
# -----------------------------

customer_profiles = {
    "Abhishek (Traveler)": {
        "balance": 80000,
        "travel": 12000,
        "shopping": 6000
    },
    "Priya (Saver)": {
        "balance": 150000,
        "travel": 2000,
        "shopping": 3000
    },
    "Ravi (Shopper)": {
        "balance": 60000,
        "travel": 1000,
        "shopping": 15000
    }
}

st.title("🏦 AI Financial Health Coach")

selected_customer = st.selectbox(
    "Select Customer",
    list(customer_profiles.keys())
)

profile = customer_profiles[selected_customer]

# -----------------------------
# LOAD TRANSACTION DATA
# -----------------------------

df = pd.read_csv("transactions.csv")

expenses = df[df["Amount"] < 0]

summary = (
    expenses.groupby("Category")["Amount"]
    .sum()
    .abs()
)

# Override values based on customer

travel = profile["travel"]
shopping = profile["shopping"]
balance = profile["balance"]

# -----------------------------
# FINANCIAL HEALTH SCORE
# -----------------------------

score = 100

if shopping > 10000:
    score -= 15

if travel > 10000:
    score -= 5

if balance < 50000:
    score -= 20

if score < 0:
    score = 0

# -----------------------------
# SAVINGS POTENTIAL
# -----------------------------

savings_potential = int(
    shopping * 0.20 +
    travel * 0.10
)

# -----------------------------
# CASHFLOW FORECAST
# -----------------------------

days = list(range(1, 11))

forecast = []

for day in days:
    forecast.append(balance - (day * 1500))

predicted_balance = forecast[-1]

# -----------------------------
# DASHBOARD METRICS
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current Balance",
        f"₹{balance:,.0f}"
    )

with col2:
    st.metric(
        "Health Score",
        f"{score}/100"
    )

with col3:
    st.metric(
        "Savings Potential",
        f"₹{savings_potential:,.0f}"
    )

with col4:
    risk = "Low" if score > 75 else "Medium"
    st.metric(
        "Risk Level",
        risk
    )

st.divider()

# -----------------------------
# SPENDING CHART
# -----------------------------

left, right = st.columns(2)

with left:

    spending_chart = pd.DataFrame({
        "Category": [
            "Rent",
            "Food",
            "Shopping",
            "Travel",
            "Utilities"
        ],
        "Amount": [
            18000,
            5000,
            shopping,
            travel,
            2000
        ]
    })

    fig = px.pie(
        spending_chart,
        values="Amount",
        names="Category",
        title="Spending Breakdown"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------
# CASHFLOW FORECAST
# -----------------------------

with right:

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=days,
            y=forecast,
            mode="lines+markers",
            name="Forecast"
        )
    )

    fig2.update_layout(
        title="Month-End Cashflow Forecast",
        xaxis_title="Days",
        yaxis_title="Balance (₹)"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

# -----------------------------
# PRODUCT RECOMMENDATION
# -----------------------------

st.subheader("🎯 Personalized Product Recommendation")

if travel > 5000:

    product = "Travel Rewards Credit Card"

    reason = """
    Customer has significant travel spend.
    Earn reward points and airport lounge access.
    """

elif balance > 100000:

    product = "Premium Fixed Deposit"

    reason = """
    Customer maintains high savings balance.
    Suitable for wealth growth and fixed returns.
    """

else:

    product = "Smart Savings Account"

    reason = """
    Improve savings discipline and earn higher interest.
    """

st.success(product)

st.info(reason)

st.divider()

# -----------------------------
# FRAUD DETECTION
# -----------------------------

st.subheader("🛡 Fraud Detection")

avg_txn = 5000

max_txn = 18000

if max_txn > avg_txn * 3:

    st.warning(
        f"""
    
