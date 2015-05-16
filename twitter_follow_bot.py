# -*- coding: utf-8 -*-

"""
Copyright 2015 Randal S. Olson

This file is part of the Twitter Follow Bot library.

The Twitter Follow Bot library is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

The Twitter Follow Bot library is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
License for more details.

You should have received a copy of the GNU General Public License along with
the Twitter Follow Bot library. If not, see http://www.gnu.org/licenses/.
"""

from twitter import Twitter, OAuth, TwitterHTTPError
import os

# put your tokens, keys, secrets, and Twitter handle in the following variables
OAUTH_TOKEN = ""
OAUTH_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
TWITTER_HANDLE = ""

# put the full path and file name of the file you want to keep track of all
# the accounts you've ever followed
ALREADY_FOLLOWED_FILE = "already-followed.txt"

# put the full paths and file names of the files you want to keep track of
# your follows in
FOLLOWERS_FILE = "followers.txt"
FOLLOWS_FILE = "following.txt"

# make sure all of the sync files exist
for sync_file in [ALREADY_FOLLOWED_FILE, FOLLOWS_FILE, FOLLOWERS_FILE]:
    if not os.path.isfile(sync_file):
        with open(sync_file, "wb") as out_file:
            out_file.write("")

# create an authorized connection to the Twitter API
t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
                       CONSUMER_KEY, CONSUMER_SECRET))


def sync_follows():
    """
        Syncs the user's followers and follows locally so it isn't necessary
        to repeatedly look them up via the Twitter API.

        It is important to run this method at least daily so the bot is working
        with a relatively up-to-date version of the user's follows.
    """

    # sync the user's followers (accounts following the user)
    followers_status = t.followers.ids(screen_name=TWITTER_HANDLE)
    followers = set(followers_status["ids"])
    next_cursor = followers_status["next_cursor"]

    with open(FOLLOWERS_FILE, "wb") as out_file:
        for follower in followers:
            out_file.write("%s\n" % (follower))

    while next_cursor != 0:
        followers_status = t.followers.ids(
            screen_name=TWITTER_HANDLE, cursor=next_cursor)
        followers = set(followers_status["ids"])
        next_cursor = followers_status["next_cursor"]

        with open(FOLLOWERS_FILE, "ab") as out_file:
            for follower in followers:
                out_file.write("%s\n" % (follower))

    # sync the user's follows (accounts the user is following)
    following_status = t.friends.ids(screen_name=TWITTER_HANDLE)
    following = set(following_status["ids"])
    next_cursor = following_status["next_cursor"]

    with open(FOLLOWS_FILE, "wb") as out_file:
        for follow in following:
            out_file.write("%s\n" % (follow))

    while next_cursor != 0:
        following_status = t.friends.ids(
            screen_name=TWITTER_HANDLE, cursor=next_cursor)
        following = set(following_status["ids"])
        next_cursor = following_status["next_cursor"]

        with open(FOLLOWS_FILE, "ab") as out_file:
            for follow in following:
                out_file.write("%s\n" % (follow))


def get_do_not_follow_list():
    """
        Returns the set of users the bot has already followed in the past.
    """

    dnf_list = []
    with open(ALREADY_FOLLOWED_FILE, "rb") as in_file:
        for line in in_file:
            dnf_list.append(int(line))

    return set(dnf_list)


def get_followers_list():
    """
        Returns the set of users that are currently following the user.
    """

    followers_list = []
    with open(FOLLOWERS_FILE, "rb") as in_file:
        for line in in_file:
            followers_list.append(int(line))

    return set(followers_list)


def get_follows_list():
    """
        Returns the set of users that the user is currently following.
    """

    follows_list = []
    with open(FOLLOWS_FILE, "rb") as in_file:
        for line in in_file:
            follows_list.append(int(line))

    return set(follows_list)


def search_tweets(q, count=100, result_type="recent"):
    """
        Returns a list of tweets matching a phrase (hashtag, word, etc.).
    """

    return t.search.tweets(q=q, result_type=result_type, count=count)


def auto_fav(q, count=100, result_type="recent"):
    """
        Favorites tweets that match a phrase (hashtag, word, etc.).
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
            if "you have already favorited this status" not in str(e).lower():
                print("error: %s" % (str(e)))


def auto_rt(q, count=100, result_type="recent"):
    """
        Retweets tweets that match a phrase (hashtag, word, etc.).
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


def auto_follow(q, count=100, result_type="recent"):
    """
        Follows anyone who tweets about a phrase (hashtag, word, etc.).
    """

    result = search_tweets(q, count, result_type)
    following = get_follows_list()
    do_not_follow = get_do_not_follow_list()

    for tweet in result["statuses"]:
        try:
            if (tweet["user"]["screen_name"] != TWITTER_HANDLE and
                    tweet["user"]["id"] not in following and
                    tweet["user"]["id"] not in do_not_follow):

                t.friendships.create(user_id=tweet["user"]["id"], follow=False)
                following.update(set([tweet["user"]["id"]]))

                print("followed %s" % (tweet["user"]["screen_name"]))

        except TwitterHTTPError as e:
            print("error: %s" % (str(e)))

            # quit on error unless it's because someone blocked me
            if "blocked" not in str(e).lower():
                quit()


def auto_follow_followers_of_user(user_screen_name, count=100):
    """
        Follows the followers of a specified user.
    """
    following = get_follows_list()
    followers_of_user = set(
        t.followers.ids(screen_name=user_screen_name)["ids"][:count])
    do_not_follow = get_do_not_follow_list()

    for user_id in followers_of_user:
        try:
            if (user_id not in following and
                user_id not in do_not_follow):

                t.friendships.create(user_id=user_id, follow=False)
                print("followed %s" % user_id)

        except TwitterHTTPError as e:
            print("error: %s" % (str(e)))


def auto_follow_followers():
    """
        Follows back everyone who's followed you.
    """

    following = get_follows_list()
    followers = get_followers_list()

    not_following_back = followers - following

    for user_id in not_following_back:
        try:
            t.friendships.create(user_id=user_id, follow=False)
        except Exception as e:
            print("error: %s" % (str(e)))


def auto_unfollow_nonfollowers():
    """
        Unfollows everyone who hasn't followed you back.
    """

    following = get_follows_list()
    followers = get_followers_list()

    # put user IDs here that you want to keep following even if they don't
    # follow you back
    # you can look up Twitter account IDs here: http://gettwitterid.com
    users_keep_following = set([])

    not_following_back = following - followers

    # update the "already followed" file with users who didn't follow back
    already_followed = set(not_following_back)
    already_followed_list = []
    with open(ALREADY_FOLLOWED_FILE) as in_file:
        for line in in_file:
            already_followed_list.append(int(line))

    already_followed.update(set(already_followed_list))

    with open(ALREADY_FOLLOWED_FILE, "wb") as out_file:
        for val in already_followed:
            out_file.write(str(val) + "\n")

    for user_id in not_following_back:
        if user_id not in users_keep_following:
            t.friendships.destroy(user_id=user_id)
            print("unfollowed %d" % (user_id))


def auto_mute_following():
    """
        Mutes everyone that you are following.
    """
    following = get_follows_list()
    muted = set(t.mutes.users.ids(screen_name=TWITTER_HANDLE)["ids"])

    not_muted = following - muted

    # put user IDs of people you do not want to mute here
    # you can look up Twitter account IDs here: http://gettwitterid.com
    users_keep_unmuted = set([])

    # mute all
    for user_id in not_muted:
        if user_id not in users_keep_unmuted:
            t.mutes.users.create(user_id=user_id)
            print("muted %d" % (user_id))


def auto_unmute():
    """
        Unmutes everyone that you have muted.
    """
    muted = set(t.mutes.users.ids(screen_name=TWITTER_HANDLE)["ids"])

    # put user IDs of people you want to remain muted here
    # you can look up Twitter account IDs here: http://gettwitterid.com
    users_keep_muted = set([])

    # unmute all
    for user_id in muted:
        if user_id not in users_keep_muted:
            t.mutes.users.destroy(user_id=user_id)
            print("unmuted %d" % (user_id))
