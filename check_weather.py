import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("business_intelligence.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Execute a query to select all data from the weather table
cursor.execute(
    """
    SELECT * FROM weather
    """
)

# Fetch all the results from the executed query
rows = cursor.fetchall()

# Loop through and print each row of data
for row in rows:
    print(row)

# Close the database connection
conn.close()