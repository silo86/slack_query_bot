#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import errno
import logging
from flask import Flask, json, request, Response, jsonify, make_response
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from mails import Mail
from verBackups import verBackups
from checkDB import checkDB
from expedienteDigital import expedienteDigital
from doQuery import queries
from info import info
from queryList import queryList
from executeQuery import execute
from pull import changes
from push import push
import datetime 
import threading

#crea la carpeta output si no existe
try:
    os.mkdir('output')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

#guarda en path la ruta donde se guardaran los archivos de salida
cwd = os.getcwd()
global path
global info_path
path = os.path.join(cwd,"output")
info_path = os.path.join(cwd,"info")
query_path = os.path.join(cwd,'queries')




# inicializa la app slack para hostear el adaptador de eventos
app = Flask(__name__)

# Crea un adaptador de eventos y lo registra como endpoint en slack para consumir eventos.
#linux
#slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)
#windows
slack_events_adapter = SlackEventAdapter(os.getenv("SLACK_EVENTS_TOKEN"), "/slack/events", app)

# Inicializa un cliente Web API
#slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))
slack_web_client = WebClient(token=os.getenv("SLACK_TOKEN"))



def get_mails(channel):
    """muestra los mails de los miembros de la oficina
    """
    # Instancia un coinbot
    mail_bot = Mail(channel)

    # Obtiene el mensaje
    message = mail_bot.get_message_payload()

    # Postea el mensaje en slack
    slack_web_client.chat_postMessage(**message)

def get_dbs_status(channel):
    query_bot = checkDB(channel)
    message = query_bot.get_message_payload()
    slack_web_client.chat_postMessage(**message)

def get_query(channel,**kwargs):
    #### variables ###
    fuero = kwargs['fuero']
    keyword = kwargs['keyword']
    if keyword[len(keyword)-1] == '_': #si el keyword termina en _ no tiene parametros
        parameters = False
    else:
        parameters = True
    query_bot = queries(channel,**kwargs)
    message = query_bot.get_message_payload(**kwargs)
    print(message)
    if parameters == True:
        try:
            fechadesde = kwargs['fechadesde']
            fechahasta = kwargs['fechahasta']
            filename = f'{keyword}_{fuero}_desde_{fechadesde}_hasta_{fechahasta}.xlsx'
            title = f'{keyword}_{fuero}_desde_{fechadesde}_hasta_{fechahasta}.xlsx'
            file= path + '/' + f'{keyword}_{fuero}_desde_{fechadesde}_hasta_{fechahasta}.xlsx'
        except(KeyError, NameError):
            pass
    else:
        filename = f'{keyword}_{fuero}.xlsx'
        title = f'{keyword}_{fuero}.xlsx'
        file= path + '/' + f'{keyword}_{fuero}.xlsx'
    #### sube el archivo excel al canal ####
    slack_web_client.files_upload(channels = channel,
          filetype= 'xlsx',
          filename= filename,
          title= title,
          file= file)

def get_executeQuery(channel,**kwargs):
    #### variables ###
    fuero = kwargs['fuero']
    _query = kwargs['_query']

    query_bot = execute(channel,**kwargs)
    message = query_bot.get_message_payload(**kwargs)

    filename = f'response_{fuero}.xlsx'
    title = f'response_{fuero}.xlsx'
    file= path + '/' + f'response_{fuero}.xlsx'
    #### sube el archivo excel al canal ####
    slack_web_client.files_upload(channels = channel,
          filetype= 'xlsx',
          filename= filename,
          title= title,
          file= file)

def get_verBackups(channel,fuero):
#    fuero = kwargs['fuero']
    query_bot = verBackups(channel)
    message = query_bot.get_message_payload(fuero)
    slack_web_client.chat_postMessage(**message)

def get_expteDigital(channel):
    query_bot = expedienteDigital(channel)
    message = query_bot.get_message_payload()
    slack_web_client.chat_postMessage(**message)

def get_changes(channel):
    query_bot = changes(channel)
    message = query_bot.get_message_payload()
    slack_web_client.chat_postMessage(**message)

def push_to_remote(channel,**kwargs):
    query_bot = push(channel,**kwargs)
    message = query_bot.get_message_payload(**kwargs)
    slack_web_client.chat_postMessage(**message)

def get_info(channel):
    query_bot = info(channel)
    message = query_bot.get_message_payload()
    slack_web_client.chat_postMessage(**message)
    slack_web_client.files_upload(channels = channel,
          filetype='png',
          filename=f'image.png',
          title= f'como consultar',
          file= info_path + '/' + f'Image.png')

def get_queryList(channel):
    ''' obtiene la lista de queries disponibles'''
    query_bot = queryList(channel)
    message = query_bot.get_message_payload()
    slack_web_client.chat_postMessage(**message)

def findsql(directory):
    ''' guarda los archivos .sql en una lista'''
    sqls = []
    for root,dir,file in os.walk(os.getcwd()):
        for name in file:
            if directory in os.path.join(root,name): #ask if the directory is in the tree
                if (name.find('.sql')>0):# ask if there are files .sql in the folder
#                    print(os.path.join(root,name) )
                    sqls.append(name)
        for name in dir:
            if directory in os.path.join(root,name): #ask if the directory is in the tree
                if (name.find('.sql')>0): # ask if there are files .sql in the folder
#                    print(os.path.join(root,name) )
                    pass
    return sqls

@slack_events_adapter.on("message")
def event_response(payload):                
    """endpoint que recibe todos los eventos"""
    # obtiene el request de slack
    event = payload.get("event", {})
    slack_request = request.form

    # empieza un nuevo trhead    
    x = threading.Thread(
            target = message,
            args = (payload,)
        )
    x.start()

    ## responde a slack con un mensaje rapido
    # y termina el thread principal para este request
    print('_procesando_')

    text = f'_Procesando..._'
    channel_id = event.get("channel")
    mensaje = {"type": "section", "text": {"type": "mrkdwn", "text": text}},
    return {
            "X-Slack-No-Retry": 1, 
            "channel": channel_id,
            "text": text
        }
    slack_web_client.chat_postMessage(**mensaje)
    return "Processing information.... please wait"

def message(payload):
    """Parse the message event, and if the activation string is in the text
    """
    dia = datetime.datetime.now()
    hoy = dia.strftime("%Y") + dia.strftime("%m") + dia.strftime("%d")
    with app.test_request_context():
        headers = request.headers
        # obtiene el evento del payload
        event = payload.get("event", {})

        # obtiene el texto del evento
        text = event.get("text")

        def get_parameters(text):
            ''' devuelve la lista de parametros de acuerdo al texto ingresado'''
            lista = []
            lista = text.split(' ')
            for i,s in enumerate(lista):
                if "sae" in s or "oga" in s:
                    index = i
                    fuero = lista[index]
                    break
            
            for i,s in enumerate(lista):
                if "desde" in s and not "desde_" in s:
                    index = i
                    fechadesde = lista[index + 1]
                    break
                else:
                    fechadesde = '20200101'
            
            for i,s in enumerate(lista):
                if "hasta" in s or " al" in s:
                    index = i
                    fechahasta = lista[index + 1]
                    break
                else:
                    if '_' in fuero: #toma la fecha hasta del backup
                        fechahasta = fuero[fuero.find('_') + 1:]
                    else:
                        fechahasta = hoy

            for i,s in enumerate(lista):
                if "cantidad" in s or "total" in s:
                    index = i
                    tipo = lista[index]
                    break
                else:
                    tipo = 'listado'
            print(f'::::::::::PARAMETROS:::::::\n fuero: {fuero},fechadesde: {fechadesde},fechahasta: {fechahasta}')
            return fuero,fechadesde,fechahasta

        # Revisa si la frase de activacion esta en el texto del mensaje
        if 'output' in cwd:
            os.chdir('..')
        # Guarda los .sql en la lista sqls
        sqls = findsql(query_path)
        # Guarda la lista con nombres de las consultas en la lista names
        names = []
        for sql in sqls:
            dot = sql.find('.')
            name = sql[:dot]
            names.append(name)
        # obtiene los parametros y ejecuta la consulta
        textlist = text.split(' ')
        for name in names:
            if name == textlist[0].lower():
                keyword = name
                fuero,fechadesde,fechahasta = get_parameters(text)
                channel_id = event.get("channel")
                return get_query(channel_id, fuero = fuero, fechadesde = fechadesde, fechahasta = fechahasta, keyword = keyword)


        if "-mails" in text.lower():
            channel_id = event.get("channel")
            data = get_mails(channel_id)
            headers = request.headers
            return data

        if "-status" in text.lower():
            channel_id = event.get("channel")
            data = get_dbs_status(channel_id)
            return data
            
        
        if "-backups" in text.lower():
            lista = []
            lista = text.split(' ')
            fuero = ''
            for i,s in enumerate(lista):
                if "sae" in s:
                    index = i
                    fuero = lista[index]
                    print(fuero)
                    break
            channel_id = event.get("channel")
            return get_verBackups(channel_id, fuero)
        
        if "-consultas" in text.lower():
            channel_id = event.get("channel")
            return get_queryList(channel_id)

        if "-expediente_digital" in text.lower():
            channel_id = event.get("channel")
            return get_expteDigital(channel_id)

        if "-info" in text.lower():
            channel_id = event.get("channel")
            return get_info(channel_id)

        if "-pull" in text.lower():
            channel_id = event.get("channel")
            return get_changes(channel_id)

        if "-push" in text.lower():
            message_begin_character = text.find('"')
            message_text = text[message_begin_character + 1:len(text)-1]
            channel_id = event.get("channel")
            return push_to_remote(channel_id, message_text = message_text)

        if "-ejecutar" in text.lower():
            query_begin_character = text.find('¡')
            query_end_character = text.find('!')
            _query = text[query_begin_character + 1:query_end_character]
            lista = []
            lista = text[query_end_character:].split(' ')
            print(lista)
            for i,s in enumerate(lista):
                if "sae" in s or "oga" in s:
                    index = i
                    fuero = lista[index]
                    break
            print(f'\nESTE ES EL TEXTO DEL MENSAJE {_query}')
            channel_id = event.get("channel")
            return get_executeQuery(channel_id, fuero = fuero,_query = _query)

 
if __name__ == "__main__":
    # Instancia un objeto de logging
    logger = logging.getLogger()

    # Setea el log level a debug. 
    logger.setLevel(logging.DEBUG)

    # Agrega StreamHandler como logging handler
    logger.addHandler(logging.StreamHandler())

    # Run your app on your externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host='0.0.0.0', port=3000)

