# python stuffs
import datetime

# django stuff
from django.utils.timezone import now

from proxypay.exceptions import ProxypayException
from proxypay.conf import get_default_reference_expires_days

# ==========================================================================================================

def get_validated_data(amount, fields={}, days=None):

    ###
    ## Custom Fields
    #

    if len(fields) > 9:
        # 
        raise ProxypayException('Error creating reference, <fields> Add 9 max custom fields')
    
    # reference data
    data         = { 'amount': amount, 'custom_fields': fields }
    end_datetime = None
    
    ###
    ## days to expires
    #

    if days is None:
        # getting days from congurations if set
        days = get_default_reference_expires_days()

    if days and type(days) is int:
        # end_datetime
        end_datetime = now() + datetime.timedelta(days=days)
        # data
        data['end_datetime'] = end_datetime.strftime("%Y-%m-%d")
        #
        data['datetime'] = end_datetime

    elif days:
        # days value error
        raise ProxypayException('Error creating reference, <days> must be an integer')

    return data