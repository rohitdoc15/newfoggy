from twitter.scraper import Scraper
from twitter.account import Account

ct0_cookie = '1623c9d82d1a7f1dae0f2799c6bc6de90937542a058b5fbe297baeb3e3af0297f7371d3faeaa8c30d6f3983f2e148aca463c9aa43e662c808c6518660638e095943eb534673889725778b1901e2c97ea'
auth_token_cookie = '051714fb57f27e9e747e1eef8817cfb10edb637b'

scraper_instance = Scraper(cookies={"ct0": ct0_cookie, "auth_token": auth_token_cookie})
account = Account(cookies={"ct0": ct0_cookie, "auth_token": auth_token_cookie})

# List of usernames to lookup
usernames_to_lookup = [ 'PopCrave','HappyPunch','WatcherGuru' ,'stats_feed','popbase' ,'CricCrazyJohns','mufaddal_vohra' , 'taran_adarsh']  # Add more usernames as required

def find_key(nested_dict, target_key):
    """A function to find a key in a deeply nested dictionary."""
    for key, value in nested_dict.items():
        if key == target_key:
            yield value
        elif isinstance(value, dict):
            yield from find_key(value, target_key)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    yield from find_key(item, target_key)

# Loop through each username and perform operations
for username in usernames_to_lookup:
    # Get user data for the current username
    user_data = scraper_instance.users(screen_names=[username])

    print(f"User data for {username}: {user_data}")  # Debug line to check the user data

    # Check if we received valid user data
    if not user_data or 'data' not in user_data[0] or 'user' not in user_data[0]['data'] or 'result' not in user_data[0]['data']['user']:
        print(f"Failed to retrieve data for {username}")
        continue  # Skip to the next username

    # Extract the user ID from the nested dictionary structure using rest_id
    user_ids = [user_data[0]['data']['user']['result']['rest_id']]  # This should be a list

    # Get tweets for the current user ID
    tweets_data = scraper_instance.tweets(user_ids, limit = 1)

    # Process the tweets as needed
    for tweets in tweets_data:
        # print(tweets)  # Add this line to print the entire tweet data response
        
        for full_text in find_key(tweets, 'full_text'):
            print(full_text)
        
        # Print all tweet IDs and bookmark them
        for entry_id in find_key(tweets, 'entryId'):
            tweet_id = entry_id.split('-')[-1]  # Get the last part of the entryId string
            print(f'Tweet ID: {tweet_id}')
            
            # Bookmark the tweet
            try:
                account.bookmark(tweet_id)
                print(f'Successfully bookmarked tweet ID: {tweet_id}')
            except Exception as e:
                print(f'Failed to bookmark tweet ID: {tweet_id}. Error: {str(e)}')