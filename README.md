# SQL Chat Assistant

## Overview

The **SQL Chat Assistant** is a Python-based web application that helps users interact with a database by converting natural language queries into SQL queries. It uses FastAPI for the backend, along with the BART model to generate SQL queries from user input. The assistant can respond to a variety of SQL-related queries and fetch results from an SQLite database containing employee and department information.

### Supported Queries:

- "Show me all employees in the [department] department."
- "Who is the manager of the [department] department?"
- "List all employees hired after [date]."
- "What is the total salary expense for the [department] department?"

## Hosted Link

You can access the deployed SQL Chat Assistant at the following URL:
- **Chat UI:** [https://sqlitechatagentfront.onrender.com/]([https://sqlitechatagentfront.onrender.com/]) 

## How It Works

The chat assistant uses a **BART-based language model** to generate SQL queries based on user input. Here's a high-level breakdown of the process:

1. **User Query:** A user submits a natural language query (e.g., "Who is the manager of the Sales department?").
2. **SQL Query Generation:** The assistant either:
   - Uses predefined rules to directly convert certain queries into SQL (e.g., "List all employees in [department]").
   - Uses the BART model to generate an SQL query for more complex queries.
3. **SQL Execution:** The generated SQL query is executed on an SQLite database containing employee and department data.
4. **Result Display:** The assistant returns the results (e.g., the manager's name or a list of employees) in a structured format.

If an error occurs, the assistant provides a meaningful message to help users understand and resolve the issue.

## Known Limitations

- None of the open-source models tried so far have been upto par, the model relies on a regex based fall-back mechanism for the requested queries.

## Suggestions for Improvement

- Implement a better open source model that can tackle various ranges of queries effectively.
- Add in more general query cases to fall back on in case of model failure.
