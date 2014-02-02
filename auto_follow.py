
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
import QUERIES
from AUTH_INFO import *

def print_results(stats_dict):
    """
    Prints stats of how many people were followed.

    """
    for q in stats_dict.keys():
        print('\nQuery: %s\nFriends in query:%s\nUsers in DB:%s\nNew followers:%s\n'
                %(stats_dict[q][0], stats_dict[q][2], stats_dict[q][1]))
    return


def auto_follow_loop(queries, db_file, count=10, result_type="recent"):
    """
    Auto-follows people that have not been followed before and match words
    in the QUERIES list.
    Adds new followers to SQLite database.    

    """

    #connect to sqlite database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    #connect to twitter api
    t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

    stats = dict()
    # search for query term, follow matched users and append user id to sqlite db      
    for q in queries:
        result = t.search.tweets(q=q, result_type=result_type, count=count)
        following = set(t.friends.ids(screen_name=TWITTER_HANDLE)['ids'])
        stats[q] = [0,0,0]  # stats for found_friends, new_followers, followers_in_db
        for tweet in result['statuses']:
            try:
                if tweet['user']['screen_name'] != TWITTER_HANDLE and tweet['user']['id'] not in following:
                    
                    # check if user ID is already in sqlite database
                    c.execute('SELECT user_id FROM twitter_db WHERE user_id=%s' %tweet['user']['id'])
                    check=c.fetchone()
                    if not check:
                        t.friendships.create(user_id=tweet['user']['id'])
                        following.update(set([tweet['user']['id']]))
                        print('following: %s' % tweet['user']['screen_name'])
                        # add new ID to sqlite database
                        c.execute('INSERT INTO twitter_db (user_id) VALUES ("%s")' %tweet['user']['id'])
                        stats[q][1] += 1
                    else:
                        stats[q][2] += 1
                else:
                    stats[q][0] += 1
                 
            except TwitterHTTPError as e:
                print("error: ", e)
    
                # quit on error unless it's because someone blocked me
                if "blocked" not in str(e).lower():
                    conn.commit()
                    conn.close()
                    print(print_results(stats))
                    quit()

    conn.commit()
    conn.close()
    print(print_results(stats))
    return


if __name__ == "__main__":
                       
    sqlite_file = './follow_db.sqlite'
    auto_follow_loop(QUERIES.queries, sqlite_file, count=100, result_type="recent")
