import csv
import sqlite3
import logging


logging.basicConfig(
    filename='logfile.log',
    encoding='utf-8',
    level=logging.INFO
)

try:
    sqlite_connection = sqlite3.connect('db.sqlite3')
    cursor = sqlite_connection.cursor()
    logging.info('Database connection successfull')

    with open('ingredients.csv', encoding='utf8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        id = 1
        for row in reader:
            query = f'INSERT INTO recipes_ingredient (id, name, measurement_unit) VALUES ({id}, "{row[0]}", "{row[1]}");'
            logging.info(f'executing: {query}')
            cursor.execute(query)
            sqlite_connection.commit()
            id += 1

except sqlite3.Error as error:
    logging.error(f'Error connecting to database: {error}')

finally:
    if sqlite_connection:
        sqlite_connection.close()
        logging.info('Connection to database closed')
