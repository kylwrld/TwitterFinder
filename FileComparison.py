import os

def fileComparison(path1, path2):
    
    print("\n-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=")
    print("Make sure the first parameter is the most recent file.")
    print("-=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=\n")
    
    try:
        with open(path1, 'r') as f:
            file_1 = f.read()
        
        with open(path2, 'r') as f:
            file_2 = f.read()
    except FileNotFoundError as e:
        print("No such file or directory exists, you need to specify an existing file. Maybe this is your first time running and creating a file for comparison.")
        print(e)
        return

    file_1_list = file_1.split(" ")
    file_2_list = file_2.split(" ")
    
    print(f"Quantidade de pessoas seguidas em {path1}: ", len(file_1_list))
    print(f"Quantidade de pessoas seguidas em {path2}: ", len(file_2_list))

    following = []
    notFollowing = []


    if file_1_list == file_2_list:
        print("Nada mudou.")
    else:
        # Checks if an account in the new list ISN'T in the old list, 
        # this account is whom the user you choose to scan data followed.
        for i in file_1_list:
            if i not in file_2_list:
                following.append(i)
        
        followingStr = " ".join(following)        
        print(f"Seguiu: \n\t{followingStr}\n")
        print(f"{len(following)} pessoa(s) seguida(s) ou mudaram/mudou de @.")

        # Checks if an account in the old list ISN'T in the new list, 
        # this account is whom the user you chose to scan data has stopped following.
        for i in file_2_list:
            if i not in file_1_list:
                notFollowing.append(i)    

        notFollowingStr = " ".join(notFollowing)
        print(f"\nParou de seguir: \n\t{notFollowingStr}")
        print(f"{len(notFollowing)} pessoas que pararam de serem seguidas ou mudaram de @. \n")
    
if __name__ == "__main__":    
    fileComparison(path1='D:\Python\\following 1.txt', path2='D:\\Python Garbage\\following 16.txt')
