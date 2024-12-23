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

def report_high_transaction_clients(cursor):
    """
    Generate a report of clients with more than 10 transactions in any single month,
    including the Client ID.

    Args:
        cursor (mysql.connector.cursor.MySQLCursorDict): Database cursor.
    """
    print("\n--- High-Transaction Clients (More than 10 Transactions in a Month) ---\n")
    
    query = """
        SELECT 
            C.ClientID AS ClientID,
            C.Name AS ClientName,
            COUNT(T.TransactionID) AS TransactionCount,
            DATE_FORMAT(T.TransactionDate, '%Y-%m') AS Month
        FROM Transactions T
        JOIN Accounts A ON T.AccountID = A.AccountID
        JOIN Clients C ON A.ClientID = C.ClientID
        GROUP BY C.ClientID, Month
        HAVING TransactionCount > 10
        ORDER BY Month ASC, TransactionCount DESC;
    """
    
    try:
        # Execute the query
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if not rows:
            print("No clients with more than 10 transactions in a single month.")
            return
        
        # Display the results
        header = f"{'Client ID':<15}{'Client Name':<25}{'Transaction Count':<20}{'Month':<10}"
        print(header)
        print("-" * len(header))
        for row in rows:
            client_id = row['ClientID']
            client_name = row['ClientName']
            transaction_count = row['TransactionCount']
            month = row['Month']
            print(f"{client_id:<15}{client_name:<25}{transaction_count:<20}{month:<10}")
        
        print("\nReport generated successfully.")
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")

def main():
    """
    Main function to execute the high-transaction client report.
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
        report_high_transaction_clients(cursor)
    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    main()
