import sqlite3

def init_db():
    """Initializes the SQLite database with Employees and Departments tables."""
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()

    # Create Employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary INTEGER NOT NULL,
            hire_date TEXT NOT NULL
        )
    """)

    # Create Departments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            manager TEXT NOT NULL
        )
    """)

    # Insert sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO employees (name, department, salary, hire_date)
            VALUES (?, ?, ?, ?)
        """, [
            ("Alice", "Sales", 50000, "2021-01-15"),
            ("Bob", "Engineering", 70000, "2020-06-10"),
            ("Charlie", "Marketing", 60000, "2022-03-20"),
            ("David", "Sales", 55000, "2023-07-01"),
            ("Eva", "Engineering", 80000, "2019-08-15"),
            ("Frank", "Marketing", 62000, "2023-01-10")
        ])

    cursor.execute("SELECT COUNT(*) FROM departments")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO departments (name, manager)
            VALUES (?, ?)
        """, [
            ("Sales", "Alice"),
            ("Engineering", "Bob"),
            ("Marketing", "Charlie")
        ])

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
