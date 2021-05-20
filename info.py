# import the random library to help us generate the random numbers
from flask import Response,jsonify
# Create the Mail Class
class info:

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

    def _get_info(self):

        text = f'''
• *-status*:  _verifica si las bases en DDEDBS estan actualizadas_
• *-backups*:  _muestra los backups restaurados en pc_vero_ 
uso: -backups [base]
• *-mails*:  _listado de mails_
• *-expediente_digital*:  _fechas de implementacion del expediente digital_
• *-consultas*:  _muestra el listado de consultas_
• *-ejecutar*: corre una consulta en una base  
uso: -ejecutar ¡[query]! [base]
• *-pull*: _actualiza el listado de consultas_  
• *-push*: _commit de los datos locales al repositorio remoto_ 
uso: -push "[mensaje]" 
        '''

        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        
    # Craft and return the entire message payload as a dictionary.
    
    def get_message_payload(self):
        return {
            "X-Slack-No-Retry": 1, 
            "channel": self.channel,
            "blocks": [
                self.MAIL_BLOCK,
                *self._get_info(),
            ],
        }
