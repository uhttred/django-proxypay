###
##  Django Proxypay Payment Reference Creation
#



# proxypay stuffs
from proxypay.api import api
from proxypay.models import Reference
from proxypay.references.utils import get_validated_data

# ==========================================================================================================
 
def create(amount, fields={}, days=None):

    """
    Request to proxypay to create a reference and
    returns an instance of proxypay.models.Reference
    """

    # get Generated reference id from proxypay
    reference_id = api.get_reference_id()

    if reference_id:
        
        data        = get_validated_data( amount, fields, days )
        datetime    = data.pop('datetime')
        # trying to create the reference
        ok = api.create_or_update_reference(reference_id,data)
        #
        if ok:
            # saving to the database
            return Reference.objects.create(
                reference=reference_id,
                amount=amount,
                entity=api.entity,
                fields=fields,
                # By default, proxypay references expire at the end of each day
                expires_in=datetime.replace(hour=23,minute=59,second=59)
            )
    return False
