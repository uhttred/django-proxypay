###
##  Django Proxypay Configurations Methods
#

# django stuff
from django.conf import settings

# proxypay stuff
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

# =================================================================================================================================================

def get_configs (raise_error=True):
    try:
        configs = settings.PROXYPAY
    except:
        if raise_error:
            raise ProxypayKeyError(
                f"{PP_SETTINGS_CONFIG_KEY} key not found on settings"
            )
        else:
            return None
    else:
        return configs

def get_configurations ():

    """Get and validate configuration for proxypay on settings"""

    configs = get_configs()
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
    if (configs := get_configs(False)):
        return configs.get(
            PP_CONFIG_ACCEPT_UNRECOGNIZED_PAYMENT_KEY,
            False
        )
    return False

def get_default_reference_expires_days():
    # getting the configuration for proxypay
    configs = get_configs()   
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
    if (configs := get_configs(False)):
        return configs.get(PP_CONFIG_API_TOKEN_KEY)
    return None

# =================================================================================================================================================