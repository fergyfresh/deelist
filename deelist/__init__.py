import logging
import requests
from flask import Flask
from flask_ask import Ask, statement, context

app = Flask(__name__)
ask = Ask(app, "/")
log = logging.getLogger('flask_ask').setLevel(logging.DEBUG)

BASE_URL = "https://api.amazonalexa.com/v2/householdlists/"

def get_shopping_list():
    URL = BASE_URL + get_shopping_list_id() + "/active"
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
    app.logger.debug(r.json)
    app.logger.debug("****************** get_lists() ************************")
    if r.status_code = 200:
        return(r.json()

def get_shopping_list_id(lists):
    list_id = ""
    for l in lists:
        if l["name"] == "Alexa shopping list":
            list_id = l["listId"]
    app.logger.debug("****************** get_shopping_list_id() ************************")
    app.logger.debug(list_id)
    app.logger.debug("****************** get_shopping_list_id() ************************")
    return list_id

def shopping_list_items():
    shopping_list = get_shopping_list()
    if shopping_list == None:
        return []
    items = []
    for item in shopping_list:
        if item['status'] == "active":
            items.append(item['value'])
    return items

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
