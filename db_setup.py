import psycopg2
from decouple import config

class DbSetup:
    def connect(self):
        """
        Connects to a PostgreSQL database using the provided credentials from the environment variables.

        Returns:
            conn (psycopg2.extensions.connection): A connection object to interact with the database.
            
        Raises:
            psycopg2.Error: If the database connection fails.
        """
        try:
            conn = psycopg2.connect(dbname=config("POSTGRES_DB_NAME"),
                                    user=config("POSTGRES_USER"),
                                    password=config("POSTGRES_PASSWORD"),
                                    port=config("POSTGRES_PORT"),
                                    host="postgres")
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        

    def create_table(self):
        """
        Creates a PostgreSQL table named "messages" with columns for id (SERIAL PRIMARY KEY), user_id (INTEGER), role (VARCHAR(20) NOT NULL), and message (TEXT NOT NULL).
        
        Raises:
            psycopg2.Error: If the database connection fails or the table creation fails.
        """
        
        command = (
        """
        CREATE TABLE messages (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            role VARCHAR(20) NOT NULL,
            message TEXT NOT NULL
        )
        """
        )
        
        try:
            conn = self.connect()
            cur = conn.cursor()
            
            cur.execute(command)
                
            cur.close()
            conn.commit()
                    
            if conn is not None:
                conn.close()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            
    def insert_mess(self,role ,message, user_id):
        """
        Inserts a new row into the "messages" table in the connected PostgreSQL database, containing the provided user_id, role, and message.

        Args:
            role (str): The role of the user who sent the message.
            message (str): The text of the message sent by the user.
            user_id (int): The unique identifier of the user who sent the message.
        
        Raises:
            psycopg2.Error: If the database connection fails or the query execution fails.
        """
        query= """ INSERT INTO messages (user_id, role, message) VALUES (%s, %s, %s)"""
        record = (user_id, role, message)
        try:
            conn = self.connect()
            cur = conn.cursor()
            
            cur.execute(query, record)
                
            cur.close()
            conn.commit()
                    
            if conn is not None:
                conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            
    def delete_mess(self,user_id):
        """
        Deletes one or more rows from the "messages" table in the connected PostgreSQL database that match the provided user_id.

        Args:
            user_id (int): The unique identifier of the user whose message(s) should be deleted.
        
        Raises:
            psycopg2.Error: If the database connection fails or the query execution fails.
        """
        query= """ DELETE FROM messages WHERE user_id = %s """
        record = [user_id]
        try:
            conn = self.connect()
            cur = conn.cursor()
            
            cur.execute(query, record)
                
            cur.close()
            conn.commit()
                    
            if conn is not None:
                conn.close()
                
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            
    def get_user_mess(self, user_id):
        """
        Retrieves all rows from the "messages" table in the connected PostgreSQL database that match the provided user_id, and returns the role and message columns for each row.

        Args:
            user_id (int): The unique identifier of the user whose messages should be retrieved.
        
        Returns:
            records (list of tuples): A list of tuples, where each tuple represents a matching row and contains the values of the role and message columns.
        
        Raises:
            psycopg2.Error: If the database connection fails or the query execution fails.
        """
        query= """ SELECT role, message FROM messages WHERE user_id = %s """
        record = [user_id]
        try:
            conn = self.connect()
            cur = conn.cursor()
            
            cur.execute(query, record)
            records = cur.fetchall()
                
            cur.close()
            conn.commit()
                    
            if conn is not None:
                conn.close()
            return records
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            

if __name__ == '__main__':
    try:
        db_setup = DbSetup()
        db_setup.create_table()
    except:
        pass