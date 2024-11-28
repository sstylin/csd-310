# Implementation Steve Stylin@Bellevue University: Module 7 Movies: Table Queries
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
    connection = mysql.connector.connect(
        host = DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME
)
    if connection.is_connected():
            print("Connection to MySQL DB successful")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username and password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR: 
        print(" The specific database does not exist")
    else:
        print(err)
finally:
    connection.close


cursor = connection.cursor()

# Query 1: Select all fields from the studio table
cursor.execute('select studio_id as "Studio ID" , studio_name as "Studio Name" from studio;')
studios = cursor.fetchall()
print("\n--DISPLAYING Studio Records--")
for studio in studios:
    print("\nStudio ID: {}\nStudio Name: {}\n".format(studio[0], studio[1]))


# Query 2: Select all fields from the genre table
cursor.execute('select genre_id as "Genre ID:", genre_name as "Genre Name:" from genre;')
genres = cursor.fetchall()
print("\n--DISPLAYING Genre Records--")
for genre in genres:
    print("Genre ID: {}\nGenre Name: {}\n".format(genre[0], genre[1]))


#Query 3: Select movie names with a run time of less than two hours
cursor.execute('select film_name as "Film Name: ", film_runtime as "Runtime" from film where film_runtime <=117;')
short_movies = cursor.fetchall()
print("\n--DISPLAYING Short Film Records--")
for film in short_movies:
    print("Film Name: {}\nRuntime: {}\n".format(film[0],film[1]))


# Query 4: List of film names and directors grouped by director
cursor.execute('select film_name , film_director from film ORDER BY film_director asc')
grouped_movies = cursor.fetchall()
print("\n--DISPLAYING Director Records in Order--")
for film in grouped_movies:
    print("Film Name: {}\nDirector: {}\n".format(film[0],film[1]))






# Closing the connection
cursor.close()
connection.close()