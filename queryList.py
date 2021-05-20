# import the random library to help us generate the random numbers
from flask import Response,jsonify
import os
# Create the Mail Class
class queryList:

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

    def _get_query_list(self):

        def findsql(directory):
            ''' guarda los archivos .sql en una lista'''
            sqls = []
            for root,dir,file in os.walk(os.getcwd()):
                for name in file:
                    if directory in os.path.join(root,name): #ask if the directory is in the tree
                        if (name.find('.sql')>0):# ask if there are files .sql in the folder
                            print(os.path.join(root,name) )
                            sqls.append(name)
                for name in dir:
                    if directory in os.path.join(root,name): #ask if the directory is in the tree
                        if (name.find('.sql')>0): # ask if there are files .sql in the folder
                            print(os.path.join(root,name) )
            return sqls
        sqls = findsql(os.path.join(os.getcwd(),'queries'))
        names = []
        for sql in sqls:
            dot = sql.find('.')
            name = sql[:dot]
            names.append(name)
        text = ''
        text_T = ''
        text_L = ''
        for name in names:
            if 'total' in name:
                text_T += f'     {name} \n'
            else:
                text_L += f'     {name} \n'
        text = f'''
• *_Listados_*:

{text_L}
• *_Totales_*:

{text_T}
        '''

        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        
    # Craft and return the entire message payload as a dictionary.
    
    def get_message_payload(self):
        return {
            "X-Slack-No-Retry": 1, 
            "channel": self.channel,
            "blocks": [
                self.MAIL_BLOCK,
                *self._get_query_list(),
            ],
        }
