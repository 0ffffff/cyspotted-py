from db import spottedDB, spotterDB, User
from tinydb.operations import increment

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
            if not spottedDB.contains(User.user_id == mentioned_user_id) and not spotterDB.contains(User.user_id == user):
                spottedDB.insert({'user_id': mentioned_user_id, 'count': 1})
                spotterDB.insert({'user_id': user, 'count': 1})
            elif not spottedDB.contains(User.user_id == mentioned_user_id):
                spottedDB.insert({'user_id': mentioned_user_id, 'count': 1})
                spotterDB.update(increment('count'), User.user_id == user)
            elif not spotterDB.contains(User.user_id == user):
                spottedDB.update(increment('count'), User.user_id == mentioned_user_id)
                spotterDB.insert({'user_id': user, 'count': 1})
            else:
                spottedDB.update(increment('count'), User.user_id == mentioned_user_id)
                spotterDB.update(increment('count'), User.user_id == user)

        client.reactions_add(channel=channel_id, name='white_check_mark', timestamp=event.get('ts')) #lol ts pmo

    #add other commands, help and leaderboard
    elif text and text.lower() == '!help':
        help_text = ("*CySpotted Commands:*\n"
                     "`!help` - Show this help message\n"
                     "`!spotboard X` - Show the top X people that have been spotted\n"
                     "`!caughtboard X` - Show the top X spotters")
        client.chat_postMessage(channel=channel_id, text=help_text)
    elif text and text.startswith('!spotboard'):
        try:
            num_spots = text.split(' ')[1]
        except IndexError:
            num_spots = 10

        #retrieve top num_spots users from spottedDB, sorted by 'count' value:
        leaderboard = spottedDB.all()
        leaderboard.sort(key=lambda x: x['count'], reverse=True)
        leaderboard = leaderboard[:int(num_spots)]

        leaderboard_text = "*Spotboard:*\n"
        for entry in leaderboard:
            leaderboard_text += f"<@{entry['user_id']}> - {entry['count']} spots\n"

        client.chat_postMessage(channel=channel_id, text=leaderboard_text)

    elif text and text.startswith('!caughtboard'):
        try:
            num_spots = text.split(' ')[1]
        except IndexError:
            num_spots = 10

        #retrieve top num_spotters users from spotterDB, sorted by 'count' value:
        leaderboard = spotterDB.all()
        leaderboard.sort(key=lambda x: x['count'], reverse=True)
        leaderboard = leaderboard[:int(num_spots)]

        leaderboard_text = "*Caughtboard:*\n"
        for entry in leaderboard:
            leaderboard_text += f"<@{entry['user_id']}> - {entry['count']} catches\n"

        client.chat_postMessage(channel=channel_id, text=leaderboard_text)