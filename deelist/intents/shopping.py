from flask_ask import statement, context, question
from deelist import ask, app, api
import requests

LIST_ACCESS = "This skill doesn't work without list read \
               and writes enabled. You need to open your \
               Alexa app and enable these permissions."

def hasnt_allowed_list_permissions():
    user = context.System.user
    return not hasattr(user, "permissions") or \
           not hasattr(user.permissions, "consentToken")

def get_token():
    return context.System.user.permissions.consentToken

def get_shopping_list_text(shopping_list):
    speech = ""
    if shopping_list == []:
      speech = "Your list is empty."
    else:
      speech = "Your shopping list is: " + ", ".join(shopping_list)
    return speech

def get_item_id(shopping_list, item):
    item_id = ""
    for i in shopping_list['items']:
        if i['value'] == item and \
              i['status'] == 'active':
            item_id = i['id']
    return item_id

@ask.launch
def login():
    text = "Welcome to dee list. Try asking me to \
            delete something from your shopping list."
    prompt = "For example, say delete relish from my \
              shopping list."
    return question(text).reprompt(prompt) \
            .simple_card(title="Welcome to dee list",
                         content="Try asking me to delete something.")

@ask.intent("AMAZON.HelpIntent")
def help():
    return question(
            "Here are some things you can say: \
            what is on my shopping list, \
            what is on the shopping list, \
            delete relish from my shopping list").reprompt(
                    "For example say, delete relish \
                    from my shopping list.")

@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("Stopping.")

@ask.intent("AMAZON.CancelIntent")
def cancel():
    return statement("Cancelling.")

@ask.intent("WhatIsMyShoppingListIntent")
def my_shopping_list():
    if hasnt_allowed_list_permissions():
        return statement(LIST_ACCESS)
    TOKEN = get_token()
    shopping_list = api.shopping_list_items(TOKEN))
    return statement(get_shopping_list_text(shopping_list))

@ask.intent("DeleteItemFromShoppingListIntent")
def delete_from_shopping_list(item):
    if hasnt_allowed_list_permissions():
        return statement(LIST_ACCESS)
    TOKEN = get_token()
    shopping_list = api.get_shopping_list(TOKEN)
    if shopping_list == []:
        return statement("Your list is empty.")
    r = api.delete_item_in_shopping_list(
      item_id=get_item_id(shopping_list, item),
      token=TOKEN
    )
    if r.status_code == 200:
        return statement("Deleted {}.".format(item))
    return statement("Don't think I found {}.".format(item))
