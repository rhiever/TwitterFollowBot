from TwitterFollowBot import TwitterBot

print("Initializing TwitterBot...")
my_bot = TwitterBot()

print("Synchronizing follows...")
my_bot.sync_follows()


print("Complete!")
