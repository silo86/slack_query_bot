# librerias
from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import datetime
import os
import glob
os.path.abspath(os.getcwd())
import sys
import errno
from pathlib import Path

# Crea la clase
class verBackups:

    # Crea una constante que contiene el texto por defecto para el mensaje
    BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "_Procesando..._\n\n"
            ),
        },
    }

    # EL constructor de la clase lleva como parametro el canal
#    def __init__(self, channel, fuero , fechadesde, fechahasta):
    def __init__(self, channel):
        self.channel = channel
    #    self.fuero = fuero
    #    self.fechadesde = '20200101'
    #    self.fechahasta = '20201031'

    def _get_query(self,fuero):
        #datos
        hostname_vero = os.getenv("pc_vl_ip")
        username = os.getenv("pc_vl_username")
        password = os.getenv("pc_vl_pass")
        #tabla = '"ADJU"'
        #update = "UPDATE  public.""{0}"" SET vers = '{1}'"
        #select = "SELECT vers from public.""{0}"" "

        con = psycopg2.connect(host=hostname_vero, user=username, password=password)

        lista_db = 'SELECT datname FROM pg_database WHERE datistemplate = false'
        bases = pd.read_sql(lista_db,con)
        bases = [base for base in bases.datname if base.startswith('sae') and base.startswith(fuero) ]
        bases.sort()
        msg = ''
        for base in bases:
            msg += f'• {base}\n'
        
#        bases = '- Detective Chimp\n- Bouncing Boy\n- Aqualad'
        return {"type": "section", "text": {"type": "mrkdwn", "text": msg}},
        #return option_groups

    # Crea y devuelve el payload como un diccionario.
    def get_message_payload(self,fuero):
        return {
            "X-Slack-No-Retry": 1, 
            "channel": self.channel,
            "blocks": [
                self.BLOCK,
                *self._get_query(fuero),
            ],
        }