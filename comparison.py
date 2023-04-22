
def comparison(list1, list2):
    following = []
    notFollowing = []
    
    if list1 == list2:
        print("Nothing changed.")
    else:
        # Checks if an account in the new list ISN'T in the old list, 
        # this account is whom the user you choose to scan data followed.
        for i in list1:
            if i not in list2:
                following.append(i)
        
        followingStr = " ".join(following)        
        print(f"Followed: \n\t{followingStr}\n")
        print(f"{len(following)} followed or changed @.")

        # Checks if an account in the old list ISN'T in the new list, 
        # this account is whom the user you chose to scan data has stopped following.
        for i in list2:
            if i not in list1:
                notFollowing.append(i)    

        notFollowingStr = " ".join(notFollowing)
        print(f"\nUnfollowed: \n\t{notFollowingStr}")
        print(f"{len(notFollowing)} unfollowed or changed @. \n")