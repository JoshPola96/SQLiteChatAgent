import sqlite3

conn = sqlite3.connect("employees.db")  # Connect to the database
cursor = conn.cursor()

# Show all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in database:", tables)

# Show data inside the tables
print("\nEmployees Table:")
cursor.execute("SELECT * FROM employees;")
print(cursor.fetchall())

print("\nDepartments Table:")
cursor.execute("SELECT * FROM departments;")
print(cursor.fetchall())

conn.close()