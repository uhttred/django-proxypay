###
##  Django Proxypay Payment Reference Creation
#



# proxypay stuffs
from proxypay.api import api
from proxypay.models import Reference
from proxypay.references.utils import get_validated_data
from proxypay.conf import PP_AUTO_PAYMENT_REF_ID

# ==========================================================================================================
 
def create(amount, fields={}, days=None):

    """
    Request to proxypay to create a reference and
    returns an instance of proxypay.models.Reference
    """

    tryTimes = 3

    while tryTimes > 0:
        tryTimes -= 1
        # Get Generated reference id from proxypay
        referenceId = api.get_reference_id()
        if not Reference.objects.is_available(referenceId):
            continue
        #
        data        = get_validated_data(amount, fields, days)
        data['custom_fields'][PP_AUTO_PAYMENT_REF_ID] = str(referenceId)
        datetime    = data.pop('datetime')
        # trying to create the reference
        if api.create_or_update_reference(referenceId, data):
            # saving to the database
            return Reference.objects.create(
                reference=referenceId,
                amount=amount,
                entity=api.entity,
                fields=fields,
                # By default, proxypay references expire at the end of each day
                expires_in=datetime.replace(hour=23,minute=59,second=59)
            )
        else:
            break
    return False
