# requests
import requests

# django
from django.conf import settings

# proxypay
from .exceptions import ProxypayException


PROXYPAY_API_BASE_URLS = [
    'https://api.proxypay.co.ao',
    'https://api.sandbox.proxypay.co.ao'
]

PROXYPAY_ENVS = ['production', 'sandbox']


# ========================================================================

def check_environmet(env):

    """ Check given environmet """

    if env is None:
        # chooses env based on debug
        return 'sandbox' if settings.DEBUG else 'production'

    elif env not in PROXYPAY_ENVS:
        raise ProxypayException(
            'API_ENV value must be production or sandbox'
        )

    return env

def check_apikey(key):

    """ Check given key """

    if not key:
        raise ProxypayException(
            'API_AUTHORIZATION_KEY key is required'
        )

    return key


# ==========================================================================================================
    
"""Responsible for making all requests to proxypay"""

class ProxypayAPI:

    __headers  = {}
    __burl     = ''

    def __init__(self, configs=None):

        # using default configurations in project settings
        if not configs:
            #
            if hasattr( settings, 'PROXYPAY'):
                configs = settings.PROXYPAY
            else:
                raise ProxypayException('PROXYPAY key not found on settings')

        # Proxypay API Private KEY
        key = check_apikey(configs.get('API_AUTHORIZATION_KEY'))
        # Proxypay Environnement to use
        env = check_environmet(configs.get('API_ENV'))

        # setting the headers
        self.__headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.proxypay.v2+json',
            'Authorization': f"Token {key}"
        }

        # 
        self.__burl = PROXYPAY_API_BASE_URLS[ 0 if env == 'production' else 1]
    
    ###
    ##
    #

    def get(self, path, params={}):
        """ makes a GET request """
        return requests.get(f"{self.__burl}{path if path[0] == '/' else '/' + path}", 
            headers=self.__headers,
            params=params
        )

# ========================================================================================

api = ProxypayAPI()