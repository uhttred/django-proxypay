###
##  Django Proxypay Views
#

# pyhton stuffs
import hmac, hashlib, json
from proxypay.models import reference

# django stuff
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# proxypay stuffs
from proxypay.references import get
from proxypay.conf import get_private_key
from proxypay.conf import PP_AUTO_PAYMENT_REF_ID

# ==============================================================================================

def check_signature(signature, raw_http_body):

    """Check Proxypay Signature"""

    # getting private key from settings.py
    private_key = get_private_key()
    # calc the signature
    calc_signature = hmac.new(
        bytearray(private_key, 'utf-8'),
        msg=raw_http_body,
        digestmod=hashlib.sha256
    ).hexdigest()
    # chack vall
    return signature == calc_signature

# ==============================================================================================

@csrf_exempt
def watch_payments (request):

    """View to watch Proxyapy API Webhook"""

    if request.method == 'POST':
        # check signature
        if check_signature(request.headers.get('X-Signature'), request.body):
            # payment data
            payment = json.loads(request.body)
            # getting reference id
            reference_id = payment.get('custom_fields', {}).get(PP_AUTO_PAYMENT_REF_ID)
            if not reference_id:
                print('No FROM DJPP_ID')
                reference_id = payment.get('reference_id')
            print(payment)
            print(reference_id)
            print(payment.get('reference_id'))
            reference = get(reference_id)
            print(reference)
            # chack reference
            if reference:
                # update as paid
                reference.paid(payment)
                # paiment done
                return HttpResponse(status=200)
            # reference not found
            return HttpResponse(status=404)
        # forbidden signatue
        return HttpResponse(status=403)
    # method not allowed
    return HttpResponse(status=405)
