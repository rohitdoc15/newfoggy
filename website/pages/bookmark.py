from twitter.account import Account

# Set your credentials
email, username, password = 'rohitdoc15@gmail.com', 'mullokamulla', 'Suckbuddy@69'

# Initialize account
account = Account(email, username, password)

# Fetch and print bookmarks
bookmarks = account.bookmarks()

tweet_ids = []

# Parse through the data
for bookmark in bookmarks:
    data = bookmark.get('data', {})
    timeline = data.get('bookmark_timeline_v2', {}).get('timeline', {})
    instructions = timeline.get('instructions', [])
    
    for instruction in instructions:
        entries = instruction.get('entries', [])
        
        for entry in entries:
            entry_id = entry.get('entryId')
            # Check if entry_id starts with 'tweet-'
            if entry_id.startswith('tweet-'):
                # Remove 'tweet-' from the entry_id and add to list
                tweet_ids.append(entry_id[6:])

# Print all tweet IDs
print(tweet_ids)
