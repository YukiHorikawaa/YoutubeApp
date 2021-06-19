import json

class get_json:
    def __init__(self, jsonData):
        self.jsonData = json.loads(jsonData)
        self.jsonData = dict(self.jsonData)
        print("Type:{}, Data:{}".format(type(jsonData), jsonData))

    def get(self):
        return self.jsonData

    def getUrl(self, url):
        return str(self.jsonData[url])

    def getWord(self, word):
        return str(self.jsonData[word])