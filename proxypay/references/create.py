###
##  Django Proxypay Payment Reference Creation
#

# python stuffs
import datetime

# proxypay stuffs
from proxypay.api import api
from proxypay.conf import get_default_reference_expires_days
from proxypay.exceptions import ProxypayException
from proxypay.models import Reference

# django stuff
from django.utils.timezone import now

# ==========================================================================================================
 
def create(amount, fields={}, days=None):

    """
    Request to proxypay to create a reference and
    returns an instance of proxypay.models.Reference
    """

    # get Generated reference id from proxypay
    reference_id = api.get_reference_id()

    if reference_id:
        
        ###
        ## Custom Fields
        #

        if len(fields) > 10:
            # 
            raise ProxypayException('Error creating reference, <fields> Add 10 max custom fields')
        
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

        elif days:
            # days value error
            raise ProxypayException('Error creating reference, <days> must be an integer')
        
        # trying to create the reference
        ok = api.create_or_update_reference(reference_id, data)
        #
        if ok:
            # saving to the database
            reference = Reference.objects.create(
                reference=reference_id,
                amount=amount,
                entity=api.entity,
                fields=fields,
                # By default, proxypay references expire at the end of each day
                expires_in=end_datetime.replace(hour=23,minute=59,second=59) if end_datetime else None
            )
            #
            return reference
    #
    return False
