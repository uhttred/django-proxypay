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
PP_CONFIG_DEFAULT_DEVELOPMENT_ENV       = 'sandbox'
PP_CONFIG_DEFAULT_PRODUCTION_ENV        = 'production'
PP_API_PRODUCTION_BASE_URL              = 'https://api.proxypay.co.ao'
PP_API_DEVELOPMENT_BASE_URL             = 'https://api.sandbox.proxypay.co.ao'
PP_AUTO_PAYMENT_REF_ID                  = 'dj_pp_reference_id'

# =================================================================================================================================================

def get_configurations():

    """Get and validate configuration for proxypay on settings"""

    if hasattr( settings, PP_SETTINGS_CONFIG_KEY ):
        
        # getting the configuration for proxypay
        configs = eval(f"settings.{PP_SETTINGS_CONFIG_KEY}")
        
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

    raise ProxypayKeyError(
        f"{PP_SETTINGS_CONFIG_KEY} key not found on settings"
    )

# =================================================================================================================================================

def get_default_reference_expires_days():

    """  """

    if hasattr( settings, PP_SETTINGS_CONFIG_KEY ):
        
        # getting the configuration for proxypay
        configs = eval(f"settings.{PP_SETTINGS_CONFIG_KEY}")
        
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
    #
    raise ProxypayKeyError(
        f"{PP_SETTINGS_CONFIG_KEY} key not found on settings"
    )

# =================================================================================================================================================

def get_private_key():
    #
    if hasattr( settings, PP_SETTINGS_CONFIG_KEY ):
        # getting the configuration for proxypay
        configs = eval(f"settings.{PP_SETTINGS_CONFIG_KEY}")
        #
        return configs.get(PP_CONFIG_API_TOKEN_KEY)
    #
    return None

# =================================================================================================================================================