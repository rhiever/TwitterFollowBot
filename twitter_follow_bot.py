# -*- coding: utf-8 -*-

"""
Copyright 2014 Randal S. Olson

This file is part of the Twitter Follow Bot library.

The Twitter Follow Bot library is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option) any
later version.

The Twitter Follow Bot library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with the Twitter
Follow Bot library. If not, see http://www.gnu.org/licenses/.
"""

import os
import pickle

from twitter import Twitter, OAuth, TwitterHTTPError



# put your tokens, keys, secrets, and Twitter handle in the following variables
OAUTH_TOKEN = ""
OAUTH_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
TWITTER_HANDLE = ""

# put the full path and file name of the file you want to store your "already followed"
# list in
ALREADY_FOLLOWED_FILE = "already-followed.csv"

t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
            CONSUMER_KEY, CONSUMER_SECRET))


def search_tweets(q, count=100, result_type="recent"):
    """
        Returns a list of tweets matching a certain phrase (hashtag, word, etc.)
    """

    return t.search.tweets(q=q, result_type=result_type, count=count)


def auto_fav(q, count=100, result_type="recent"):
    """
        Favorites tweets that match a certain phrase (hashtag, word, etc.)
    """

    result = search_tweets(q, count, result_type)

    for tweet in result["statuses"]:
        try:
            # don't favorite your own tweets
            if tweet["user"]["screen_name"] == TWITTER_HANDLE:
                continue

            result = t.favorites.create(_id=tweet["id"])
            print("favorited: %s" % (result["text"].encode("utf-8")))

        # when you have already favorited a tweet, this error is thrown
        except TwitterHTTPError as e:
            print("error: %s" % (str(e)))


def auto_rt(q, count=100, result_type="recent"):
    """
        Retweets tweets that match a certain phrase (hashtag, word, etc.)
    """

    result = search_tweets(q, count, result_type)

    for tweet in result["statuses"]:
        try:
            # don't retweet your own tweets
            if tweet["user"]["screen_name"] == TWITTER_HANDLE:
                continue

            result = t.statuses.retweet(id=tweet["id"])
            print("retweeted: %s" % (result["text"].encode("utf-8")))

        # when you have already retweeted a tweet, this error is thrown
        except TwitterHTTPError as e:
            print("error: %s" % (str(e)))


def load_already_followed_list():
    """
        Returns list of users the bot has already followed.
    """
    already_followed = set()

    # make sure the "already followed" file exists
    if not os.path.isfile(ALREADY_FOLLOWED_FILE):
        with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
            out_file.write("")

    # read in the list of user IDs that the bot has already followed in the
    # past
    with open(ALREADY_FOLLOWED_FILE) as in_file:
        try:
            already_followed = pickle.load(in_file)
        except EOFError:
            pass

    return already_followed


def save_into_file(af, replace=False):
    """
        Saves set of users' id into file
    """
    #TODO: some refactoring needed

    # load old value and update them with new values
    # then save it
    already_followed = set()

    if not replace:
        already_followed = load_already_followed_list()

    already_followed.update(af)
    with open(ALREADY_FOLLOWED_FILE, "w") as f:
        pickle.dump(already_followed, f)


def follow_by_id(user_id, save_changes = False):
    """
        Follows user by id
    """
    t.friendships.create(user_id=user_id, follow=False)
    print("followed %s" % user_id)
    if save_changes:
        _add_id_into_file(user_id)



def _add_id_into_file(user_id):
    """
        Save user_id into file
    """
    already_followed = load_already_followed_list()
    already_followed.update(set([user_id]))
    save_into_file(already_followed)
    print("added into file %d" % user_id)


def _delete_id_from_file(user_id):
    already_followed = load_already_followed_list()
    already_followed -= set([user_id])
    save_into_file(already_followed, replace=True)
    print("deleted from file %d" % user_id)


def auto_follow(q, count=100, result_type="recent"):
    """
        Follows anyone who tweets about a specific phrase (hashtag, word, etc.)
    """

    result = search_tweets(q, count, result_type)
    do_not_follow = load_already_followed_list()

    for tweet in result["statuses"]:
        try:
            if (tweet["user"]["screen_name"] != TWITTER_HANDLE and
                    tweet["user"]["id"] not in load_already_followed_list() and
                    tweet["user"]["id"] not in do_not_follow):

                follow_by_id(tweet["user"]["id"], save_changes=True)
                mute_user_by_id(tweet["user"]["id"])

        except TwitterHTTPError as e:
            print("error: %s" % (str(e)))

            # quit on error unless it's because someone blocked me
            if "blocked" not in str(e).lower():
                quit()


def auto_follow_followers_for_user(user_screen_name, count=100):
    """
        Follows the followers of a user
    """
    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    followers_for_user = set(t.followers.ids(screen_name=user_screen_name)["ids"][:count]);
    do_not_follow = load_already_followed_list()
    
    for user_id in followers_for_user:
        try:
            if (user_id not in following and 
                user_id not in do_not_follow):

                follow_by_id(user_id, save_changes=True)

        except TwitterHTTPError as e:
            print("error: %s" % (str(e)))

def auto_follow_followers():
    """
        Follows back everyone who's followed you
    """

    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])

    not_following_back = followers - following

    for user_id in not_following_back:
        try:
            follow_by_id(user_id, save_changes=True)
        except Exception as e:
            print("error: %s" % (str(e)))


def unfollow_by_id(user_id, save_changes = False):
    """
        Unfollows user by id
    """
    t.friendships.destroy(user_id=user_id)
    print("unfollowed %d" % (user_id))

    if save_changes:
        _delete_id_from_file(user_id)




def auto_unfollow_nonfollowers():
    """
        Unfollows everyone who hasn't followed you back
    """

    # it checks if file exists so we don't have to do it again
    already_followed = load_already_followed_list()
    followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])

    # put user IDs here that you want to keep following even if they don't
    # follow you back
    users_keep_following = set([])

    # searching for only in the already followed
    # and don't touch those who we followed on purpose
    not_following_back = already_followed - followers

    unfollowed = []

    for user_id in not_following_back:
        if user_id not in users_keep_following:
            unfollow_by_id(user_id, save_changes = True)




def mute_user_by_id(user_id):
    """
        Mutes user by id
    """
    t.mutes.users.create(user_id=user_id)
    print("muted %d" % user_id)


def auto_mute_following():
    """
        Mutes everyone that you are following
    """
    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    muted = set(t.mutes.users.ids(screen_name=TWITTER_HANDLE)["ids"])

    not_muted = following - muted

    # put user IDs of people you do not want to mute here
    users_keep_unmuted = set([])
            
    # mute all        
    for user_id in not_muted:
        if user_id not in users_keep_unmuted:
            mute_user_by_id(user_id)
            print("muted %d" % user_id)


def auto_unmute():
    """
        Unmutes everyone that you have muted
    """
    muted = set(t.mutes.users.ids(screen_name=TWITTER_HANDLE)["ids"])

    # put user IDs of people you want to remain muted here
    users_keep_muted = set([])
            
    # mute all        
    for user_id in muted:
        if user_id not in users_keep_muted:
            t.mutes.users.destroy(user_id=user_id)
            print("unmuted %d" % (user_id))


if __name__ == "__main__":
    auto_follow("english language", 10)
    auto_unfollow_nonfollowers()




