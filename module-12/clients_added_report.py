import mysql.connector
from mysql.connector import errorcode
import sys

def connect_to_database(config):
    """
    Connect to the MySQL database using the provided configuration.

    Args:
        config (dict): Database configuration parameters.

    Returns:
        tuple: A tuple containing the database connection and cursor objects.
    """
    try:
        connection = mysql.connector.connect(**config)
        print("Connected to the database successfully.")
        # Use dictionary=True to fetch rows as dictionaries
        cursor = connection.cursor(dictionary=True)
        return connection, cursor
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Invalid username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist.")
        else:
            print(f"Error: {err}")
        sys.exit(1)  # Exit the script with an error status

def report_clients_added(cursor):
    """
    Fetch and display the number of clients added in the last six months.

    Args:
        cursor (mysql.connector.cursor.MySQLCursorDict): Database cursor.
    """
    print("\n--- Clients Added in the Last Six Months ---\n")
    
    query = """
        SELECT 
            DATE_FORMAT(ClientCreationDate, '%Y-%m') AS Month,
            COUNT(ClientID) AS NewClients
        FROM Clients
        WHERE ClientCreationDate >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        GROUP BY Month
        ORDER BY Month ASC;
    """
    
    try:
        # Execute the query
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if not rows:
            print("No client data found in the last six months.")
            return
        
        # Display the results
        header = f"{'Month':<15}{'New Clients':<15}"
        print(header)
        print("-" * len(header))
        for row in rows:
            month = row['Month']
            new_clients = row['NewClients']
            print(f"{month:<15}{new_clients:<15}")
        
        print("\nReport generated successfully.")
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")

def main():
    """
    Main function to execute the client count report.
    """
    # Database configuration
    config = {
        'user': 'Willson_user',
        'password': 'securepassword123',
        'host': '127.0.0.1',
        'database': 'WillsonFinancial',
        'raise_on_warnings': True
    }

    # Connect to the database
    connection, cursor = connect_to_database(config)

    try:
        # Generate the report
        report_clients_added(cursor)
    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    main()
