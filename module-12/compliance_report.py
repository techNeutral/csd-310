import mysql.connector
from mysql.connector import errorcode
import sys

def connect_to_database(config):
    """
    Connect to the MySQL database using the provided configuration.

    Args:
        config (dict): Database configuration parameters.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object.
    """
    try:
        connection = mysql.connector.connect(**config)
        print("Connected to the database successfully.")
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Invalid username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist.")
        else:
            print(f"Error: {err}")
        sys.exit(1)  # Exit the script with an error status

def fetch_compliance_reports(cursor):
    """
    Fetch and display the total number of compliance reports per employee,
    including Employee ID.

    Args:
        cursor (mysql.connector.cursor.MySQLCursorDict): Database cursor.
    """
    print("\n--- Compliance Reports by Employee ---\n")
    query = """
        SELECT 
            E.EmployeeID AS Employee_ID,
            E.Name AS Employee_Name,
            COUNT(CM.ComplianceID) AS Total_Compliance_Reports 
        FROM 
            Compliance CM
        INNER JOIN 
            Employees E ON CM.EmployeeID = E.EmployeeID 
        GROUP BY 
            E.EmployeeID, E.Name
        ORDER BY 
            E.EmployeeID ASC;
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            print("No compliance reports found in the database.")
            return

        # Display the results
        header = f"{'Employee ID':<15}{'Employee Name':<25}{'Total Compliance Reports':<25}"
        print(header)
        print("-" * len(header))
        for row in rows:
            employee_id = row['Employee_ID']
            employee_name = row['Employee_Name']
            total_reports = row['Total_Compliance_Reports']
            print(f"{employee_id:<15}{employee_name:<25}{total_reports:<25}")
        print("\nReport generated successfully.")
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")

def main():
    """
    Main function to execute the compliance reports query.
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
    connection = connect_to_database(config)

    try:
        # Use a dictionary cursor for easier data handling
        with connection.cursor(dictionary=True) as cursor:
            fetch_compliance_reports(cursor)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        # Close the database connection
        if connection.is_connected():
            connection.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    main()
