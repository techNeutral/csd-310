#Brett Fuller
#12/1/2024
#CSD 310 – Assignment 7.2

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

    cursor = db.cursor()
    cursor.execute("SELECT studio_id, studio_name FROM studio")
    studios = cursor.fetchall()

    print("\n-- DISPLAYING Studio RECORDS --")
    for studio in studios:
        print("Studio ID: {}\nStudio Name: {}\n".format(studio[0], studio[1]))
    

    cursor = db.cursor()
    cursor.execute("SELECT genre_id, genre_name FROM genre")
    genres = cursor.fetchall()

    print("\n-- DISPLAYING Genre RECORDS --")
    for genre in genres:
        print("Genre ID: {}\nGenre Name: {}\n".format(genre[0], genre[1]))

    cursor = db.cursor()
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120")
    films = cursor.fetchall()

    print("\n-- DISPLAYING Short Film RECORDS --")
    for film in films:
        print("Film Name: {}\nRuntime: {}\n".format(film[0], film[1]))

    cursor = db.cursor()
    cursor.execute("SELECT film_name, film_director FROM film GROUP BY film_director, film_name ORDER BY film_director ASC, film_name DESC")
    films = cursor.fetchall()

    print("\n-- DISPLAYING Director RECORDS in Order --")
    for film in films:
        print("Film Name: {}\nDirector: {}\n".format(film[0], film[1]))
    
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('  The supplied username or password is invalid')
    elif err.errno == errorcode.ER_BAD_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)

finally:
    db.close()