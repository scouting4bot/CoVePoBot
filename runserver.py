"""
This script runs the application using a development server.
"""

import os
# Import the code from each app. e.g.: BotApp/__init__.py
from CoVePoBot import app

# This is optional code that starts the Flask development server with specific host and port values taken from environment variables
if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')

    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    app.run(HOST, PORT)