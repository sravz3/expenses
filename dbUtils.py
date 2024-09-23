import sqlite3
import pandas as pd
import datetime as dt 

DATABASE_NAME = "expenses.db"

DEFAULT_CATEGORIES = ["Rent", "Utilities", "Groceries"]

cat_list = ""
for i in DEFAULT_CATEGORIES:
    cat_list = cat_list + "(\"" + i + "\"),"

def create_tables():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Add the categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY,
            category TEXT
        )
    ''')
    # Insert some default category values
    cat_query = 'SELECT category FROM category'
    category_list = pd.read_sql_query(cat_query, connection).category.to_list()
    if len(category_list) == 0:
        cursor.execute('INSERT INTO category (category) VALUES ' + cat_list[:-1])

    # Add the expenses table 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            date INTEGER,
            category_id INTEGER,
            amount REAL,
            FOREIGN KEY (category_id) REFERENCES category(id)
        )
    ''')

    connection.commit()
    connection.close()

# create_tables()

def get_category_list():
    connection = sqlite3.connect(DATABASE_NAME) 
    query = '''
        SELECT c.id, c.category
        FROM category c
    '''
    df = pd.read_sql_query(query, connection)   
    connection.close()
    return df.category.tolist()

def save_category(new_choice):
    new_choice = new_choice.title()
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cat_query = 'SELECT category FROM category'
    category_list = pd.read_sql_query(cat_query, connection).category.to_list()

    if new_choice in category_list:
        result = new_choice + " already exists in the list of categories"
    else:
        cursor.execute('INSERT INTO category (category) VALUES (?)', (new_choice,))
        result = new_choice + " added successfully to the list of categories"

    connection.commit()
    connection.close()

    return result

def save_expense(date, category, amount):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('SELECT id FROM category WHERE category = ?', (category,))
    row = cursor.fetchone()
    cat_id = row[0]

    try:
        cursor.execute('INSERT INTO expenses (date, category_id, amount) VALUES (?, ?, ?)', (date, cat_id, amount))
        result='Expense record saved successfully!'
    except:
        result='Oops something is not right. Please check your inputs and try again!'

    connection.commit()
    connection.close()
    
    return result

def get_expenses():
    connection = sqlite3.connect(DATABASE_NAME) 
    query = '''
        SELECT e.date, c.category, e.amount
        FROM expenses e
        LEFT JOIN category c ON c.id = e.category_id
    '''
    df = pd.read_sql_query(query, connection)   
    connection.close()
    return df






