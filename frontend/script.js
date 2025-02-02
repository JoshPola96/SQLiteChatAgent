document.getElementById("queryForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const queryInput = document.getElementById("queryInput").value;
    const outputDiv = document.getElementById("output");
    const generatedSqlElement = document.getElementById("generatedSql");
    const tableHeaders = document.getElementById("tableHeaders");
    const tableBody = document.getElementById("tableBody");

    // Show loading state
    outputDiv.style.display = "none";
    generatedSqlElement.textContent = "Loading...";

    try {
        const response = await fetch("http://localhost:8000/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query: queryInput })
        });

        const data = await response.json();

        if (data.error) {
            generatedSqlElement.textContent = `Error: ${data.error}`;
            outputDiv.style.display = "block";
            return;
        }

        // Display generated SQL query
        generatedSqlElement.textContent = data.sql_query;

        // Clear previous table data
        tableHeaders.innerHTML = "";
        tableBody.innerHTML = "";

        // If there are results, display them
        if (data.results.length > 0) {
            // Create table headers based on the keys in the first result
            const headers = Object.keys(data.results[0]);
            headers.forEach(header => {
                const th = document.createElement("th");
                th.textContent = header;
                tableHeaders.appendChild(th);
            });

            // Create table rows
            data.results.forEach(row => {
                const tr = document.createElement("tr");
                headers.forEach(header => {
                    const td = document.createElement("td");
                    td.textContent = row[header];
                    tr.appendChild(td);
                });
                tableBody.appendChild(tr);
            });
        }

        outputDiv.style.display = "block";

    } catch (error) {
        generatedSqlElement.textContent = `Error: ${error.message}`;
        outputDiv.style.display = "block";
    }
});
