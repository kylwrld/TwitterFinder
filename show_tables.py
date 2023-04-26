import sqlite3 as sl

def show_tables(): 
    try:
        con = sl.connect('user.db')
        sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
        cursor = con.cursor()
        cursor.execute(sql_query)
        
        print("List of tables:")
        print("\t",cursor.fetchall())
    
    except sl.Error as e:
        print(e)
        
    finally:
        if con:
            con.close()
            
if __name__ == "__main__":
    show_tables()