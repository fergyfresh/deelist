from builtins import object
import requests

class ListWrapper(object):
    def __init__(self, base_url):
        self.base_url = base_url
    
    def header(self, token):
        HEADER = {"Accept": "application/json",
                  "Authorization": "Bearer {}".format(token)}
        return HEADER
    
    def get_lists(self, token):
        r = requests.get(self.base_url, 
                         headers=self.header(token))
        if r.status_code == 200:
            return(r.json())
    
    def get_shopping_list_id(self, token):
        list_metadeta = self.get_lists(token)
        list_id = ""
        for list in list_metadata["lists"]:
            if list["name"] == "Alexa shopping list":
                list_id = list["listId"]
        return list_id
        
    def get_shopping_list(self, token):
        URL = self.base_url + \
              self.get_shopping_list_id(token) + \
              "/active"
        r = requests.get(URL, headers=self.header(token))
        if r.status_code == 200:
            return(r.json())

    def shopping_list_items(self, token):
        shopping_list = self.get_shopping_list(token)
        if shopping_list == None:
            return []
        items = []
        for item in shopping_list["items"]:
            if item["status"] == "active":
                items.append(item["value"])
        return items
    
    def delete_item_in_shopping_list(self, item_id, token):
        URL = self.base_url + self.get_shopping_list_id(token) + \
              "/items/" + item_id
        return requests.delete(URL, headers=self.header(token))
