import sqlite3 as sl

class Database:
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
        
        # Checks if the given 'following' list is already in the database
        if len(comparison) == 0:
            values = [self.user, followingString]
            with self.connect:
                query = (f"INSERT INTO {self.user} (user, following) VALUES (?, ?)")
                self.cursor.execute(query, values)  
        else:
            for following in comparison:
                if followingString in following:
                    print(f"Alredy in database: id={comparison.index(following)+1}", )
                    
                    values = [self.user, followingString]
                    with self.connect:
                        query = (f"INSERT INTO {self.user} (user, following) VALUES (?, ?)")
                        self.cursor.execute(query, values)
                    break
            else:
                values = [self.user, followingString]
                with self.connect:
                    query = (f"INSERT INTO {self.user} (user, following) VALUES (?, ?)")
                    self.cursor.execute(query, values) 
    
    
    def delete_by_id(self, id: int):
        with self.connect:
            query = (f"DELETE FROM {self.user} WHERE id_user = ?")
            self.cursor.execute(query, str(id))
            self.connect.commit()
        
        with self.connect:
            self.cursor.execute(f"SELECT id_user FROM {self.user}")
            idselected = self.cursor.fetchall()
            
        idselectedlist = []
        for id in idselected:
            listindex = idselected[idselected.index(id)][0]
            idselectedlist.append(listindex)
        
        missingNumbers = sorted(set(range(idselectedlist[0], idselectedlist[-1])) - set(idselectedlist))
        allNumbers = []
        
        for i in idselectedlist:
            allNumbers.append(i)
        for i in missingNumbers:
            allNumbers.append(i)
        if 1 not in allNumbers:
            allNumbers.append(1)
        allNumbers.sort()
        
        values = [allNumbers[0:-1], idselectedlist]
        with self.connect:
            query = f"UPDATE {self.user} SET id_user = ? WHERE id_user = ?"
            for i in range(len(allNumbers)-1):
                self.cursor.execute(query, [allNumbers[i], idselectedlist[i]])
            self.connect.commit()

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
                result = self.cursor.fetchall()
                return result
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
        
        mostRecent = followingList[-1]
        secondRecent = followingList[-2]
        
        try:
            return mostRecent, secondRecent
        except IndexError as e:
            print("You need to run the program twice to compare two lists")
            print(e)

    def select_by_id(self, id: int):
        with self.connect:
            self.cursor.execute(f"SELECT following FROM {self.user} WHERE id_user = {id}")
            result = self.cursor.fetchall()
            result = " ".join(result[0])
            return result

    def show_tables(self): 
        with self.connect:
            sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
            self.cursor.execute(sql_query)
            
            print("List of tables:")
            print("\t",self.cursor.fetchall())
            
    def comparison(list1, list2):
        following = []
        notFollowing = []
        
        list1l = list1.split(" ")
        list2l = list2.split(" ")
        
        for i in list1l:
            list1l[list1l.index(i)] = list1l[list1l.index(i)].lower()
            
        for i in list2l:
            list2l[list2l.index(i)] = list2l[list2l.index(i)].lower()
            
        if list1l == list2l:
            print("Nothing changed.")
        else:
            # Checks if an account in the new list ISN'T in the old list, 
            # this account is whom the user you choose to scan data followed.
            for i in list1l:
                if i not in list2l:
                    following.append(i)
            
            followingStr = " ".join(following)        
            print(f"Followed: \n\t{followingStr}\n")
            print(f"{len(following)} followed or changed @.")

            # Checks if an account in the old list ISN'T in the new list, 
            # this account is whom the user you chose to scan data has stopped following.
            for i in list2l:
                if i not in list1l:
                    notFollowing.append(i)    

            notFollowingStr = " ".join(notFollowing)
            print(f"\nUnfollowed: \n\t{notFollowingStr}")
            print(f"{len(notFollowing)} unfollowed or changed @. \n")