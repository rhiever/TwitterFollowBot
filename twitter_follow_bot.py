"""
Copyright 2014 Randal S. Olson

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

from __future__ import unicode_literals

from twitter import Twitter, OAuth, TwitterHTTPError
import os

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
TWITTER_HANDLE = os.environ['TWITTER_HANDLE']

# put the full path and file name of the file you want to store your "already
# followed" list in
ALREADY_FOLLOWED_FILE = "already-followed.csv"

t = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
            API_KEY, API_SECRET))


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


def auto_follow(q, count=100, result_type="recent"):
    """
        Follows anyone who tweets about a specific phrase (hashtag, word, etc.)
    """

    result = search_tweets(q, count, result_type)

    to_follow = set()

    for tweet in result["statuses"]:
        if tweet["user"]["screen_name"] == TWITTER_HANDLE:
            continue
        print('@{}:\n{}\n'.format(
            tweet['user']['screen_name'],
            tweet['text']))
        to_follow.add(tweet['user']['id'])

    already_following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])

    to_follow -= already_following
    print("Following {} users".format(len(to_follow)))
    for twitter_id in to_follow:
        print(twitter_id)
        try:
            t.friendships.create(user_id=twitter_id, follow=True)
        except TwitterHTTPError as e:
            if 'blocked' not in str(e).lower():  # ignore block errors
                print(repr(e))
            else:
                raise


def auto_follow_followers():
    """
        Follows back everyone who's followed you
    """

    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])

    not_following_back = followers - following

    for user_id in not_following_back:
        try:
            t.friendships.create(user_id=user_id, follow=True)
        except Exception as e:
            print("error: %s" % (str(e)))


def auto_unfollow_nonfollowers():
    """
        Unfollows everyone who hasn't followed you back
    """

    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])

    # put user IDs here that you want to keep following even if they don't
    # follow you back
    users_keep_following = set([])

    not_following_back = following - followers

    # make sure the "already followed" file exists
    if not os.path.isfile(ALREADY_FOLLOWED_FILE):
        with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
            out_file.write("")

    # update the "already followed" file with users who didn't follow back
    already_followed = set(not_following_back)
    af_list = []
    with open(ALREADY_FOLLOWED_FILE) as in_file:
        for line in in_file:
            af_list.append(int(line))

    already_followed.update(set(af_list))
    del af_list

    with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
        for val in already_followed:
            out_file.write(str(val) + "\n")

    for user_id in not_following_back:
        if user_id not in users_keep_following:
            t.friendships.destroy(user_id=user_id)
            print("unfollowed %d" % (user_id))
