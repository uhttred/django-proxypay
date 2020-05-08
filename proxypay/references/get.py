###
##  Django Proxypay Get Reference
#

# proxypay stuffs
from proxypay.models import Reference

# ==========================================================================================================
 
def get( reference_id ):

    """
    Get a payment reference instance from proxypay.models.Reference
    Returns false if the passed id reference is not found
    """

    try:
        ref = Reference.objects.get(
            reference=reference_id
        )
        return ref
    except:
        return False