from env import secure
import mysql.connector

# Database class
class Database:
    try: 
        db = mysql.connector.connect(
        host = secure.DATABASE_HOST,
        user = secure.DATABASE_USER,
        password = secure.DATABASE_PASSWORD,
        database = secure.DATABASE_NAME,
        auth_plugin="mysql_native_password"
        )
        cursor = db.cursor(buffered=True)
        print(cursor)
    except Exception as e:
        print(e)
        pass
 

