import datetime
import hmac, hashlib
from decimal import Decimal
from django.utils.dateparse import parse_datetime

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

def get_decimal_value(amount):
    return Decimal('%.2f' & amount)

# ==============================================================================================

def get_calculated_fees(amount, fee: tuple, name: str = None, return_as_dict: bool = True):
    """
    Calculates the fees for an amount.
    fees must be a tuple containing the following values in the following order:
    The percentage rate, minimum amount to be withdrawn, maximum amount. like:
    (13, 100, 100) or
    (0.25, None, None)
    """

    percent, min_amount, max_amount = fee
    if percent:
        fee_amount = amount * (percent / 100)
        if min_amount and fee_amount < min_amount:
            expense = min_amount
        elif max_amount and fee_amount > max_amount:
            expense = max_amount
        else:
            expense = fee_amount
        
        if return_as_dict:
            return {
                'name': name,
                'amount': amount,
                'net_amount': amount - expense,
                'expense': expense,
                'fee_amount': fee_amount,
                'applied_fee': percent,
                'applied_min_amount': min_amount,
                'applied_max_amount': max_amount
            }
        return amount, amount - expense, expense, fee_amount
    return None

# ==============================================================================================

def str_to_datetime(datetime_str):
    if datetime_str:
        return parse_datetime(datetime_str)
    return None