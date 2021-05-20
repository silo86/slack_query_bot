# import the random library to help us generate the random numbers
import random
from flask import Response,jsonify
# Create the Mail Class
class Mail:

    # Create a constant that contains the default text for the message
    MAIL_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "....\n\n"
            ),
        },
    }

    # El constructor de la clase. Toma el nombre del canal como parametro
    # y lo setea como una variable de instancia
    def __init__(self, channel):
        self.channel = channel

    def _get_mails(self):

        text = f'• vilencina@gmail.com\n• verolayana79@gmail.com\n• amiradip0@gmail.com\n• ortizjavier77@gmail.com\n• varasmariano@gmail.com\n• abrandsal@gmail.com\n• manugd90@gmail.com'

        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        
    # Craft and return the entire message payload as a dictionary.
    
    def get_message_payload(self):
        return {
            "X-Slack-No-Retry": 1, 
            "channel": self.channel,
            "blocks": [
                self.MAIL_BLOCK,
                *self._get_mails(),
            ],
        }
