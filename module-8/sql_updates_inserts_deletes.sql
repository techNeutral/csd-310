INSERT INTO film(film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) 
    VALUES('Nope', '2022', '130', 'Jordan Peele', (SELECT studio_id FROM studio WHERE studio_name = 'Universal Pictures'),(SELECT genre_id FROM genre WHERE genre_name = 'Horror') );


UPDATE film
SET genre_id = 1
WHERE film_name = 'Alien';