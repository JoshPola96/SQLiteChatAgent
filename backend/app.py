from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(title="SQL Chat Assistant")

# Allow all origins for simplicity (can restrict to specific origins later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load the BART model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large")

class QueryRequest(BaseModel):
    query: str

def process_query(query: str) -> str:
    """Generate SQL query using BART."""
    # Shortened schema for better comprehension
    prompt = f"""
    You are an SQL expert. Given the following table structures:
    - employees(id, name, department, salary, hire_date)
    - departments(id, name, manager)

    Write an SQL query for the following question:
    Question: {query}
    SQL Query:
    """

    # Tokenize the input
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)

    # Generate SQL query
    outputs = model.generate(**inputs)

    # Decode the generated sequence
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Clean up the result to remove extra text and ensure proper SQL format
    result = result.split("SQL Query:")[-1].strip()

    return result

def validate_query(query: str) -> str:
    """Handle manual answers for known queries and validate input."""
    
    # Handle "Show me all employees in the [department]" query
    match_department = re.search(r"show me all employees (?:in|from) the (\w+)(?: department)?", query, re.IGNORECASE)
    if match_department:
        department = match_department.group(1).strip().lower()
        return f"SELECT name FROM employees WHERE department LIKE '{department}';"

    # Handle "Who is the manager of the [department]" query
    match_manager = re.search(r"who is the manager (?:of|for) the (\w+)(?: department)?", query, re.IGNORECASE)
    if match_manager:
        department = match_manager.group(1).strip().lower()
        return f"SELECT manager FROM departments WHERE name LIKE '{department}';"

    # Handle "List all employees hired after [date]" query
    match_date = re.search(r"list all employees (?:hired|joined) after (\d{4}-\d{2}-\d{2})", query, re.IGNORECASE)
    if match_date:
        try:
            date = datetime.strptime(match_date.group(1).strip(), "%Y-%m-%d")
            return f"SELECT name FROM employees WHERE hire_date > '{date}';"
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD format."
    
    # Handle "What is the total salary expense for the [department]" query
    match_salary = re.search(r"what is the total salary expense (?:for|of) the (\w+)(?: department)?", query, re.IGNORECASE)
    if match_salary:
        department = match_salary.group(1).strip().lower()
        return f"SELECT SUM(salary) FROM employees WHERE department LIKE '{department}';"

    # Handle edge cases for variations like "employees from [department]" or "department [department]"
    match_edge_case = re.search(r"employees (?:from|of) the (\w+)(?: department)?", query, re.IGNORECASE)
    if match_edge_case:
        department = match_edge_case.group(1).strip().lower()
        return f"SELECT name FROM employees WHERE department LIKE '{department}';"

    return None

@app.post("/ask")
async def ask_database(request: QueryRequest):
    try:
        # First, try to validate and return a known SQL query
        sql_query = validate_query(request.query)

        if not sql_query:
            # If not a known query, use the BART model to generate a query
            sql_query = process_query(request.query)
        
        # Execute query (add basic validation before executing)
        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()

        # Ensure the SQL query is valid before executing
        try:
            cursor.execute(sql_query)
        except sqlite3.Error as e:
            return {
                "error": f"Invalid SQL query: {str(e)}",
                "generated_sql": sql_query
            }

        # Get column names and results
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        
        # Format results as list of dictionaries
        formatted_results = [
            dict(zip(columns, row))
            for row in results
        ]
        
        conn.close()
        
        # Return formatted response with the SQL query and results
        return {
            "question": request.query,
            "sql_query": sql_query,
            "results": formatted_results
        }
        
    except sqlite3.Error as e:
        return {
            "error": f"Database error: {str(e)}",
            "generated_sql": sql_query
        }
    except Exception as e:
        return {
            "error": str(e),
            "generated_sql": sql_query if 'sql_query' in locals() else None
        }

@app.get("/")
def read_root():
    return {
        "message": "Welcome to SQL Chat Assistant",
        "usage": "Send a POST request to /ask with your question",
        "example_queries": [
            "Who is the highest paid employee?",
            "Show me the total salary by department",
            "List all employees in Sales",
            "Who are the department managers?"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
