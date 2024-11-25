#Brett Fuller
#11/23/2024
#CSD 310 – Assignment 6.2

import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "movies_user",
    "password": "P0pC0rn!",
    "host": "127.0.0.1",
    "database": "movies",
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)

    print("\n Database user {} connected to MySQL on host {} with database {}", format(config["user"]), config["host"], config["database"])

    input("\n\n Press any key to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('  The supplied username or password is invalid')
    elif err.errno == errorcode.ER_BAD_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)

finally:
    db.close()