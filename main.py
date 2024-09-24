import streamlit as st
import pandas as pd
import sqlite3

import dbUtils as u

st.set_page_config(layout="wide")

u.create_tables()

if 'category' not in st.session_state:
    st.session_state['category'] = ', '.join(u.get_category_list())

# Sidebar with instructions
st.sidebar.title("Expenses App")
st.sidebar.write("**Overview:** This project showcases how to use Streamlit for gathering and analyzing personal expenses. It utilizes SQLite, a user-friendly database system, ideal for small-scale data management.")
st.sidebar.write("**About the Developer:** I'm Alle Sravani, experienced Senior Data Analyst with 6+ years of experience in data analysis, data modeling, and business intelligence. Let's connect on LinkedIn: https://www.linkedin.com/in/alle-sravani/")
st.sidebar.write("**Source Code:** You can access the code on GitHub: https://github.com/sravz3/expenses/tree/main")

t_left, t_right = st.columns([3, 1])

with t_left:
    st.title("Personal Expenses App")
    st.write(""" Enter your expense to be recorded into the system. """)

with t_right:
    # -------------- Download Button------------------ 
    df = u.get_expenses()
    st.download_button(
        label="Download data as CSV",
        data=df.to_csv().encode("utf-8"),
        file_name="expenses.csv",
        mime="text/csv",
    )

def update_value():
    cat_list = u.get_category_list()
    st.session_state.category = ', '.join(cat_list)

b_left, b_right = st.columns([3, 1])

with b_left:
    # ------------ Record Expense and Save -------------------- 
    st.header("Record Expense")

    with st.form("record_form", clear_on_submit=True):
        st.write("Fill in your expense details here")
        f_date = st.date_input("Enter the date", value=None)
        f_category = st.selectbox('Pick a category', u.get_category_list())
        f_amount = st.number_input("Enter amount in $")
        f_submitted = st.form_submit_button('Submit Expense')

    if f_submitted:
        expense_result = u.save_expense(f_date,f_category,f_amount)
        st.success(expense_result)


with b_right:
    st.header("Categories")
    new_choice = st.text_input('Add your own new category:')
    submitted = st.button("Add new category")  

    if submitted:
        category_result = u.save_category(new_choice)
        st.success(category_result)
        update_value()
    # st.session_state['category'] = u.get_entry()

    # ---------- Show Categories --------------------
    st.write("Here are the categories.")
    st.write(st.session_state.category)
