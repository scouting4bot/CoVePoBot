import os
from flask import Flask
from logging.config import dictConfig, fileConfig
from CoVePoBot.application.utils import fromJsonToDict, getListOfFiles

# Configure logging
dictConfig(fromJsonToDict('CoVePoBot/static/conf/logger.json'))

# Create an instance of the Flask class and assign to the variable "app"
app = Flask(__name__)

# Add a configuration
app.config.from_json('static/conf/settings.json')

# Get configuration from JSON
app_config = fromJsonToDict('CoVePoBot/static/conf/app.json')
#telegram_config = fromJsonToDict('CoVePoBot/static/conf/telegram.json')
#data4bot = fromJsonToDict('CoVePoBot/static/conf/data4bot.json')
#imgs_list = getListOfFiles('CoVePoBot/static/img/','png')
#google_sheet_credentials = fromJsonToDict('CoVePoBot/static/conf/aids2botmastership.json')

logger = app.logger

# ----------------------------------------------------------
def config_environment_variables(app_config):#, telegram_config, data4bot, google_sheet_credentials):
    
    if os.environ.get('has_config_vars') and os.environ.get('has_config_vars') != "":
        logger.info("Override configuration with Environment Variables")
        # app_config
        for key in app_config.keys():
            set_environment_variable(app_config, key)
        # telegram_config
#        for key in telegram_config.keys():
#            set_environment_variable(telegram_config, key)
        # data4bot
#        for key in data4bot.keys():
#            set_environment_variable(data4bot, key)
        # data4bot
#        for key in google_sheet_credentials.keys():
#            set_google_environment_variable(google_sheet_credentials, key)

    else:
        logger.info("No configuration was found in the Environment")

def set_environment_variable(config_dict, variable_key):
    variable_value = os.environ.get(variable_key)
    if variable_value is not None and variable_value != "":
        logger.info("- Environment has {0}".format(variable_key))
        config_dict[variable_key] = variable_value

def set_google_environment_variable(config_dict, variable_key):
    variable_value = os.environ.get("GOOGLE_"+variable_key)
    if variable_value is not None and variable_value != "":
        logger.info("- Environment has {0}".format(variable_key))
        config_dict[variable_key] = variable_value
    return google_sheet_credentials
# ----------------------------------------------------------

# Override configuration with environment variables
config_environment_variables(app_config)#, telegram_config, data4bot, google_sheet_credentials)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

import CoVePoBot.views