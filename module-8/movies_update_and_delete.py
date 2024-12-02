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

def revert_to_stock(cursor):
    cursor.execute("UPDATE film SET genre_id = 2 WHERE film_name = 'Alien'")

    cursor.execute("Delete from film WHERE film_name = 'Nope'")
    movie =''
    cursor.execute("Select film_name from film WHERE film_name = 'Gladiator'")
    movie = cursor.fetchall()
    if movie[0][0] != 'Gladiator':
        cursor.execute("INSERT INTO film(film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) VALUES('Gladiator', '2000', '155', 'Ridley Scott', (SELECT studio_id FROM studio WHERE studio_name = 'Universal Pictures'),(SELECT genre_id FROM genre WHERE genre_name = 'Drama') )")


def change_genre_for_alien_to_horror(cursor):
    #sqlString = "UPDATE film SET genre_id =" + genre_id + " WHERE film_name = " + film_name
    cursor.execute("UPDATE film SET genre_id = 1 WHERE film_name = 'Alien'")

def remove_Gladiator(cursor):
    cursor.execute("DELETE from film WHERE film_name = 'Gladiator'")

def add_Nope_to_Films(cursor):
    cursor.execute("INSERT INTO film(film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) VALUES('Nope', '2022', '130', 'Jordan Peele', (SELECT studio_id FROM studio WHERE studio_name = 'Universal Pictures'),(SELECT genre_id FROM genre WHERE genre_name = 'Horror') )")

def show_films(cursor, title):
    cursor.execute("SELECT film_name as Name, film_director as Director, genre_name as Genre, studio_name as 'Studio Name' from film INNER JOIN genre ON film.genre_id=genre.genre_id INNER JOIN studio ON film.studio_id=studio.studio_id")
    films = cursor.fetchall()

    print("\n -- {} --".format(title))

    for film in films:
        #print("Film Name: {}\n".format(film[0]))
        print("Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n".format(film[0], film[1], film[2], film[3]))



try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    #This is a command to put the records back to how they were in the database originally, this made it so I could test my code repeatedly. Should not cause errors even at first run.
    revert_to_stock(cursor)

    #FIrst run of display sql info, this is what the DB looks like at the beginning
    show_films(cursor, "DISPLAYING FILMS")

    #Here I execute the function to add the film nope to the film table, then rerun the show films function with the new description
    add_Nope_to_Films(cursor)
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    #Here I execute the function to update the genre link to horror for alien in film table, then rerun the show films function with the new description
    change_genre_for_alien_to_horror(cursor)
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror")

    #Here I execute the function to remove the film Gladiator from the film table, then rerun the show films function with the new description
    remove_Gladiator(cursor)
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('  The supplied username or password is invalid')
    elif err.errno == errorcode.ER_BAD_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)

finally:
    db.close()


