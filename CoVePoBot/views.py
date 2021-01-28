"""
This script contains the definition of routes and views for the application.
"""
import sys
import hashlib
import time
import random
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from CoVePoBot import app, logger, app_config
from CoVePoBot.application.datasource.mysql.connection import ExecuteQueryInsert, ExecuteQueryUpdate, ExecuteQuerySelect
from CoVePoBot.application.datasource.initcache import init_vote_session_list

app_full_name = app_config["app_full_name"]
app_short_name = app_config['app_short_name']
domain = app_config['domain']

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

mysql = MySQL()
mysql.init_app(app)


#-----------------------------------------------------------------------
vote_session_list = init_vote_session_list(mysql)
print('==========> vote_session_list = ' + str(vote_session_list))


#-----------------------------------------------------------------------
@app.route('/')
def home():
    """Renders a sample page."""
    return "Nessun servizio disponibile!"


#-----------------------------------------------------------------------
@app.route('/CoVePoBot/dashboard/<vote_id>')
def mngDashboard(vote_id):
    """Render a dashboard with html template."""
    
    #validate vote_id
    if vote_id is None or vote_id == '' or extractDictValue(vote_id, vote_session_list) is None:
        result = "Votazione non valida"
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", 409
    
    #check password
    psw = request.args.get('password', '')
    if psw is None or psw == '' or psw != vote_session_list[vote_id]["psw"]:
        return 'Non sei autorizzato', 403
    
    content = "Lista degli OTP ancora attivi in questa sessione"
    list2show = getOnlyActiveStatus(vote_session_list[vote_id]["otps"])
    info = {"vote_id":vote_id, "password":psw}
    url_base = domain + "/CoVePoBot/" + vote_id + "/otp/"

    # the templating engine (Jinja) automatically escapes HTML content in the variables.
    # Automatic escaping prevents accidental vulnerabilities to injection attacks.
    return render_template(
        "dashboard.html",
        title = "Management Dashboard",
        content = content,
        info = info,
        list2show = list2show,
        url_base = url_base)


#-----------------------------------------------------------------------
@app.route('/CoVePoBot/dashboard/<vote_id>/additionalotp')
def mngDashboard_additionalotp(vote_id):
    """ Creates additional otps for the vote session. """
    
    #validate vote_id
    if vote_id is None or vote_id == '' or extractDictValue(vote_id, vote_session_list) is None:
        result = "Votazione non valida"
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", 409
    
    #check password
    psw = request.args.get('password', '')
    if psw is None or psw == '' or psw != vote_session_list[vote_id]["psw"]:
        return 'Non sei autorizzato', 403
    
    # Validate number of otps to be created
    otp_num = request.args.get('otp_num', '')
    try:
        if otp_num is None or otp_num == '':
            otp_num = '0'
        otp_num = int(otp_num)

    except ValueError:
        return "NUM non è un numero valido", 400
    
    #create additional otps
    otps = createOtps(vote_id, otp_num)
    vote_session_list[vote_id]["otps"].update(otps)
    
    content = "Lista dei nuovi OTP attivati per questa sessione"
    list2show = otps
    info = {"vote_id":vote_id, "password":psw}
    url_base = domain + "/CoVePoBot/" + vote_id + "/otp/"

    # the templating engine (Jinja) automatically escapes HTML content in the variables.
    # Automatic escaping prevents accidental vulnerabilities to injection attacks.
    return render_template(
        "dashboard.html",
        title = "Management Dashboard",
        content = content,
        info = info,
        list2show = list2show,
        url_base = url_base,
        showurl = True)


#-----------------------------------------------------------------------
@app.route('/CoVePoBot/dashboard/<vote_id>/list')
def mngDashboard_list(vote_id):
    """ Creates additional otps for the vote session. """
    
    #validate vote_id
    if vote_id is None or vote_id == '' or extractDictValue(vote_id, vote_session_list) is None:
        result = "Votazione non valida"
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", 409
    
    #check password
    psw = request.args.get('password', '')
    if psw is None or psw == '' or psw != vote_session_list[vote_id]["psw"]:
        return 'Non sei autorizzato', 403
    
    # Validate element type to be listed
    element = request.args.get('element', '')
    if element is None or element == '' or (element != 'secrets' and element != 'otps'):
        return 'Richiesta non valida', 409
    
    content = "Lista dei "+element+" ancora attivi in questa sessione"
    list2show = getOnlyActiveStatus(vote_session_list[vote_id][element])
    info = {"vote_id":vote_id, "password":psw}
    url_base = domain + "/CoVePoBot/" + vote_id + "/otp/"
    showurl = element == 'otps'

    # the templating engine (Jinja) automatically escapes HTML content in the variables.
    # Automatic escaping prevents accidental vulnerabilities to injection attacks.
    return render_template(
        "dashboard.html",
        title = "Management Dashboard",
        content = content,
        info = info,
        list2show = list2show,
        url_base = url_base,
        showurl = showurl)


#-----------------------------------------------------------------------
@app.route('/CoVePoBot/dashboard/<vote_id>/secret')
def mngDashboard_disableSecret(vote_id):
    """ Disables a secret. """

    #validate vote_id
    if vote_id is None or vote_id == '' or extractDictValue(vote_id, vote_session_list) is None:
        result = "Votazione non valida"
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", 409

    #check password
    psw = request.args.get('password', '')
    if psw is None or psw == '' or psw != vote_session_list[vote_id]["psw"]:
        return 'Non sei autorizzato', 403

    content = 'Per revocare il secret, devi invocare il seguente Link, sostituendo "<OTP>" con il valode della otp che ha generato il secret.'
    alert = domain+'/CoVePoBot/'+vote_id+'/secret/<OTP>?password='+psw
    info = {"vote_id":vote_id, "password":psw}
    showurl = False

    # the templating engine (Jinja) automatically escapes HTML content in the variables.
    # Automatic escaping prevents accidental vulnerabilities to injection attacks.
    return render_template(
        "dashboard.html",
        title = "Management Dashboard",
        content = content,
        info = info,
        showurl = showurl,
        alert = alert)


#-----------------------------------------------------------------------
@app.route('/CoVePoBot/setup/aggiungi') # "setup/aggiungi" is deprecated
@app.route('/CoVePoBot/session')
def setupCreateVoteSession():
    """ Creates a new vote session. """
    vote_id = request.args.get('id', '')

    try:
        # Validate number of otps to be created
        otp_num = request.args.get('otp_num', '')
        if otp_num is None or otp_num == '':
            otp_num = '0'
        otp_num = int(otp_num)

        # Validate flag about otps print
        get_otp_as_url = request.args.get('otp_as_url', '')
        if get_otp_as_url is None or get_otp_as_url == '':
            get_otp_as_url = 'false'
        get_otp_as_url = (get_otp_as_url.lower() == 'true')

        # Validate flag about link_dashboard
        link_dashboard = request.args.get('dashboard', '')
        if link_dashboard is None or link_dashboard == '':
            link_dashboard = 'false'
        link_dashboard = (link_dashboard.lower() == 'true')

    except ValueError:
        return "NUM non è un numero valido", 400

    msg, http, psw = createVoteSession(vote_id, otp_num, get_otp_as_url)
    if (link_dashboard):
        return str(msg)+'<br /><a href="/CoVePoBot/dashboard/'+vote_id+'?password='+str(psw)+'">Dashboard</a>', http
    else:
        return msg, http


#-----------------------------------------------------------------------
@app.route('/CoVePoBot/<vote_id>/additionalotp')
def setupAddOtps(vote_id):
    """ Creates additional otps for the vote session. """
    
    #check password
    psw = request.args.get('password', '')
    if psw is None or psw == '' or psw != vote_session_list[vote_id]["psw"]:
        return 'Non sei autorizzato', 403
    
    try:
        # Validate number of otps to be created
        otp_num = request.args.get('otp_num', '')
        if otp_num is None or otp_num == '':
            otp_num = '0'
        otp_num = int(otp_num)

        # Validate flag about otps print
        get_otp_as_url = request.args.get('otp_as_url', '')
        if get_otp_as_url is None or get_otp_as_url == '':
            get_otp_as_url = 'false'
        get_otp_as_url = (get_otp_as_url.lower() == 'true')

    except ValueError:
        return "NUM non è un numero valido", 400
    
    #create additional otps
    return addOtps(vote_id, otp_num, get_otp_as_url)


#-----------------------------------------------------------------------
@app.route('/CoVePoBot/<vote_id>/secret/<otp>')
def disableSecret(vote_id, otp):
    """ Disables a secret. """
    
    #validate vote_id
    if vote_id is None or vote_id == '' or extractDictValue(vote_id, vote_session_list) is None:
        result = "Votazione non valida"
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", 409
    
    #validate password
    psw = request.args.get('password', '')
    if psw is None or psw == '' or psw != vote_session_list[vote_id]["psw"]:
        return 'Non sei autorizzato', 403
    
    #validate secret
    if otp is None or otp == '' or extractDictValue(otp, vote_session_list[vote_id]['otps']) is None:
        result = "Secret non valido"
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", 409
    
    secret = getSecret(vote_id, otp, 10)

    if extractDictValue(secret, vote_session_list[vote_id]['secrets']) is None:
        result = "Secret non valido"
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", 409

    vote_session_list[vote_id]['secrets'][secret] = 'expired'

    # Update in the DB
    result = ExecuteQueryUpdate('secret', {'vote_id':vote_id,'secret':secret,'nwVal':{'status':'expired'}}, mysql)
    if result != 1:
        return "Errore con DB", 500

    #create the requested csv
    return "Secret disabilitato", 200


#-----------------------------------------------------------------------
@app.route('/CoVePoBot/<vote_id>/secrets')
@app.route('/CoVePoBot/<vote_id>/secrets/')
def getSecretCSV(vote_id):
    """ Return a list of activated secrets. """
    
    #validate vote_id
    if vote_id is None or vote_id == '' or extractDictValue(vote_id, vote_session_list) is None:
        result = "Votazione non valida"
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", 409
    
    #check password
    psw = request.args.get('password', '')
    if psw is None or psw == '' or psw != vote_session_list[vote_id]["psw"]:
        return 'Non sei autorizzato', 403

    #check source
    source = request.args.get('source', '')
    if source is None or source == '' or source != 'db':
        #create the requested csv from CACHE
        return csvFromDictByStatus(vote_session_list[vote_id]["secrets"], 'enabled'), 200
    else:
        #create the requested csv from DB
        result_list = ExecuteQuerySelect('secret', {'columns2select':'secret', 'vote_id':vote_id, 'status':'enabled'}, mysql)
        csv = ''
        for row in result_list:
            csv = csv + str(row[0]) + ','
        if csv is not None or csv != '':
            csv = csv[:-1]
        return csv, 200


#-----------------------------------------------------------------------
@app.route('/CoVePoBot/<vote_id>/otps')
@app.route('/CoVePoBot/<vote_id>/otps/')
def getOtpCSV(vote_id):
    """ Return a list of available otps. """

    #validate vote_id
    if vote_id is None or vote_id == '' or extractDictValue(vote_id, vote_session_list) is None:
        result = "Votazione non valida"
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", 409

    #check password
    psw = request.args.get('password', '')
    if psw is None or psw == '' or psw != vote_session_list[vote_id]["psw"]:
        return 'Non sei autorizzato', 403

    #create the requested csv
    return csvFromDictByStatus(vote_session_list[vote_id]["otps"], 'available'), 200


#-----------------------------------------------------------------------
@app.route('/CoVePoBot/<vote_id>/otp/<otp>')
def autorizeOtp(vote_id, otp):
    """ Given an OTP, validates it and provides a secret. """
    if otp is None:
        otp = request.args.get('otp', '')

    msg, value, alert, http = convertOtp(vote_id, otp)

    return render_template(
        "layout.html",
        title = "Password per la sessione di voto " + vote_id,
        msg = msg,
        value = value,
        alert = alert)


#-----------------------------------------------------------------------
@app.route('/CoVePoBot/<vote_id>/otp')
@app.route('/CoVePoBot/<vote_id>/otp/')
def autorizeOtp_missingOtp(vote_id):
    """ Given an OTP, validates it and provides a secret. """
    otp = request.args.get('otp', '')
    return autorizeOtp(vote_id, otp)


#-----------------------------------------------------------------------
def convertOtp(vote_id, otp):
    """ Check if the otp is valid. """

    #validate vote_id
    if vote_id is None or vote_id == '' or extractDictValue(vote_id, vote_session_list) is None:
        result = "Votazione non valida"
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", "", "", 409
    #validate otp
    elif otp is None or otp == '':
        result = "Codice otp mancante"
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", "", "", 400
    #check that the otp exists
    elif extractDictValue(otp, vote_session_list[vote_id]['otps']) is None or vote_session_list[vote_id]['otps'][otp] == 'expired':
        result = "Codice otp non valido"
        return result + ". Accertati che sia tutto corretto per votare alla "+vote_id+".", "", "", 403
    #convert otp into a secret
    else:
        secret = getSecret(vote_id, otp, 10)

        # Disable otp
        vote_session_list[vote_id]['otps'][otp] = 'expired'

        # Update in the DB
        result = ExecuteQueryUpdate('otp', {'vote_id':vote_id,'otp':otp,'nwVal':{'status':'expired'}}, mysql)
        if result != 1:
            return "Errore con DB", "", "", 500

        # Enable secret
        vote_session_list[vote_id]['secrets'][secret] = 'enabled'

        # Store in the DB
        result = ExecuteQueryInsert('secret', {'vote_id':vote_id,'secret':secret,'status':'enabled','create_date':now()}, mysql)
        if result != 1:
            return "Errore con DB", "", "", 500

        print(vote_session_list)
        return "Il tuo codice per votare alla sessione di voto '"+vote_id+"' è ", secret, "Attenzione! Non sarà possibile riprodurlo nuovamente. Perciò conservalo accuratamente e non perderlo", 200


def getSecret(vote_id, otp, digits):
    return getHash(app_short_name+otp+vote_id+vote_session_list[vote_id]['psw']+vote_session_list[vote_id]['create_date'], digits)#TODO enhance the hash with date hash


def createVoteSession(vote_id, otp_num, get_otp_as_url):
    """ Adds a vote session to the vote_session_list """

    #check if the key already exists
    if vote_id is None or vote_id == '':
        return "ID non valido", 400, ''
    elif extractDictValue(vote_id, vote_session_list) is not None:
        return "ID già in uso", 409, ''
    else:
        isSuccess, result, psw = getNewVoteSession(vote_id, otp_num)
        if isSuccess:
            #update vote_session_list
            vote_session_list[vote_id] = result

            #build response
            response = "Aggiunta la nuova sessione "+vote_id+". "
            response += "Usa come password per la gestione: " + psw
            response += "\nGli otp disponibili sono:\n" + printOtp(vote_session_list[vote_id]["otps"], vote_id, get_otp_as_url)
            
            return response, 200, psw
        else:
            return result, 500, ''


def printOtp(dict, vote_id, get_otp_as_url):
    """ Extract the list of new otps to  return in the response """
    if get_otp_as_url:
        url_base = domain + "/CoVePoBot/" + vote_id + "/otp/"
        return listFromDictWithPrefix(dict, url_base)
    else:
        return csvFromDict(dict)


def csvFromDict(dict):
    """ Extract a Comma Separated List (CSV) string of keys in a dictionary """
    csv = ''
    for key in dict:
        csv = csv + key + ','
    if csv is not None or csv != '':
        csv = csv[:-1]
    return csv


def listFromDictWithPrefix(dict, prefix):
    """ Extract a Comma Separated List (CSV) string of keys in a dictionary and adds to each one a prefix. """
    csv = ''
    for key in dict:
        csv = csv + prefix + key + '\n'
    if csv is not None or csv != '':
        csv = csv[:-2]
    return csv


def csvFromDictByStatus(dict, status):
    """ Extract a Comma Separated List (CSV) string of keys with value "available" in a dictionary """
    csv = ''
    for key in dict:
        if dict[key] == status:
            csv = csv + key + ','
    if csv is not None or csv != '':
        csv = csv[:-1]
    return csv


def getOnlyActiveStatus(dict):
    """ Extract a Dict with only 'enabled' or 'available' elements """
    output = {}
    for key in dict:
        if dict[key] == 'enabled' or dict[key] == 'available':
            output[key] = dict[key]
    return output


def getNewVoteSession(vote_id, otp_num):
    """ Creates a new Vote Session with its set of otps. """
    # Create password
    psw = getHash(time.time(), 10)

    # Crete date
    create_date = now()

    # Store in the DB
    result = ExecuteQueryInsert('vote_session', {'vote_id':vote_id,'psw':psw,'create_date':create_date}, mysql)
    if result != 1:
        return False, '', ''

    if otp_num is None or otp_num == '':
        return True, {"id":vote_id, "psw":psw, "otps":{}, "secrets":{}, "create_date":create_date}, psw
    else:
        otps = createOtps(vote_id, otp_num)
        return True, {"id":vote_id, "psw":psw, "otps":otps, "secrets":{}, "create_date":create_date}, psw


def createOtps(vote_id, otp_num):
    """ Creates a dictionary with "otp_num" quantity of new otps. """
    otps = {}
    i = 0
    while i < otp_num:
        uid = getUid(otps, 6)
        otps[uid] = "available"

        # Store in the DB
        result = ExecuteQueryInsert('otp', {'vote_id':vote_id,'otp':uid,'create_date':now(),'status':'available'}, mysql)
        if result != 1:
            return {}
        i += 1
    return otps


def getHash(input, digits):
    #create hash
    hash = hashlib.sha256()
    #convert time into hash
    hash.update(str(input).encode('utf-8'))
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


def addOtps(vote_id, otp_num, get_otp_as_url):
    """ Adds more otps to the voting session. """
    if vote_id is None or vote_id == '' or extractDictValue(vote_id, vote_session_list) is None:
        return "ID non valido", 400
    
    otps = createOtps(vote_id, otp_num)
    vote_session_list[vote_id]["otps"].update(otps)
    print(vote_session_list)

    #build response
    response = "La sessione "+vote_id+" è stata aggiornata. "
    #extract the list of new otps to  return in the response
    response += "\nI nuovi otp disponibili sono: \n" + printOtp(otps, vote_id, get_otp_as_url)
    return response, 200


def now():
    """ Return the now-timestam in the format 'YYYY-mm-dd HH:MM:SS.ssssss'. """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
