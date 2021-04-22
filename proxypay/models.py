from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from dateutil import parser

from .api import api
from .configs import conf
from .utils import (
    get_validated_data_for_reference_creation,
    get_calculated_fees
)
from .exceptions import ProxypayException
from .signals import reference_paid, reference_created

# ==========================================================================================================

###
## Paymentt Status
#

PAYMENT_STATUS_WAITING = 0
PAYMENT_STATUS_PAID = 1

# ==========================================================================================================

"""Proxypay References Model Manager"""

class ReferenceModelManager(models.Manager):

    def is_available(self, reference):
        return not self.filter(
            reference=reference,
            status=PAYMENT_STATUS_WAITING,
            expires_in__gt=now()
        ).exists() if reference else False

    def get_reference(self, reference):
        return self.filter(
            reference=reference,
            status=PAYMENT_STATUS_WAITING,
            expires_in__gt=now()
        ).first()

    def create(self, **kwargs):
        # creating the signal and add additional data
        data = kwargs.pop('data', {})
        data['proxypay_fee'] = get_calculated_fees(kwargs['amount'],(
            conf.PROXYPAY_FEE.get('percent', 0),
            conf.PROXYPAY_FEE.get('min_amount'),
            conf.PROXYPAY_FEE.get('max_amount'),
        ))
        data['bank_fee'] = get_calculated_fees(kwargs['amount'],(
            conf.BANK_FEE.get('percent', 0),
            conf.BANK_FEE.get('min_amount'),
            conf.BANK_FEE.get('max_amount'),
        ))
        if data['bank_fee']:
            data['bank_fee']['name'] = conf.BANK_FEE.get('name')
        reference = super(ReferenceModelManager, self).create(data=data, **kwargs)
        # Dispatching Signal
        reference_created.send(
            reference.__class__, 
            reference=reference
        )
        return reference

"""Proxypay References Model"""

class Reference(models.Model):
    
    class Meta:
        verbose_name = _('Reference')
        verbose_name_plural = _('Referencecs')
    
    class Status(models.IntegerChoices):
        WAITING = PAYMENT_STATUS_WAITING, _('Waitng')
        PAID = PAYMENT_STATUS_PAID, _('Paid')

    # reference id
    key                 = models.CharField(_('unique key'), max_length=125, unique=True, editable=False, null=True, default=None)
    reference           = models.CharField(_('reference'), editable=False, max_length=100)
    amount              = models.DecimalField(_('amount'), max_digits=12, decimal_places=2, editable=False)
    entity              = models.CharField(_('entity'), max_length=100, null=True, default=None, editable=False)
    
    # reference payment status: paid, expired, waiting
    status              = models.IntegerField(_('status'), default=Status.WAITING, choices=Status.choices, editable=False)

    # data fields
    fields              = models.JSONField(default=dict) # fileds in proxypay api data reference
    payment             = models.JSONField(default=None, null=True) # payment data form proxypay
    data                = models.JSONField(default=dict) # addtional data

    # date
    paid_at    = models.DateTimeField(_('paid at'), default=None, null=True)
    expires_in = models.DateTimeField(_('expires in'), null=True, default=None)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('update at'), auto_now=True)

    ###
    ##  Manager
    #

    objects = ReferenceModelManager()

    # --------------------------------------------------------------------------------------------
    ###
    ##  Property Methods
    #

    @property
    def expired(self):
        if self.expires_in:
            return self.expires_in < now()
        return False

    @property
    def is_paid(self):
        return self.status == Reference.Status.PAID

    # --------------------------------------------------------------------------------------------
    ###
    ##  Methods
    #

    def delete(self):
        """Delete payment reference from Proxypay and Database"""
        deleted = api.delete_reference(self.reference)
        if deleted:
            return super(Reference, self).delete()
        raise ProxypayException(_('Error when trying to delete the reference in the Proxypay'))

    def paid(self, payment_data):
        """
        Update reference payment status to paid
        Suitable for use with Proxypay's Webhook
        """
        if not self.payment:
            # passando os dados de pagamento na instancia
            self.payment = payment_data
            self.status  = Reference.Status.PAID
            try:
                self.paid_at = parser.isoparse(self.payment.get('datetime'))
            except:
                self.paid_at = now()  
            self.save()
            self.__dispatch_paid_signal()

    def check_payment(self):
        """
        Checks whether the referral payment has already been processed.
        Initially check on the instanse, if it is not processed, check the Proxypay API to be sure. 
        Returns payment data or false
        """
        if not self.payment:
            if (payment := api.check_reference_payment(self.reference)):
                self.paid(payment)
                return payment
            return False
        return self.payment
    

    def update(self):
        if self.expired:
            data        = get_validated_data_for_reference_creation(float(self.amount), self.fields)
            datetime    = data.pop('datetime')
            # updating
            if api.create_or_update_reference(self.reference, data=data):
                self.expires_in = datetime.replace(hour=23,minute=59,second=59)
                self.save()
                return True
        return False

    # --------------------------------------------------------------------------------------------
    ###
    ##  Class Methods
    #

    def __str__(self):
        return  _("Proxypay reference: '%s'") % self.reference

    def __repr__(self):
        return _("Proxypay reference: '%s'") % self.reference

    # --------------------------------------------------------------------------------------------
    ###
    ##  Signals
    #

    def __dispatch_paid_signal(self):
        reference_paid.send(
            self.__class__, 
            reference=self
        )
        