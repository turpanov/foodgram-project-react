import csv
import sqlite3
from winreg import QueryReflectionKey

try:
    sqlite_connection = sqlite3.connect('db.sqlite3')
    cursor = sqlite_connection.cursor()
    print('Database connection successfull')

    with open('ingredients.csv', encoding='utf8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        id = 1
        for row in reader:
            print(row)
            query = f'INSERT INTO recipes_ingredient (id, name, measurement_unit) VALUES ({id}, "{row[0]}", "{row[1]}");'
            print(query)
            cursor.execute(query)
            sqlite_connection.commit()
            id += 1

except sqlite3.Error as error:
    print('Error connecting to database', error)

finally:
    if sqlite_connection:
        sqlite_connection.close()
        print('Connection to database closed')