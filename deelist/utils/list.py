from builtins import object
import requests

class ListWrapper(object):
    def __init__(self, base_url, token, header):
        self.base_url = base_url
        self.token = token
        self.header = header
        
    def get_lists(self):
        r = requests.get(self.base_url, 
                         headers=self.header)
        if r.status_code == 200:
            return(r.json())
    
    def get_shopping_list_id(self):
        list_metadeta = self.get_lists()
        list_id = ""
        for list in list_metadata["lists"]:
            if list["name"] == "Alexa shopping list":
                list_id = list["listId"]
        return list_id
        
    def get_shopping_list(self):
        URL = self.base_url + \
              self.get_shopping_list_id() + \
              "/active"
        r = requests.get(URL, headers=self.header)
        if r.status_code == 200:
            return(r.json())

    def shopping_list_items(self):
        shopping_list = self.get_shopping_list()
        if shopping_list == None:
            return []
        items = []
        for item in shopping_list["items"]
            if item["status"] == "active":
                items.append(item["value"])
        return items
    
    def delete_item_in_shopping_list(self, item_id):
        URL = self.base_url + self.get_shopping_list_id() + \
              "/items/" + item_id
        return requests.delete(URL, headers=self.header)
