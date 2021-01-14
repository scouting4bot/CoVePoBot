"""
This script contains the definition of routes and views for the application.
"""
import sys
import hashlib
import time
import random
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from CoVePoBot import app, logger, app_config#, telegram_config
#from CoVePoBot.application.errors import ValidationError
#from CoVePoBot.application.telegram.notify import notify
#from CoVePoBot.application.telegram.setup import setup_api
#from CoVePoBot.application.telegram.webhook import telegram_webhook_api

app_full_name = app_config["app_full_name"]
app_short_name = app_config['app_short_name']
#telegram_bot_token = telegram_config["bot_token"]

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

#-----------------------------------------------------------------------
vote_session_list = {}
#-----------------------------------------------------------------------
@app.route('/')
def hello():
    """Renders a sample page."""
    return "Nessun servizio disponibile!"

#-----------------------------------------------------------------------
@app.route('/CoVePoBot/setup/aggiungi')
def setupCreateVoteSession():
    """ Creates a new vote session. """
    vote_id = request.args.get('id', '')
    otp_num = request.args.get('num', '')
    try:
        otp_num = int(otp_num)
    except ValueError:
        return "NUM non è un numero valido", 400

    msg, http_code = createVoteSession(vote_id, otp_num)
    return msg, http_code

#-----------------------------------------------------------------------
@app.route('/CoVePoBot/<vote_id>/secret')
@app.route('/CoVePoBot/<vote_id>/secrets')
@app.route('/CoVePoBot/<vote_id>/secrets/')
def getSecretCSV(vote_id):
    """ Return a list of activated secrets. """

    if vote_id is None or vote_id == '' or extractDictValue(vote_id, vote_session_list) is None:
        result = "votazione non valida"
        http_code = 409
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", http_code
    #check password
    psw = request.args.get('password', '')
    if psw is None or psw == '' or psw != vote_session_list[vote_id]["psw"]:
        return 'Non sei autorizzato', 403

    #create the requested csv
    return csvFromDict(vote_session_list[vote_id]["secrets"]), 200

#-----------------------------------------------------------------------
@app.route('/CoVePoBot/<vote_id>/otps')
@app.route('/CoVePoBot/<vote_id>/otps/')
def getOtpCSV(vote_id):
    """ Return a list of available otps. """

    if vote_id is None or vote_id == '' or extractDictValue(vote_id, vote_session_list) is None:
        result = "votazione non valida"
        http_code = 409
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", http_code

    #check password
    psw = request.args.get('password', '')
    if psw is None or psw == '' or psw != vote_session_list[vote_id]["psw"]:
        return 'Non sei autorizzato', 403

    #create the requested csv
    return csvFromDictOfAvailable(vote_session_list[vote_id]["otps"]), 200

#-----------------------------------------------------------------------
@app.route('/CoVePoBot/<vote_id>/otp/<otp>')
def autorizeOtp(vote_id, otp):
    """ Given an OTP, validates it and provides a secret. """
    if otp is None:
        otp = request.args.get('otp', '')
    msg, http_code = convertOtp(vote_id, otp)
    return msg, http_code

#-----------------------------------------------------------------------
@app.route('/CoVePoBot/<vote_id>/otp')
@app.route('/CoVePoBot/<vote_id>/otp/')
def autorizeOtpMissingOtp(vote_id):
    """ Given an OTP, validates it and provides a secret. """
    otp = request.args.get('otp', '')
    return autorizeOtp(vote_id, otp)

#-----------------------------------------------------------------------
def convertOtp(vote_id, otp):
    """ Check if the otp is valid. """

    #validate vote_id
    http_code = 200
    if vote_id is None or vote_id == '' or extractDictValue(vote_id, vote_session_list) is None:
        vote_id = ''
        result = "votazione non valida"
        http_code = 409
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", http_code
    #validate otp
    elif otp is None or otp == '':
        result = "Codice otp mancante"
        http_code = 400
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", http_code
    #check that the otp exists
    elif extractDictValue(otp, vote_session_list[vote_id]['otps']) is None or vote_session_list[vote_id]['otps'][otp] == 'expired':
        result = "Codice otp non valido"
        http_code = 403
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", http_code
    #convert otp into a secret
    else:
        result = getTimeHash(10)
        vote_session_list[vote_id]['otps'][otp] = 'expired'
        vote_session_list[vote_id]['secrets'][result] = 'enabled'
        print(vote_session_list)
        return "Il tuo codice è " + result + " e ti servirà per votare alla "+vote_id+".\n Attenzione! Non sarà possibile riprodurlo nuovamente. Perciò conservalo accuratamente e non perderlo", http_code


def createVoteSession(vote_id, otp_num):
    """ Adds a vote session to the vote_session_list """

    #check if the key already exists
    http_code = 200
    if vote_id is None or vote_id == '':
        return "ID non valido", 400
    elif extractDictValue(vote_id, vote_session_list) is not None:
        return "ID già in uso", 409
    else:
        isSuccess, result, psw = getNewVoteSession(vote_id, otp_num)
        if isSuccess:
            #update vote_session_list
            vote_session_list[vote_id] = result

            #extract the list of new otps to  return in the response
            otps_csv = csvFromDict(vote_session_list[vote_id]["otps"])
            return "Aggiunta la nuova sessione "+vote_id+". Usa come password per la gestione: "+psw+"\nGli otp disponibili sono:"+otps_csv, http_code
        else:
            http_code = 500
            return result, http_code


def csvFromDict(dict):
    """ Extract a Comma Separated List (CSV) string of keys in a dictionary """
    csv = ''
    for key in dict:
        csv = csv + key + ','
    if csv is not None or csv != '':
        csv = csv[:-1]
    return csv


def csvFromDictOfAvailable(dict):
    """ Extract a Comma Separated List (CSV) string of keys with value "available" in a dictionary """
    csv = ''
    for key in dict:
        if dict[key] == 'available':
            csv = csv + key + ','
    if csv is not None or csv != '':
        csv = csv[:-1]
    return csv


def getNewVoteSession(vote_id, otp_num):
    if vote_id is None or vote_id == '':
        psw = getTimeHash(10)
        return True, {"id":vote_id, "psw":psw}, psw
    else:
        otp_dict = {}
        otps = {}
        i = 0
        while i < otp_num:
            otps[getUid(otps, 6)] = "available"
            i += 1
        psw = getTimeHash(10)
        return True, {"id":vote_id, "psw":psw, "otps":otps, "secrets":{}}, psw


def getTimeHash(digits):
    #create hash
    hash = hashlib.sha256()
    #convert time into hash
    hash.update(str(time.time()).encode('utf-8'))
    #keep only first 10 chars of hash.hexdigest()
    return hash.hexdigest()[:digits]


def extractDictValue(key, dict):
    """
    Geven a 'key', the method returns the related value from the 'dict' dictionary.
    If dict has no keys of value "key" the method returns None.
    """
    if key is None:
        return None
    return None if dict.get(key) is None else dict.get(key)


def getUid(existing_uids, digits_num):
    """ Extract a random UID
    (with the given digits)
    ensuring that do not already exists. """
    max = calcMax(digits_num)
    while True:
        uid = str(random.randint(0, max))
        #fill empty spaces to get the requested digits
        uid = uid.zfill(digits_num)
        if extractDictValue(uid, existing_uids) is not None:
            #uuid already in use, extract a new one
            continue
        return uid

def calcMax(digits_num):
    """ """
    max = ''
    i = 0
    while i < digits_num:
        max += str(9)
        i += 1
    return int(max)