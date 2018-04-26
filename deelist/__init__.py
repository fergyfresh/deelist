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
    if r.status_code == 200:
        return(r.json())

def shopping_list_items():
    shopping_list = get_shopping_list()['items']
    items = []
    for item in shopping_list:
        if item['status'] == "active":
            items.append(item['value'])
    return items

@ask.intent("WhatIsMyShoppingList")
def my_shopping_list()
    shopping_list = shopping_list_items()
    speech = "Your list is "
    if shopping_list == []:
        speech += "empty"
    else:
        speech = base_speech + " and ".join(shopping_list)
    return statement(speech)
