import sqlite3 as sl

class Bdd:
    # Initializes the connection to the 'user' database
    def __init__(self, user):
        self.connect = sl.connect("user.db")
        
        self.user = str(user).lower()
        
        with self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.user} (id_user INTEGER, user TEXT, following TEXT, PRIMARY KEY('id_user' AUTOINCREMENT))")
       
    # Adds followingList to the 'user' database
    def add_database(self, followingList: list):
        followingString = " ".join(followingList)
        comparison = self.get_only_following()
        
        for following in comparison:
            if followingString in following:
                print(f"Alredy in database: id={comparison.index(following)+1}", )
                while True:
                    ask = input("Wanna add to the database again? y/n\n")
                    if ask.lower() == "y":
                        valores = [self.user, followingString]
        
                        with self.connect:
                            query = (f"INSERT INTO {self.user} (user, following) VALUES (?, ?)")
                            self.cursor.execute(query, valores)
                        break
                    elif ask.lower() == "n":
                        print("Finished.")
                        break
                    else:
                        print("Type y or n please.")
                break
        # valores = [self.user, followingString]
        
        # with self.connect:
        #     query = (f"INSERT INTO {self.user} (user, following) VALUES (?, ?)")
        #     self.cursor.execute(query, valores)
    
    def get_only_following(self):
        with self.connect:
            self.cursor.execute(f"SELECT following FROM {self.user}")
            self.following = self.cursor.fetchall()
            return self.following
    
    # Returns the given user's table
    def get_database(self):
        try:
            with self.connect:
                self.cursor.execute(f"SELECT * FROM {self.user}")
                self.result = self.cursor.fetchall()
                return self.result
        except AttributeError as e:
            print("You must have forgotten to call the 'add_database' function to pass the username and add something to the database")
            print(e)
            
    def get_last_two(self):
        followingList = []
        followingDict = {}
        result = self.get_database()
        
        for user in result:
            followingDict.update({f"{user[1]}-{user[0]}":f"{user[2]}"})
        
        for item in followingDict.values():
            followingList.append(item)
        
        mostRecent = []
        secondRecent = []
        mostRecent.append(followingList[-1]) # Most recent
        try:
            secondRecent.append(followingList[-2])
            return mostRecent, secondRecent
        except IndexError as e:
            print("You need to run the program twice to compare two lists")
            print(e)

    def show_tables(self): 
        with self.connect:
            sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
            self.cursor.execute(sql_query)
            
            print("List of tables:")
            print("\t",self.cursor.fetchall())