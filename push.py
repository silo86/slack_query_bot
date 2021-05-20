# import the random library to help us generate the random numbers
from flask import Response,jsonify
import subprocess as cmd
import os
# Create the Mail Class
class push:

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
    def __init__(self, channel,**kwargs):
        self.message_text = kwargs['message_text']
        self.channel = channel

    def _push_to_remote(self,**kwargs):
        commit_message = kwargs['message_text']
        try:
            cmd.run('git add .')
            cmd.run(f'git commit -m "{commit_message}"')
            cmd.run('git push origin master')
            text = f''' _Repositorio remoto actualizado_'''
        except Exception as e:
            text = f'''_Error al actualizar repositorio remoto_ {e}'''

        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        
    # Craft and return the entire message payload as a dictionary.
    
    def get_message_payload(self,**kwargs):
        return {
            "X-Slack-No-Retry": 1, 
            "channel": self.channel,
            "blocks": [
                self.MAIL_BLOCK,
                *self._push_to_remote(**kwargs),
            ],
        }
