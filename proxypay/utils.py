import datetime
import hmac, hashlib

from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .configs import conf
from .exceptions import ProxypayException

# ==============================================================================================

def get_validated_data_for_reference_creation (amount: float, fields: dict={}, days: int = None) -> dict:
    
    if len(fields) > 9:
        raise ProxypayException(
            _("Error creating reference, <fields> Add 9 max custom fields")
        )
    
    # reference data
    data         = { 'amount': amount, 'custom_fields': fields }
    end_datetime = now() + datetime.timedelta(
        days=conf.get_reference_lifetime(days)
    )
    data['end_datetime'] = end_datetime.strftime("%Y-%m-%d")
    data['datetime'] = end_datetime

    return data

# ==============================================================================================

def check_api_signature(signature, raw_http_body_msg, token=None):
    """Check Proxypay API Signature"""

    private_key = token or conf.get_token()
    # calc the signature
    calc_signature = hmac.new(
        bytearray(private_key, 'utf-8'),
        msg=raw_http_body_msg,
        digestmod=hashlib.sha256
    ).hexdigest()
    # chack vall
    return signature == calc_signature

# ==============================================================================================

def calculate_transaction_fees(amount, fees: tuple):

    percent, min_amount, max_amount = fees
    if percent:
        fees_amount = amount * (percent / 100)
        if min_amount and fees_amount < min_amount:
            expense = min_amount
        elif max_amount and fees_amount > max_amount:
            expense = max_amount
        else:
            expense = fees_amount
        return amount, amount - expense, expense, fees_amount
    return amount, 0, 0, 0