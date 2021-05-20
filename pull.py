# import the random library to help us generate the random numbers
from flask import Response,jsonify
import git
import os
# Create the Mail Class
class changes:

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

    def _get_changes(self):
        try:
            git.Repo(os.getcwd()).remotes.origin.pull('master')
            text = f''' _Listado de consultas actualizado_'''
        except Exception as e:
            text = f'''_Error al actualizar el listado de consultas_ {e}'''

        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        
    # Craft and return the entire message payload as a dictionary.
    
    def get_message_payload(self):
        return {
            "X-Slack-No-Retry": 1, 
            "channel": self.channel,
            "blocks": [
                self.MAIL_BLOCK,
                *self._get_changes(),
            ],
        }
