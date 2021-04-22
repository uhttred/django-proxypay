from django.conf import settings
from django.utils.translation import gettext_lazy as _

from proxypay.exceptions import ProxypayKeyError, ProxypayValueError

# =================================================================================================================================================

###
##  Django Proxypay Constant
#
PP_SETTINGS_CONFIG_KEY                  = 'PROXYPAY'
PP_CONFIG_API_TOKEN_KEY                 = 'PRIVATE_KEY'
PP_CONFIG_API_ENTITY_KEY                = 'ENTITY'
PP_CONFIG_API_ENV_KEY                   = 'ENV'
PP_CONFIG_REFS_EXPIRES_DAYS_KEY         = 'REFERENCE_DAYS'
PP_CONFIG_ACCEPT_UNRECOGNIZED_PAYMENT_KEY = 'ACCEPT_UNRECOGNIZED_PAYMENT'
PP_CONFIG_DEFAULT_DEVELOPMENT_ENV       = 'sandbox'
PP_CONFIG_DEFAULT_PRODUCTION_ENV        = 'production'
PP_API_PRODUCTION_BASE_URL              = 'https://api.proxypay.co.ao'
PP_API_DEVELOPMENT_BASE_URL             = 'https://api.sandbox.proxypay.co.ao'
PP_UUID_REF_KEY                         = 'djpp_uuid_ref'

DEFAULTS = {
    # entity
    'PRIVATE_KEY': None,
    'ENTITY': None,

    # references
    'REFERENCE_LIFE_TIME_IN_DAYS': 1,
    'REFERENCE_UUID_KEY': 'djpp_uuid_ref',

    # payments
    'ACCEPT_UNRECOGNIZED_PAYMENT': False,

    # fees
    'PROXYPAY_FEES': {
        'PERCENTAGE': 0.5,
        'MIN_AMOUNT': 50,
        'MAX_AMOUNT': 1000
    },
    'BANK_FEES': {
        'PERCENTAGE': 0,
        'MIN_AMOUNT': 0,
        'MAX_AMOUNT': 0
    },

    # proxypay
    'API_PRODUCTION_BASE_URL': 'https://api.proxypay.co.ao',
    'API_SANDBOX_BASE_URL': 'https://api.sandbox.proxypay.co.ao',
    'ENV': None, # production or sandbox
}


# =================================================================================================================================================

def get_user_configurations (raise_exception=False):
    try:
        configs = settings.PROXYPAY
    except:
        if raise_exception:
            raise ProxypayKeyError(
                _("'%s' key not found on django settings" % PP_SETTINGS_CONFIG_KEY)
            )
        return {}
    return configs

def get_configurations ():

    """Get and validate configuration for proxypay on settings"""

    configs = get_user_configurations()
    # gettings api environment
    if configs.get(PP_CONFIG_API_ENV_KEY) is None:
        # using env based on settings.DEBUG status
        environment = PP_CONFIG_DEFAULT_DEVELOPMENT_ENV if settings.DEBUG else PP_CONFIG_DEFAULT_PRODUCTION_ENV
    else:
        environment = configs.get(PP_CONFIG_API_ENV_KEY)
        #
        if environment not in [PP_CONFIG_DEFAULT_DEVELOPMENT_ENV, PP_CONFIG_DEFAULT_PRODUCTION_ENV]:
            raise ProxypayValueError(
                f"{PP_CONFIG_API_ENV_KEY} expected value was {PP_CONFIG_DEFAULT_PRODUCTION_ENV} or {PP_CONFIG_DEFAULT_DEVELOPMENT_ENV}"
            )
    # getting api token key
    token = configs.get(PP_CONFIG_API_TOKEN_KEY)
    if not token:
        raise ProxypayValueError(
            f"{PP_CONFIG_API_TOKEN_KEY} is required"
        )
    # getting entity
    entity = configs.get(PP_CONFIG_API_ENTITY_KEY)
    if not entity:
        raise ProxypayValueError(
            f"{PP_CONFIG_API_ENTITY_KEY} is required"
        )
    #
    return {
        'environment': environment,
        'entity': entity,
        'token': token,
        'url': PP_API_PRODUCTION_BASE_URL if environment == PP_CONFIG_DEFAULT_PRODUCTION_ENV else PP_API_DEVELOPMENT_BASE_URL
    }

# =================================================================================================================================================

def get_accept_unrecognized_payment ():
    #
    if (configs := get_user_configurations(False)):
        return configs.get(
            PP_CONFIG_ACCEPT_UNRECOGNIZED_PAYMENT_KEY,
            False
        )
    return False

def get_default_reference_expires_days():
    # getting the configuration for proxypay
    configs = get_user_configurations()   
    # 
    if configs.get(PP_CONFIG_REFS_EXPIRES_DAYS_KEY):
        # 
        days = configs.get(PP_CONFIG_REFS_EXPIRES_DAYS_KEY)
        #
        if type(days) is int:
            return days
        #
        if type(days) is str:
            if days.isnumeric():
                return int(days)
        raise ProxypayValueError(f"{PP_CONFIG_REFS_EXPIRES_DAYS_KEY} value expected to be an integer")
    #
    return False

# =================================================================================================================================================

def get_private_key():
    if (configs := get_user_configurations(False)):
        return configs.get(PP_CONFIG_API_TOKEN_KEY)
    return None

# =================================================================================================================================================

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
    
    ### ------------------------------------------------------------------------------------

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