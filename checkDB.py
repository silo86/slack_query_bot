# import librarys
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
import sandesh

# Crea la clase
class checkDB:

    # Crea una constante que contiene el texto por defecto para el mensaje
    BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "."
            ),
        },
    }

    # EL constructor de la clase lleva como parametro el canal
    def __init__(self, channel):
        self.channel = channel

    def _get_query(self):
        hostname = os.getenv("ddedbs_ip")
        username = os.getenv("ddedbs_username")
        password = os.getenv("ddedbs_pass")
        

        con = psycopg2.connect(host=hostname, user=username, password=password, dbname='saeciv')
        lista_db = '''SELECT datname FROM pg_database WHERE datistemplate = false '''
        bases = pd.read_sql(lista_db,con)


        dbs = [base for base in bases.datname if base.startswith('sae') and not base.startswith('saemed') and not base.startswith('saeoga') and base not in ('saejes','saepjt','saeori','saepencam','saesup')]

        dfs = pd.DataFrame()
        query = ''' select current_database() as base,max(febo) as febo,max(fepf) as fepf, max(fefi) as fefi from public."HIST" '''
        for  fila in dbs:
            print(f'Iniciando lectura de base de datos {fila}', end='\n')
            msg = ''
            msg = f'Iniciando lectura de base de datos {fila}'
            sandesh.send(msg, webhook = "https://hooks.slack.com/services/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")
            con_b = psycopg2.connect(host=hostname, user=username, password=password, dbname = fila)
            df = pd.read_sql(query,con_b)
            dfs = dfs.append(df)
            con_b.close()

        hoy = datetime.datetime.now() 
        #ayer = datetime.datetime.now() - datetime.timedelta(days=1)
        #si es lunes, toma ayer el viernes anterior
        if hoy.weekday() == 0:
            d = datetime.datetime.now() - datetime.timedelta(days=1)
            s = datetime.datetime.now() - datetime.timedelta(days=2)
            v = datetime.datetime.now() - datetime.timedelta(days=3)
            dias = [hoy,v,s,d]
            dias = [dia.strftime("%Y") + dia.strftime("%m") + dia.strftime("%d") for dia in dias]
        else:
            ayer = datetime.datetime.now() - datetime.timedelta(days=1)
            ayer = ayer.strftime("%Y") + ayer.strftime("%m") + ayer.strftime("%d")
            hoy = hoy.strftime("%Y") + hoy.strftime("%m") + hoy.strftime("%d")
            dias = [hoy,ayer]

        msg= ''
        for i in range(dfs.shape[0]):
            if((dfs.febo.iloc[i] in dias or  dfs.fepf.iloc[i] in dias or  dfs.fefi.iloc[i] in dias) == False):
                msg += f"_La base {dfs.base.iloc[i]} no está actualizada, último movimiento: febo: {dfs.febo.iloc[i]} ,fepf: {dfs.fepf.iloc[i]}, fefi: {dfs.fefi.iloc[i]}_ \n"
        if msg == '':
            msg = '_Todas las bases estan actualizadas_'
        #text = f"The result is {results}"

        return {"type": "section", "text": {"type": "mrkdwn", "text": msg}},

    # Crea y devuelve el payload como un diccionario.
    def get_message_payload(self):
        return {
            "X-Slack-No-Retry": 1,
            "channel": self.channel,
            "blocks": [
                self.BLOCK,
                *self._get_query(),
            ],
        }