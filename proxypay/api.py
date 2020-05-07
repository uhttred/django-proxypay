# requests 
import requests

# proxypay stuff
from .conf import get_configurations

# ==========================================================================================================
    
"""Responsible for making all requests to proxypay"""

class ProxypayAPI:

    __headers  = {} # default api headers
    __url      = '' # base api url

    def __init__(self):

        # proxypay configuration from project settings
        configs = get_configurations()

        # setting the headers
        self.__headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.proxypay.v2+json',
            'Authorization': f"Token {configs.get('token')}"
        }

        # base url
        self.__url = configs.get('url')

    # ==========================================================

    ###
    ##  Utils
    # 

    def get_create_reference(self):
        pass
    
    # ==========================================================

    ###
    ##  Base Request Methods, GET, POST, PUT, DELETE
    #   

    def get(self, path, params={}):
        """ makes a GET request, path parameter must init with / """
        return requests.get(f"{self.__url}{path}", 
            headers=self.__headers,
            params=params
        )

# ==========================================================================================================

api = ProxypayAPI()