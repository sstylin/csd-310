# Implementation Steve Stylin@Bellevue University: Module 8  Movies: Update & Deletes
import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()
# Database connection parameters
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

try:
    # Create a database connection to the MySQL database
    db = mysql.connector.connect(
        host = DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME
)
    if db.is_connected():
            print("Connection to MySQL DB successful")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username and password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR: 
        print(" The specific database does not exist")
    else:
        print(err)
finally:
    db.close

def show_films(cursor, title):
    # Method to execute an inner join on all tables and iterate over the dataset to output the results
    cursor.execute("""
        SELECT film_name AS Name, 
               film_director AS Director, 
               genre_name AS Genre, 
               studio_name AS 'Studio Name' 
        FROM film 
        INNER JOIN genre ON film.genre_id = genre.genre_id 
        INNER JOIN studio ON film.studio_id = studio.studio_id
    """)
    
    # Get the results from the cursor object
    films = cursor.fetchall()
    print("\n --{} --".format(title))
    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre: {}\nStudio Name: {}\n".format(film[0], film[1], film[2], film[3]))


cursor = db.cursor()

# Displaying films
show_films(cursor, "DISPLAYING FILMS")

# Inserting a new record into the film table
insert_query = """
    INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) 
    VALUES ('Inception', '2010', 148, 'Christopher Nolan', 1, 1)
"""
cursor.execute(insert_query)
db.commit()

# Displaying films after insertion
show_films(cursor, "DISPLAYING FILMS AFTER INSERTION")

# Updating the film 'Alien' to being a Horror film
update_query = """
    UPDATE film 
    SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror') 
    WHERE film_name = 'Alien'
"""
cursor.execute(update_query)
db.commit()

# Displaying films after update
show_films(cursor, "DISPLAYING FILMS AFTER UPDATING ALIEN")

# Deleting the movie 'Gladiator'
delete_query = "DELETE FROM film WHERE film_name = 'Gladiator'"
cursor.execute(delete_query)
db.commit()

# Displaying films after deletion
show_films(cursor, "DISPLAYING FILMS AFTER DELETION")

# Closing the cursor and database connection
cursor.close()
db.close()
