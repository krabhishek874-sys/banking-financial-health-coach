import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Financial Health Coach",layout="wide")

df=pd.read_csv("transactions.csv")
balance=df["Amount"].sum()
expenses=df[df["Amount"]<0]
summary=expenses.groupby("Category")["Amount"].sum().abs()

score=82
savings_potential=int(summary.get("Shopping",0)*0.2+summary.get("Food",0)*0.1)
predicted=balance-(abs(expenses["Amount"].sum())/30)*10

st.title("AI Financial Health Coach")
col1,col2,col3,col4=st.columns(4)
col1.metric("Balance",f"₹{balance:,.0f}")
col2.metric("Health Score",f"{score}/100")
col3.metric("Savings Potential",f"₹{savings_potential:,.0f}")
col4.metric("Predicted Month-End",f"₹{predicted:,.0f}")

fig=px.pie(values=summary.values,names=summary.index,title="Spending Breakdown")
st.plotly_chart(fig,use_container_width=True)

if summary.get("Travel",0)>3000:
    product="Travel Rewards Credit Card"
else:
    product="Fixed Deposit"

st.subheader("Product Recommendation")
st.success(product)

q=st.text_input("Ask a financial question")
if q:
    st.info(f"Based on your transactions, current balance is ₹{balance:,.0f}. Reduce shopping spend to increase savings.")
