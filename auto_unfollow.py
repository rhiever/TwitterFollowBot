"""
Copyright 2014 Sebastian Raschka

Original project: https://github.com/rhiever/twitter-follow-bot
Copyright 2014 Randal S. Olson


This file is part of the Twitter Follow Bot2 library.

The Twitter Follow Bot2 library is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option) any
later version.

The Twitter Follow Bot library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with the Twitter
Follow Bot library. If not, see http://www.gnu.org/licenses/.

"""


import sqlite3
from twitter import Twitter, OAuth, TwitterHTTPError
from KEEP_FOLLOWING import keep_following
from AUTH_INFO import *


def auto_unfollow(db_file):
    """ 
       Unfollows users that are not following back and add them to
       the SQLite database.
       Keeps following uses that are in the KEEP_FOLLOWING list.

    """

    #connect to sqlite database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    #connect to twitter api
    t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
    
    # get twitter data
    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)['ids'])
    followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)['ids'])
    
    # convert twitter handles into IDs
    users_keep_following = set(t.users.lookup(screen_name=i)[0]['id'] for i in keep_following)
    
    # unfollow users
    not_following_back = following - followers
    cnt = 0
    for userid in not_following_back:
        try:
            if userid not in users_keep_following:
                t.friendships.destroy(user_id=userid)
                cnt += 1
                c.execute('SELECT user_id FROM twitter_db WHERE user_id=%s' %userid)
                check=c.fetchone()
                if not check:              
                    c.execute('INSERT INTO twitter_db (user_id) VALUES ("%s")' %userid)              
                print('unfollowed: %s' % t.users.lookup(user_id=userid)[0]['screen_name'])
                print('Unfollowed %s users' %cnt)
        except Exception as e:
            print(e)
            conn.commit()
            conn.close()
            print('Unfollowed %s users' %cnt)
            quit()
    
    conn.commit()
    conn.close()
    print('Unfollowed %s users' %cnt)  
    return

if __name__ == "__main__":
                       
    sqlite_file = './follow_db.sqlite'
    auto_unfollow(sqlite_file)
