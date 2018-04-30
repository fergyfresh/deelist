import logging
import requests
from flask import Flask
from flask_ask import Ask, statement, context

app = Flask(__name__)
ask = Ask(app, "/")
log = logging.getLogger('flask_ask').setLevel(logging.DEBUG)

BASE_URL = "https://api.amazonalexa.com/v2/householdlists/"

def get_shopping_list():
    URL = BASE_URL + "shopping_list_list_id/active"
    TOKEN = context.System.user.permissions.consentToken
    HEADER = {'Accept': 'application/json',
             'Authorization': 'Bearer {}'.format(TOKEN)}
    r = requests.get(URL, headers=HEADER)
    app.logger.debug("****************** get_shopping_list() ************************")
    app.logger.debug(r.text)
    app.logger.debug("****************** get_shopping_list() ************************")
    if r.status_code == 200:
        return(r.json())                                        
    
def get_lists():
    TOKEN = context.System.user.permissions.consentToken
    HEADER = {'Accept': 'application/json',
              'Authorization': 'Bearer {}'.format(TOKEN)}
    r = requests.get(BASE_URL, headers=HEADER)
    app.logger.debug("****************** get_lists() ************************")
    app.logger.debug(r.text)
    app.logger.debug("****************** get_lists() ************************")

@ask.intent("WhatIsMyShoppingListIntent")
def my_shopping_list():
    lists = get_lists()
    shopping_list = shopping_list_items()
    speech = "Your list is "
    if shopping_list == []:
        speech += "empty"
    else:
        speech += " and ".join(shopping_list)
    return statement(speech)
