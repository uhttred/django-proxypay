###
##  Django Proxypay Get Reference
#

# ==========================================================================================================
 
def get (key, reference_id=False):

    """
    Get a payment reference instance from proxypay.models.Reference
    Returns false if the passed id reference is not found
    """

    from proxypay.models import Reference

    try:
        return Reference.objects.get(key=key)
    except:
        if reference_id:
            return Reference.objects.get_reference(
                reference=reference_id
            )
        return False