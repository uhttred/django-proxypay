###
##  Django Proxypay API 
#

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
    ##  Interaction With Proxypay
    # 

    def get_reference_id(self):
        
        """
        Get Generated Reference Id from Proxypay
        Returns reference id (int as string) or False 
        """

        r = self.post('/reference_ids')
        # response status
        return r.json() if r.status_code == 200 else False

    def create_or_update_reference(self, reference_id, data):

        """
        Creates or Update a Pament Reference by Reference Id
        Returns Proxypay Payment Reference Object 

        data = { amount, end_datetime, custom_fields }
        """

        r = self.put(f"/references/{reference_id}", data=data)
        # response status
        return True if r.status_code == 204 else False
        
    # ==========================================================

    ###
    ##  Base Request Methods, GET, POST, PUT, DELETE
    #   

    def get(self, path, params={}):

        """ makes a GET request, path parameter must init with / """

        with requests.get(f"{self.__url}{path}", params=params, headers=self.__headers,) as r:
            return r

    def post(self, path, data={}, params={}):

        """ makes a POST request, path parameter must init with / """

        with requests.post(f"{self.__url}{path}", json=data, params=params, headers=self.__headers,) as r:
            return r

    def put(self, path, data={}, params={}):

        """ makes a PUT request, path parameter must init with / """

        with requests.put(f"{self.__url}{path}", json=data, params=params, headers=self.__headers,) as r:
            return r
    
    # ==========================================================
    
    ###
    ##  Utils
    # 

    # def default_ok_response(self, r):

    #     """Default response for requests Request"""

    #     pass

    # def default_error_response(self, r):

    #     """Default response for requests Request"""

    #     return

# ==========================================================================================================

api = ProxypayAPI()