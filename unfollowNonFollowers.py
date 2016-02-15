from TwitterFollowBot import TwitterBot

print("Initializing TwitterBot...")
my_bot = TwitterBot()

#print("Synchronizing follows...")
#my_bot.sync_follows()

print("Auto-unfollowing the non-followers (or: PURGE THE NONBELIEVERS!!!)")
my_bot.auto_unfollow_nonfollowers()


print("Complete!")
