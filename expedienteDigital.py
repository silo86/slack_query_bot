# import the random library to help us generate the random numbers
from flask import Response,jsonify
# Create the Mail Class
class expedienteDigital:

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

    def _get_fechas(self):

        text = f'''
_*Implementación del expediente digital en Capital:*_\n
            _•Fuero Civil y Comercial Común : 18/05/2019_
            _•Fuero Cobros y Apremios : 19/06/2020_
            _•Fuero Familia y Sucesiones : 26/06/2020_
            _•Fuero Documentos y Locaciones : 03/07/2020_
            _•Centro de Mediación : 03/07/2020_
            _•Fuero Contencioso Administrativo : 08/07/2020_
            _•Fuero del Trabajo : 17/07/2020_
            _•Fuero Penal - Conclusional : 01/09/2020_
            _•Originarios Corte y resto : 01/09/2020_
            _•Resto de expedientes elevados a Corte : --/--/----_
            
_*Implementación del expediente digital en Concepcion:*_\n
            _•Fuero Cobros y Apremios : 18/05/2019_
            _•Fuero Civil y Comercial Común : 23/06/2020_
            _•Fuero Familia y Sucesiones : 26/06/2020_
            _•Fuero Documentos y Locaciones : 03/07/2020_
            _•Centro de Mediación : 03/07/2020_
            _•Fuero del Trabajo : 17/07/2020_
            _•Fuero Penal - Conclusional : 24/07/2020_
            
  
_*Implementación del expediente digital en Monteros:*_\n
            _•Fuero Civil y Comercial Común : 23/06/2020_
            _•Fuero Familia y Sucesiones : 26/06/2020_
            _•Fuero Documentos y Locaciones : 03/07/2020_
            _•Centro de Mediación : 03/07/2020_
            _•Fuero del Trabajo : 17/07/2020_
            _•Fuero Penal - Conclusional : 01/09/2020_
        '''

        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        
    # Craft and return the entire message payload as a dictionary.
    
    def get_message_payload(self):
        return {
            "X-Slack-No-Retry": 1, 
            "channel": self.channel,
            "blocks": [
                self.MAIL_BLOCK,
                *self._get_fechas(),
            ],
        }
