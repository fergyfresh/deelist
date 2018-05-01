from __future__ import absolute_import
import logging
import requests
from flask import Flask
from flask_ask import Ask, statement, context

from .utils.list import ListWrapper

app = Flask(__name__)
ask = Ask(app, "/")
log = logging.getLogger('flask_ask').setLevel(logging.DEBUG)

BASE_URL = "https://api.amazonalexa.com/v2/householdlists/"

TOKEN = context.System.user.permissions.consentToken
HEADER = {'Accept': 'application/json',
          'Authorization': 'Bearer {}'.format(TOKEN)}

api = ListWrapper(base_url=BASE_URL,
                  token=TOKEN,
                  header=HEADER)

@ask.intent("WhatIsMyShoppingListIntent")
def my_shopping_list():
    shopping_list = api.shopping_list_items()
    speech = "Your list is "
    if shopping_list == []:
        speech += "empty"
    else:
        speech += " and ".join(shopping_list)
    return statement(speech)

@ask.intent("DeleteItemFromShoppingListIntent")
def delete_from_shopping_list(item):
    shopping_list = api.get_shopping_list()
    if shopping_list == []:
        return statement("Your list is empty.")
    item_id = ""
    for i in shopping_list['items']:
        if i['value'] == item and \
             i['status'] == 'active':
            item_id = i['id']
    r = api.delete_item_in_shopping_list(item_id)
    if r.status_code == 200:
        return statement("Deleted {}.".format(item))
    return statement("Don't think I found that.")
