from twitter import Twitter, OAuth, TwitterHTTPError

# put your tokens, keys, secrets, and twitter handle in the following variables
OAUTH_TOKEN = ""
OAUTH_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
TWITTER_HANDLE = ""

t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

def search_tweets(q, count=100, result_type="recent"):
    return t.search.tweets(q=q, result_type=result_type, count=count)

def auto_fav(q, count=100, result_type="recent"):
    result = search_tweets(q, count, result_type)
    
    for tweet in result['statuses']:
        try:
            result = t.favorites.create(_id=tweet['id'])
            print "Favorited: %s" % (result['text'])
        # when you have already favorited a tweet this error is thrown
        except TwitterHTTPError as e:
            print "Error: ", e

def auto_follow(q, count=100, result_type="recent"):
    result = search_tweets(q, count, result_type)
    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    
    for tweet in result['statuses']:
        try:
            if tweet['user']['screen_name'] != TWITTER_HANDLE and tweet['user']['id'] not in following:
                t.friendships.create(user_id=tweet['user']['id'], follow=True)
                following.update(set([tweet['user']['id']]))
                
                print "followed " + tweet['user']['screen_name']
        except TwitterHTTPError as e:
            print "Error: ", e
        
def auto_unfollow_nonfollowers():
    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])
    
    # put user IDs here that you want to keep following even if they don't follow you back
    users_keep_following = set([])
    
    not_following_back = following - followers
    
    for userid in not_following_back:
        if userid not in users_keep_following:
            t.friendships.destroy(user_id=userid)
