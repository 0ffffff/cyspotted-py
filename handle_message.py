from db import spottedDB, spotterDB, Query
#from main import client

def handle_msg(event, client):
    channel_id = event.get('channel')
    user = event.get('user')
    text = event.get('text')
    has_image = bool(event.get('files'))

    #if message contains mention of another user: log mentioned user as spotted in db, react with a check emoji
    if text and '<@' in text and has_image:
        mentioned_users = [word for word in text.split() if word.startswith('<@') and word.endswith('>')]
        for mentioned in mentioned_users:
            mentioned_user_id = mentioned[2:-1]  # Extract user ID from <@USERID>
            if mentioned_user_id not in spottedDB.all():
                spottedDB.insert({'user_id': mentioned_user_id, 'count': 1})
            if user not in spotterDB.all():
                spotterDB.insert({'user_id': user})
            else:
                User = Query()
                spottedDB.update({'count': spottedDB.get(User.user_id == mentioned_user_id)['count'] + 1}, User.user_id == mentioned_user_id) #this is ai generated no clue if it works or not
                spotterDB.update() #todo: figure out db update
        client.reactions_add(channel=channel_id, name='white_check_mark', timestamp=event.get('ts'))

    #add other commands, help and leaderboard
    elif text and text.lower() == '!help':
        help_text = ("*CySpotted Commands:*\n"
                     "`!help` - Show this help message\n"
                     "`!leaderboard` - Show the leaderboard of spotted users")
        client.chat_postMessage(channel=channel_id, text=help_text)
    elif text and text.lower() == '!leaderboard':
        
        #too lazy to implement leaderboard logic rn
        leaderboard_text = "Leaderboard feature coming soon!"
        client.chat_postMessage(channel=channel_id, text=leaderboard_text)

    # Example logic: If a user sends "spot <username>", add to spottedDB
    """if text and text.startswith("spot "):
        spotted_user = text.split(" ")[1]
        spottedDB.insert({'spotted_by': user, 'spotted_user': spotted_user})
        client.chat_postMessage(channel=channel_id, text=f"<@{user}> spotted <@{spotted_user}>!")"""