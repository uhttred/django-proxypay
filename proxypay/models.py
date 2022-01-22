import decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from django_admin_display import admin_display as d

from .api import api
from .utils import (
    get_validated_data_for_reference_creation,
    get_decimal_value,
    str_to_datetime
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
        reference = super(ReferenceModelManager, self).create(**kwargs)
        # Dispatching Signal
        reference_created.send(
            reference.__class__, 
            reference=reference
        )
        return reference

class Reference(models.Model):
    
    class Meta:
        verbose_name = _('Reference')
        verbose_name_plural = _('References')
    
    class Status(models.IntegerChoices):
        WAITING = PAYMENT_STATUS_WAITING, _('Waitng')
        PAID = PAYMENT_STATUS_PAID, _('Paid')

    # reference id
    key                 = models.CharField(_('unique key'), max_length=125, unique=True, editable=False, null=True, default=None)
    reference           = models.CharField(_('reference'), editable=False, max_length=100)
    amount              = models.DecimalField(_('amount'), max_digits=12, decimal_places=2)
    entity              = models.CharField(_('entity'), max_length=100, null=True, default=None, editable=False)
    
    # reference payment status: paid, expired, waiting
    status              = models.IntegerField(_('status'), default=Status.WAITING, choices=Status.choices, editable=False)

    # data fields
    fields              = models.JSONField(_('reference data fields'), default=dict) # fileds in proxypay api data reference
    payment             = models.JSONField(_('payment data from proxypay'), default=None, null=True) # payment data form proxypay
    data                = models.JSONField(_('additional data'), default=dict) # addtional data

    # date
    paid_at    = models.DateTimeField(_('paid at'), default=None, null=True)
    expires_in = models.DateTimeField(_('expires in'), null=True, default=None)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('update at'), auto_now=True)

    objects = ReferenceModelManager()

    # --------------------------------------------------------------------------------------------
    ###
    ##  Property Methods
    #

    @property
    def payment_data(self):
        return self.payment or {}
    
    @property
    def bank_fee_data(self):
        return self.data.get('bank_fee', {})
    
    @property
    def proxypay_fee_data(self):
        return self.data.get('proxypay_fee', {})

    # @property
    @d(short_description=_('Expired'), boolean=True)
    def expired(self):
        if self.expires_in:
            return self.expires_in < now()
        return False

    # @property
    @d(short_description=_('Is Paid'), boolean=True)
    def is_paid(self):
        return self.status == Reference.Status.PAID
    
    @property
    @d(short_description=_('Proxypay Fee'))
    def proxypay_fee(self):
        if (fee := self.data.get('proxypay_fee')):
            return fee.get('expense', 0)
        return 0
    
    @property
    @d(short_description=_('Bank Fee'))
    def bank_fee(self):
        if (fee := self.data.get('bank_fee')):
            return fee.get('expense', 0)
        return 0
        
    @property
    @d(short_description=_('Fees Expense'))
    def fees_expense(self):
        return decimal.Decimal('%.2f' % (self.proxypay_fee + self.bank_fee))
    
    @property
    @d(short_description=_('Net Amount'))
    def net_amount(self):
        return self.amount - self.fees_expense

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
                self.paid_at = str_to_datetime(self.payment.get('datetime'))
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
        return  _("Proxypay reference: '%s' <> key: '%s'") % (self.reference, self.key)

    def __repr__(self):
        return _("Proxypay reference: '%s' <> key: '%s'") % (self.reference, self.key)

    # --------------------------------------------------------------------------------------------
    ###
    ##  Signals
    #

    def __dispatch_paid_signal(self):
        reference_paid.send(
            self.__class__, 
            reference=self
        )
        