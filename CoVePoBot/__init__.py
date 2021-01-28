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

logger = app.logger

# ----------------------------------------------------------
def config_environment_variables(app_config):
    
    if os.environ.get('has_config_vars') and os.environ.get('has_config_vars') != "":
        logger.info("Override configuration with Environment Variables")
        # app_config
        for key in app_config.keys():
            set_environment_variable(app_config, key)

    else:
        logger.info("No configuration was found in the Environment")

def set_environment_variable(config_dict, variable_key):
    variable_value = os.environ.get(variable_key)
    if variable_value is not None and variable_value != "":
        logger.info("- Environment has {0}".format(variable_key))
        config_dict[variable_key] = variable_value
# ----------------------------------------------------------

# Override configuration with environment variables
config_environment_variables(app_config)

app.config['MYSQL_DATABASE_USER'] = app_config['MYSQL_DATABASE_USER']
app.config['MYSQL_DATABASE_PASSWORD'] = app_config['MYSQL_DATABASE_PASSWORD']
app.config['MYSQL_DATABASE_DB'] = app_config['MYSQL_DATABASE_DB']
app.config['MYSQL_DATABASE_HOST'] = app_config['MYSQL_DATABASE_HOST']
app.config['MYSQL_DATABASE_PORT'] = app_config['MYSQL_DATABASE_PORT']

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

import CoVePoBot.views