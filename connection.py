import mysql.connector

def connect():
    conn = mysql.connector.connect(host='localhost',user='root',password='Likin@(2005)',database='hackwave')
    cursor = conn.cursor()
    return conn,cursor

conn,cursor = connect()
query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
data = ('Likin M B', 'likinmb915@gmail.com', 'Likin@2005') 
cursor.execute(query,data)
conn.commit()
cursor.close()
conn.close()