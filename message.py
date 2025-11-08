from db import spottedDB, spotterDB
from main import client

def handle_message(event):
    channel_id = event.get('channel')
    user = event.get('user')
    text = event.get('text')

    # Example logic: If a user sends "spot <username>", add to spottedDB
    """if text and text.startswith("spot "):
        spotted_user = text.split(" ")[1]
        spottedDB.insert({'spotted_by': user, 'spotted_user': spotted_user})
        client.chat_postMessage(channel=channel_id, text=f"<@{user}> spotted <@{spotted_user}>!")"""