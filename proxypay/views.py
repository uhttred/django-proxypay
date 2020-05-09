###
##  Django Proxypay Views
#

# django stuff
from django.http import JsonResponse

# proxypay stuffs
from proxypay.models import Reference
from proxypay.references import get

# ==============================================================================================

def check_signature(signature):
    return False

def watch_payments(request):

    """View to watch Proxyapy API Webhook"""

    if request.method == 'POST':
        # catch the signature from header
        signature = request.headers.get('X-Signature')
        # check signature
        if check_signature(signature):
            # payment data
            payment = request.POST
            # gettings the referenc by reference id
            reference = get(payment.get('reference_id'))
            #
            if reference:
                reference.paid(
                    payment
                )
                # paiment done
                return JsonResponse(status=200)
            # reference not found
            return JsonResponse(status=404)
        # signatue forbidden
        return JsonResponse(status=403)
    # method not allowed
    return JsonResponse(status=405)
