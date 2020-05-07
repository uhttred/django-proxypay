###
##  Django Proxypay Reference Creation
#

import datetime

# proxypay stuffs
from proxypay.api import api
from proxypay.conf import get_default_reference_expires_days
from proxypay.exceptions import ProxypayException

def create( amount, days=None, fields={} ):

    """
    Request to proxypay to create a reference and
    returns an instance of proxypay.models.Reference
    """

    # get Generated reference id from proxypay
    reference_id = api.get_reference_id()

    if reference_id:
        
        # reference data
        data = { 'amount': amount, 'custom_fields': fields }
        
        ###
        ## days to expires
        #

        if days is None:
            # getting days from congurations if set
            days = get_default_reference_expires_days()

        if days and type(days) is int:
            # end_datetime
            end_datetime = datetime.datetime.today() + datetime.timedelta(days=days)
            # data
            data['end_datetime'] = end_datetime.strftime("%Y-%m-%d")

        elif days:
            # days value error
            raise ProxypayException('Error creating reference, <days> must be an integer')
        
        created = api.create_or_update_reference(
            reference_id,
            data
        )

        # return created reference
        return created
    #
    return False

