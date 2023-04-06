import psycopg2
from decouple import config

class DbSetup:
    def connect(self):
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
    # try:
    print("set")
        # db_setup = DbSetup()
    #     db_setup.create_table()
    # except:
    #     pass