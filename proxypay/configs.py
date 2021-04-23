from django.conf import settings
from django.utils.translation import gettext_lazy as _

from proxypay.exceptions import ProxypayValueError

# ================================================================================

DEFAULTS = {
    # entity
    'PRIVATE_KEY': None,
    'ENTITY': None,
    # references
    'REFERENCE_LIFE_TIME_IN_DAYS': 1,
    'REFERENCE_UUID_KEY': 'djpp_uuid_ref',
    # payments
    'ACCEPT_UNRECOGNIZED_PAYMENT': False,
    # If true, in sandbox env mode fictitious payments will be processed automatically without the proxypay webhook.
    # Useful if you want to test local payments without configuring the endpoint watch payments on proxypay
    'ACKNOWLEDGE_MOCK_PAYMENT_LOCALLY_AUTOMATICALLY': True,
    # proxypay defaults fees
    # fee must be a tuple in this order: Fee Name, Fee Percent, Min Amount, Max Amount
    'PROXYPAY_FEE': ('Proxypay', 0.25, 50, 1000),
    'BANK_FEE': (None, 0, 0, 0),
    # proxypay
    'API_PRODUCTION_BASE_URL': 'https://api.proxypay.co.ao',
    'API_SANDBOX_BASE_URL': 'https://api.sandbox.proxypay.co.ao',
    'ENV': None, # production or sandbox
}

# ================================================================================

class AppConfigurations:

    PRODUCTION_ENV = 'production'
    SANDBOX_ENV = 'sandbox'

    def __init__(self, user_configurations=None, defaults=None) -> None:
        if user_configurations:
            self._user_configurations = self._check_user_configurations(user_configurations)
        self.defaults = defaults or DEFAULTS
        self._cached_attrs = set()

    @property
    def user_configurations(self):
        if not hasattr(self, '_user_configurations'):
            return getattr(settings, 'PROXYPAY', {})
        return self._user_configurations
    
    def _check_user_configurations(self, configs):
        if isinstance(configs, dict):
            return configs
        return {}

    def __getattr__(self, attr: str):
        if attr not in self.defaults:
            raise AttributeError(_("Invalid app configuration key: '%s'") % attr)
        
        try:
            value = self.user_configurations[attr]
        except KeyError:
            value = self.defaults[attr]
        
        # caching
        self._cached_attrs.add(attr)
        setattr(self, attr, value)
        return value
    
    # def reload(self):
    #     for attr in self._cached_attrs:
    #         delattr(self, attr)
    #     self._cached_attrs.clear()
    #     if hasattr(self, '_user_configurations'):
    #         delattr(self, '_user_configurations')
    
    ### ------------------------------------------------------------------------

    def get_url(self) -> str:
        if self.ENV == self.PRODUCTION_ENV:
            return self.API_PRODUCTION_BASE_URL
        return self.API_SANDBOX_BASE_URL
    
    def get_environment(self):
        if not self.ENV:
            return self.PRODUCTION_ENV if not getattr(settings, 'DEBUG') else self.SANDBOX_ENV
        return self.ENV
    
    def get_entity(self):
        return self.ENTITY

    def get_token(self):
        return self.PRIVATE_KEY
    
    def get_reference_lifetime(self, days=None):
        try:
            return int(days or self.REFERENCE_LIFE_TIME_IN_DAYS or 1)
        except:
            raise ProxypayValueError(_('days must be a number'))
    
conf = AppConfigurations()