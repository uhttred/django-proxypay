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

    __headers  = {}     # default api headers
    __url      = ''     # base api url
    __entity   = None   # 
    env        = None

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
        self.__url    = configs.get('url')
        # entity
        self.__entity = configs.get('entity')
        # envi
        self.env = configs.get('environment')

    # ==========================================================

    ###
    ##  Property Methods
    # 

    @property
    def entity(self):
        return self.__entity

    # ==========================================================
    
    ###
    ##  Interaction With Proxypay
    # 

    # ------------------------ REFERENCES -----------------------

    # get new reference

    def get_reference_id(self):
        
        """
        Get Generated Reference Id from Proxypay
        Returns reference id (int as string) or False 
        """

        r = self.post('/reference_ids')
        # response status
        return r.json() if r.status_code == 200 else False

    # create or update a payment reference

    def create_or_update_reference(self, reference_id, data):

        """
        Creates or Update a Pament Reference by Reference Id
        Returns Proxypay Payment Reference Object 

        data = { amount, end_datetime, custom_fields }
        """

        r = self.put(f"/references/{reference_id}", data=data)
        # response status
        return True if r.status_code == 204 else False

    # delete reference

    def delete_reference(self, reference_id):

        """
        Delete a reference from Proxypay
        """

        r = self.delete(f"/references/{reference_id}")
        # response status
        return True if r.status_code == 204 else False


    # ------------------------ PAYMENTS -----------------------

    # get unrecognized payments

    def get_payments(self):
        
        """
        Returns a list of all payments that have 
        not yet been recognized
        """

        r = self.get('/payments')
        # response status
        return r.json() if r.status_code == 200 else False

    # check reference payment status

    def check_reference_payment(self, reference_id):

        """
        Checks if a reference has already been paid, if so, 
        returns the payment data and eliminates the payment data in proxyapy

        Make sure to update the reference (proxypay.models.Reference) as paid
        """

        # getting all unrecognized payments
        payments = self.get_payments()

        if payments:
            for payment in payments:
                if payment.get('reference_id') == reference_id:
                    # acknowledge payment
                    self.acknowledge_payment(payment.get('id'))
                    # returns the paymen data
                    return payment
        
        return False

    # Acknowledges payment

    def acknowledge_payment(self, payment_id):

        r = self.delete(f"/payments/{payment_id}")
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

    def delete(self, path, data={}, params={}):

        """ makes a DELETE request, path parameter must init with / """

        with requests.delete(f"{self.__url}{path}", json=data, params=params, headers=self.__headers,) as r:
            return r
    
    # ==========================================================
    

# ==========================================================================================================

api = ProxypayAPI()