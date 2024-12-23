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

def report_average_asset_per_client(cursor):
    """
    Generate a report showing the average asset value for each client in alphabetical order,
    including the Client ID.

    Args:
        cursor (mysql.connector.cursor.MySQLCursorDict): Database cursor.
    """
    print("\n--- Average Asset Value for Each Client Report ---\n")
    
    query = """
        SELECT 
            C.ClientID AS ClientID,
            C.Name AS ClientName,
            AVG(A.Value) AS AverageAssetValue
        FROM Clients C
        LEFT JOIN Accounts Ac ON C.ClientID = Ac.ClientID
        LEFT JOIN Assets A ON Ac.AccountID = A.AccountID
        GROUP BY C.ClientID, C.Name
        ORDER BY C.Name ASC;
    """
    
    try:
        # Execute the query
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Display the results
        if rows:
            header = f"{'Client ID':<15}{'Client Name':<25}{'Average Asset Value':<20}"
            print(header)
            print("-" * len(header))
            for row in rows:
                client_id = row['ClientID']
                client_name = row['ClientName']
                avg_asset_value = row['AverageAssetValue'] if row['AverageAssetValue'] is not None else 0.0
                print(f"{client_id:<15}{client_name:<25}${avg_asset_value:,.2f}")
        else:
            print("No asset data found in the database.")
        
        print("\nReport generated successfully.")
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")

def main():
    """
    Main function to execute the average asset per client report.
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
        report_average_asset_per_client(cursor)
    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    main()
