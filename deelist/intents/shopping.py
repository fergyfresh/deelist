import requests
from flask_ask import statement, context
from deelist import ask, app, api

@ask.intent("WhatIsMyShoppingListIntent")
def my_shopping_list():
    TOKEN = context.System.user.permissions.consentToken
    shopping_list = api.shopping_list_items(TOKEN)
    speech = "Your list is "
    if shopping_list == []:
        speech += "empty"
    else:
        speech += " and ".join(shopping_list)
    return statement(speech)

@ask.intent("DeleteItemFromShoppingListIntent")
def delete_from_shopping_list(item):
    TOKEN = context.System.user.permissions.consentToken
    shopping_list = api.get_shopping_list(TOKEN)
    if shopping_list == []:
        return statement("Your list is empty.")
    item_id = ""
    for i in shopping_list['items']:
        if i['value'] == item and \
              i['status'] == 'active':
            item_id = i['id']
     r = api.delete_item_in_shopping_list(item_id=item_id, token=TOKEN)
     if r.status_code == 200:
         return statement("Deleted {}.".format(item))
     return statement("Don't think I found that.")
