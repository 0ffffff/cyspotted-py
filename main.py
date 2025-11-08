import os
from slack_sdk import WebClient
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

from handle_message import handle_msg
import db

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
events = SlackEventAdapter(os.environ['SIGN_SECRET'],'/slack/events',app)

client = WebClient(token=os.environ['TOKEN'])

@events.on('message')
def message(payload):
    event = payload.get('event', {})
    handle_msg(event, client)

if __name__ == '__main__':
    app.run(debug=True)