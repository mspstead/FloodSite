import psycopg2

try:
    conn = psycopg2.connect(database='django', user='', password='', host='localhost')
except:
    print("Unable to connect to the database.")

