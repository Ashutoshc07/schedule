import json
import requests

WAIT_TIME = 70
message = ''
routing_key = ''
dev_url = 'http://localhost:3000/api'

class Apicalls:
    def __init__(self):

        self.url = dev_url
        self.username = 'esvtbeammap'
        self.password = 'GoWildBlue!'
        self.authid = self.authid()

    def authid(self):
        res = requests.post(self.url+'/v1/users',headers={'Content-Type':'application/json',
                                                          'Accept': 'application/json',
                                                          'username': self.username,
                                                          'password': self.password},
                            verify=False)
        if res.status_code == 200:
            return res.json()['api_key']
        else:
            print "Token Error, status code is "+str(res.status_code)
            return False


    def get(self,endpoint,payload=None):
        res = requests.get(self.url+endpoint+'&api_key='+self.authid,
                           headers={'Accept':'application/json'},
                           params=payload,
                           verify=False)
        if res.status_code == 200:
            return res
        else:
            print "GET Error, status code is "+str(res.status_code)
            return res

    def delete(self,endpoint,payload=None):
        res = requests.delete(self.url+endpoint+'&api_key='+self.authid,
                           headers={'Accept':'application/json'},
                           params=payload,
                           verify=False)
        if res.status_code == 200:
            return res
        else:
            print "GET Error, status code is "+str(res.status_code)
            return res        
