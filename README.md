[![PyPI version](https://badge.fury.io/py/TwitterFollowBot.svg)](https://badge.fury.io/py/TwitterFollowBot)
![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)
![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)
![License](https://img.shields.io/badge/license-GPLv3-blue.svg)

# Twitter Bot

[![Join the chat at https://gitter.im/rhiever/TwitterFollowBot](https://badges.gitter.im/rhiever/TwitterFollowBot.svg)](https://gitter.im/rhiever/TwitterFollowBot?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A Python bot that automates several actions on Twitter, such as following users and favoriting tweets.

## Notice: Repository is no longer being maintained

Twitter has started cracking down heavily on users who use bots like this one to follow users or favorite tweets en masse. For that reason, I am no longer developing this code repository but will leave it up for anyone who wants to use it as a code base for future projects. Please respect the [software license](https://github.com/rhiever/TwitterFollowBot/blob/master/LICENSE) if you use the code from this repository.

## Disclaimer

I hold no liability for what you do with this bot or what happens to you by using this bot. Abusing this bot *can* get you banned from Twitter, so make sure to read up on [proper usage](https://support.twitter.com/articles/76915-automation-rules-and-best-practices) of the Twitter API.

## Installation

You can install the Twitter Follow Bot using `pip`:

    pip install TwitterFollowBot

## Dependencies

You will need to install Python's [python-twitter](https://github.com/sixohsix/twitter/) library:

    pip install twitter

Although this library should be installed along with the Twitter Follow Bot if you used `pip`.

You will also need to create an app account on https://dev.twitter.com/apps

1. Sign in with your Twitter account
2. Create a new app account
3. Modify the settings for that app account to allow read & write
4. Generate a new OAuth token with those permissions

Following these steps will create 4 tokens that you will need to place in the configuration file discussed below.

## Usage

### Configuring the bot

Before running the bot, you must first set it up so it can connect to the Twitter API. Create a config.txt file and fill in the following information:

    OAUTH_TOKEN:
    OAUTH_SECRET:
    CONSUMER_KEY:
    CONSUMER_SECRET:
    TWITTER_HANDLE:
    ALREADY_FOLLOWED_FILE:already-followed.txt
    FOLLOWERS_FILE:followers.txt
    FOLLOWS_FILE:following.txt
    USERS_KEEP_FOLLOWING:
    USERS_KEEP_UNMUTED:
    USERS_KEEP_MUTED:
    FOLLOW_BACKOFF_MIN_SECONDS:10
    FOLLOW_BACKOFF_MAX_SECONDS:60
    
`OAUTH_TOKEN`, `OAUTH_SECRET`, `CONSUMER_KEY`, `CONSUMER_SECRET` are your API keys that you received from creating your app account. `TWITTER_HANDLE` is your Twitter name, case-sensitive.

You can change the `FILE` entries if you want to store that information in a specific location on your computer. By default, the files will be created in your current directory.

Add comma-separated Twitter user IDs to the `USERS_KEEP` entries to:

* `USERS_KEEP_FOLLOWING`: Keep following these users even if they don't follow you back.

* `USERS_KEEP_UNMUTED`: Keep these users unmuted (i.e., you receive a mobile notification when they tweet)

* `USERS_KEEP_MUTED`: Keep these users muted (i.e., you don't receive a mobile notification when they tweet)

For example:

    ...
    FOLLOWS_FILE:following.txt
    USERS_KEEP_FOLLOWING:1234,1235,1236
    USERS_KEEP_UNMUTED:
    ...
    
You can look up a users' Twitter ID [here](http://tweeterid.com/).

### Create an instance of the bot

To create an instance of the bot:

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    
By default, the bot will look for a configuration file called `config.txt` in your current directory.
    
If you want to use a different configuration file, pass the configuration file to the bot as follows:

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot("my-other-bot-config.txt")
    
Note that this allows you to run multiple instances of the bot with different configurations, for example if you run multiple Twitter accounts:

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    my_other_bot = TwitterBot("my-other-bot-config.txt")

### Syncing your Twitter following locally

Due to Twitter API rate limiting, the bot must maintain a local cache of all of your followers so it doesn't use all of your API time looking up your followers. It is highly recommended to sync the bot's local cache daily:

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    my_bot.sync_follows()
    
The bot will create cache files where you specified in the configuration file.
    
**DO NOT** delete the cache files ("followers.txt", "follows.txt", and "already-followed.txt" by default) unless you want to start the bot over with a fresh cache.

### Automating Twitter actions with the bot

This bot has several functions for programmatically interacting with Twitter:

#### Automatically follow any users that tweet something with a specific phrase

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    my_bot.auto_follow("phrase")
    
You can also search based on hashtags:

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    my_bot.auto_follow("#hashtag")
  
By default, the bot looks up the 100 most recent tweets. You can change this number with the `count` parameter:

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    my_bot.auto_follow("phrase", count=1000)
    
#### Automatically follow any users that have followed you

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    my_bot.auto_follow_followers()

#### Automatically follow any users that follow a user
    
    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot() 
    my_bot.auto_follow_followers_of_user("jack", count=1000)

#### Automatically favorite any tweets that have a specific phrase

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    my_bot.auto_fav("phrase", count=1000)
    
#### Automatically retweet any tweets that have a specific phrase

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    my_bot.auto_rt("phrase", count=1000)

#### Automatically unfollow any users that have not followed you back

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    my_bot.auto_unfollow_nonfollowers()
  
If there are certain users that you would like to not unfollow, add their user id to the USERS_KEEP_FOLLOWING list.

You will need to manually edit the code if you want to add special users that you will keep following even if they don't follow you back.

#### Automatically unfollow all users.

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    my_bot.auto_unfollow_all_followers()
  


#### Automatically mute all users that you have followed

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    my_bot.auto_mute_following()

You will need to manually edit the code if you want to add special users that you will not mute.

#### Automatically unmute everyone you have muted

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    my_bot.auto_unmute()
    
You will need to manually edit the code if you want to add special users that will remain muted. 

#### Post a tweet on twitter

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    my_bot.send_tweet("Hello world!")

#### Automatically add users tweeting about something to one of your list

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    my_bot.auto_add_to_list("#TwitterBot", "twitterbot-list", count=10)
    
In the example above, the bot will try to add 10 users to the twitterbot-list that are tweeting #TwitterBot.

Remember that the max number of users in a list is 5000.
    
## Have questions? Need help with the bot?

If you're having issues with or have questions about the bot, [file an issue](https://github.com/rhiever/TwitterFollowBot/issues) in this repository so one of the project managers can get back to you. **Please [check the existing (and closed) issues](https://github.com/rhiever/TwitterFollowBot/issues?q=is%3Aissue) to make sure your issue hasn't already been addressed.**
