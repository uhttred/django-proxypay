import json
from .references import get
from .configs import conf
from .utils import check_api_signature

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# ==============================================================================================

@csrf_exempt
def watch_payments (request):
    """View to watch Proxyapy API Webhook"""
    if request.method == 'POST':
        if check_api_signature(request.headers.get('X-Signature'), request.body):
            confirmed   = conf.ACCEPT_UNRECOGNIZED_PAYMENT
            payment     = json.loads(request.body)
            reference   = get(
                # getting from uuid or reference id
                payment.get('custom_fields', {}).get(conf.REFERENCE_UUID_KEY),
                payment.get('reference_id')
            )
            # check reference
            if reference:
                reference.paid(payment)
                confirmed = True
            #
            if confirmed:
                return HttpResponse(status=200)
            return HttpResponse(status=404)
        return HttpResponse(status=403)
    return HttpResponse(status=405)
