###
##  Django Proxypay Get Reference
#

# proxypay stuffs
from proxypay.models import Reference

# ==========================================================================================================
 
def get (reference_id):

    """
    Get a payment reference instance from proxypay.models.Reference
    Returns false if the passed id reference is not found
    """

    return Reference.objects.get_reference(reference=reference_id)