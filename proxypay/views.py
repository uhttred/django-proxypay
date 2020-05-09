###
##  Django Proxypay Views
#

# pyhton stuffs
import hmac, hashlib

# django stuff
from django.http import HttpResponse

# proxypay stuffs
from proxypay.models import Reference
from proxypay.references import get
from proxypay.conf import get_configurations

# ==============================================================================================

def check_signature(signature, raw_http_body):

    """Check Proxypay Signature"""

    # getting private key from settings.py
    private_key = get_configurations().get('token')
    # calcutaing the signature
    computed_signature = hmac.new(
        private_key,
        msg=raw_http_body,
        digestmod=hashlib.sha256
    ).hexdigest()
    # chack vall
    return signature == computed_signature

# ==============================================================================================

def watch_payments(request):

    """View to watch Proxyapy API Webhook"""

    if request.method == 'POST':
        # catch the signature from header
        signature = request.headers.get('X-Signature')
        # check signature
        if check_signature(signature, request.body):
            # payment data
            payment = request.POST
            # gettings the referenc by reference id
            reference = get(payment.get('reference_id'))
            #
            if reference:
                #
                reference.paid( payment )
                # paiment done
                return HttpResponse(status=200)
            # reference not found
            return HttpResponse(status=404)
        # signatue forbidden
        return HttpResponse(status=403)
    # method not allowed
    return HttpResponse(status=405)
