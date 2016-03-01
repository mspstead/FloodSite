import psycopg2

try:
    conn = psycopg2.connect(database='django', user='django', password='AgZP7U56Mw', host='localhost')
except:
    print("Unable to connect to the database.")

