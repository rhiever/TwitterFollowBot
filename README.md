#Twitter Follow Bot2

Copyright 2014 Sebastian Raschka 

A Python twitter bot that automatically follows users that
match a specified search query on Twitter and can unfollow
users that are not following you back.
Supports smart tracking of users you already followed and 
unfollowed in a SQLite database.

Original project: [https://github.com/rhiever/twitter-follow-bot](https://github.com/rhiever/twitter-follow-bot) by Randal S. Olson (2014)

##Disclaimer

I hold no liability for what you do with this script or what happens to you by using this script. Abusing this script *can* get you banned from Twitter, so make sure to read up on proper usage of the Twitter API.


##Dependencies

You will need to install Python's `twitter` library first:

    easy_install twitter
    
You will also need to create an app account on https://dev.twitter.com/apps

1. Sign in with your Twitter account
2. Create a new app account
3. Modify the settings for that app account to allow read & write
4. Generate a new OAuth token with those permissions
5. Manually edit this script and put those tokens in the script


##Usage

#### Running Twitter Follow Bot2 for the first time

**1)**  
Open the file `AUTH_INFO.py` and add your Twitter information


	OAUTH_TOKEN = ""
	OAUTH_SECRET = ""
	CONSUMER_KEY = ""
	CONSUMER_SECRET = ""
	TWITTER_HANDLE = ""



**2)**  
Go into the script directory and run  
`python3 init_follow_db.py`  
to create a new SQLite3 database that will keep track of the Twitter UserIDs that you have already followed of unfollowed.
By default the SQLite database will be created as "follow_db.sqlite" in the script directory.



####Automatically follow all users who recently tweeted about a specific topic
**1)**  
Open the file `QUERIES.py` and add the search queries to search for people  
who you want to follow.  
Example:

	
	queries = [
				"bioinformatics",
                "Python AND sqlite3""
              ]
	

    from twitter_follow_bot import auto_follow
  
**2)**  
By default 10 people per search query will be followed. If you want to change
the number of people, open the file `auto_follow.py` and change the `count`
parameter at the bottom of the script
	
	if __name__ == "__main__":
                       
    db_file = './follow_db.sqlite'
    auto_follow_loop(QUERIES.queries, db_file, count=10, result_type="recent")

**3)**  
Via the terminal, execute the script in the script's directory:  
	`python3 auto_follow.py`

New people you are following will be added to the SQLite database so you don't follow them twice once you unfollowed them.



####Automatically unfollow all users who have not followed you back

**1)**  
Open the file `KEEP_FOLLOWING.txt` to add users who you want to keep following to the list.

Example:
	
	keep_following = [
        'someimaginaryfantasyname1',
        'someimaginaryfantasyname2',
        'someimaginaryfantasyname3',
    ]

**2)**  
Via the terminal, execute the script in the script's directory:  
	`python3 auto_unfollow.py`

New people you are unfollowing will be added to the SQLite database so you don't follow them twice once you unfollowed them.

####Automatically follow any user back who has followed you

**1)**
Open the file `DONT_FOLLOW.py` to add users who you really don't want to
follow - even if they are following you.

Example:
	
	dont_follow = [
        'someimaginaryfantasyname1',
        'someimaginaryfantasyname2',
        'someimaginaryfantasyname3',
    ]

**2)**  
Via the terminal, execute the script in the script's directory:  
	`python3 auto_follow_back.py`

New people you are unfollowing will be added to the SQLite database so you don't follow them twice once you unfollowed them.