#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(page_title='Personal Finance', page_icon='💰', layout="wide")




def main():
    # Create a sidebar with navigation options
    page = st.sidebar.radio("Select a page", ["Net Worth", "Portfolio", "Budget"])
    
    # Display content based on the selected page
    if page == "Net Worth":
        net_worth()
    elif page == "Portfolio":
        portfolio()
    elif page == "Budget":
        budget()

    




def net_worth():
    
    st.title('Net Worth Calculator')

    st.sidebar.header('User Input')

    assets = st.sidebar.number_input('Total Assets', value=0)
    liabilities = st.sidebar.number_input('Total Liabilities', value=0)
    
    net_worth = assets - liabilities
    
    st.write(f"### Your Current Net Worth: ${net_worth:,.2f}")
    
    st.sidebar.header('Net Worth Goal')
    net_worth_goal = st.sidebar.number_input('Set Your Net Worth Goal', value=1)
    
    progress_percentage = (net_worth / net_worth_goal) * 100
    
    if net_worth_goal > 0:
        st.write(f"### Progress Towards Net Worth Goal: {progress_percentage:.2f}%")
    
    
    net_worth_data = pd.DataFrame({
        'category': ['Current Net Worth', 'Net Worth Goal', 'Assets', 'Liabilities'],
        'amount': [net_worth, net_worth_goal, assets, liabilities]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        net_worth_chart = px.bar(net_worth_data, x='category', y='amount', color='category')
        
        st.plotly_chart(net_worth_chart)
    
    with col2:
        
        net_worth_data_2 = pd.DataFrame({
            'category': ['Current Net Worth', 'Remaining to Goal'],
            'amount': [net_worth, net_worth_goal - net_worth]
        })
        
        net_worth_chart_2 = px.bar(net_worth_data_2, x='category', y='amount', color='category')
        
        st.plotly_chart(net_worth_chart_2)
    
    
    
    # Additional tips or information
    st.info("💡 Tip: Regularly update your assets, liabilities, and goals to track your financial progress.")
    
    # Disclaimer
    st.warning("This calculator is a simple example for educational purposes. Consult with financial professionals for personalized advice.")
    
    # Note to users
    st.write("Feel free to input your financial details on the sidebar, set goals, and track your net worth journey!")


# Function to calculate portfolio growth
def calculate_portfolio_growth(investments):
    portfolio_value = investments.cumsum()
    return portfolio_value


def portfolio():
       st.title("Investment Portfolio Visualization App")

       # Input form
       st.sidebar.header("Input Your Investments")
       initial_investment = st.sidebar.number_input("Initial Investment Amount", min_value=0, step=1000)
       investment_date = st.sidebar.date_input("Date of Investment", pd.to_datetime("today"))
    
       # User inputs for investment data
       st.header("Enter Your Investment Data")
       investment_data = st.text_area("Enter your investment data (comma-separated):")
    
       if investment_data:
           investments = pd.Series([initial_investment] + [float(x.strip()) for x in investment_data.split(",")])
           
           investments.index = pd.date_range(start=investment_date, periods=len(investments), freq='M')
           
           
           col1,col2=st.columns(2)
           
           with col1:
               # Portfolio visualization with Plotly
               fig = px.line(x=investments.index, y=calculate_portfolio_growth(investments), labels={"y": "Portfolio Value"}, title="Portfolio Growth Over Time")
               fig.update_xaxes(title_text="Date")
               fig.update_yaxes(title_text="Portfolio Value")
        
               st.plotly_chart(fig)
           with col2:
               # Display investment details
               st.subheader("Investment Details")
               st.write("Initial Investment Amount:", initial_investment)
               st.write("Date of Initial Investment:", investment_date)
               st.write("Investment Data:")
               st.dataframe(investments.reset_index().rename(columns={"index": "Date", 0: "Investment"}))
       else:
           st.warning("Please enter your investment data.")


def categorize_expenses(amount):
    if amount > 0:
        return "Income"
    else:
        return "Expense"
    
def budget():
    st.title("Budgeting Tool")

    # Input form
    st.sidebar.header("Enter Your Financial Data")
    income = st.sidebar.number_input("Monthly Income", min_value=0, step=1000)
    expenses = st.sidebar.text_area("Monthly Expenses (comma-separated)", "Rent,Utilities,Groceries,Entertainment")

    # Process expense data
    expense_list = [x.strip() for x in expenses.split(",")]
    expense_amounts = {expense: st.sidebar.number_input(f"{expense} Expense", min_value=0, step=10) for expense in expense_list}

    # Create a DataFrame for visualization
    data = {'Category': [], 'Amount': []}
    for expense, amount in expense_amounts.items():
        data['Category'].append(expense)
        data['Amount'].append(amount)

    df = pd.DataFrame(data)
    
    col1, col2 = st.columns(2)
    with col1:
        # Visualization with Plotly
        fig = px.pie(df, values='Amount', names='Category', title='Expense Distribution')
        st.plotly_chart(fig)
    with col2:
        # Display financial summary
        st.header("Financial Summary")
        st.write("Monthly Income:", income)
        st.write("Monthly Net:", income - df['Amount'].sum())
        st.write("Monthly Expenses:")
        st.dataframe(df)




if __name__ == "__main__":
    main()   
