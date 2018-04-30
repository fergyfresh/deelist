import logging
import requests
from flask import Flask
from flask_ask import Ask, statement, context

app = Flask(__name__)
ask = Ask(app, "/")
log = logging.getLogger('flask_ask').setLevel(logging.DEBUG)

BASE_URL = "https://api.amazonalexa.com/v2/householdlists/"

def get_lists():
    TOKEN = context.System.user.permissions.consentToken
    HEADER = {'Accept': 'application/json',
              'Authorization': 'Bearer {}'.format(TOKEN)}
    r = requests.get(BASE_URL, headers=HEADER)
    if r.status_code == 200:
        return(r.json())

def get_shopping_list_id():
    list_metadata = get_lists()
    list_id = ""
    for l in list_metadata["lists"]:
        if l["name"] == "Alexa shopping list":
            list_id = l["listId"]
    return list_id

def get_shopping_list():
    URL = BASE_URL + get_shopping_list_id() + "/active"
    TOKEN = context.System.user.permissions.consentToken
    HEADER = {'Accept': 'application/json',
              'Authorization': 'Bearer {}'.format(TOKEN)}
    r = requests.get(URL, headers=HEADER)
    if r.status_code == 200:
        return(r.json())

def shopping_list_items():
    shopping_list = get_shopping_list()
    if shopping_list == None:
        return []
    items = []
    for item in shopping_list["items"]:
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
