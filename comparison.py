
def comparison(list1, list2):
    following = []
    notFollowing = []
    
    list1l = list1[0].split(" ")
    list2l = list2[0].split(" ")
    
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