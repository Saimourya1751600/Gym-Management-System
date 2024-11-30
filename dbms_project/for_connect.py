import mysql.connector
def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root', 
            password='',
            database='gym_aero_yoga_zumba_management'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None