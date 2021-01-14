###
##  Django Proxypay Reference Model
#

# django stuff
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from dateutil import parser
from django.db.models.constraints import UniqueConstraint

# proxypay stuff
from proxypay.api import api
from proxypay.references.utils import get_validated_data
from proxypay.exceptions import ProxypayException
from proxypay.signals import reference_paid, reference_created

# ==========================================================================================================

###
## Paymentt Status
#

PAYMENT_STATUS_WAITING = 0
PAYMENT_STATUS_PAID = 1
PAYMENT_STATUS_CHOICES = (
    (PAYMENT_STATUS_WAITING , 'Waiting'),
    (PAYMENT_STATUS_PAID , 'Paid')
)

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
        # creating the signal
        reference = super(ReferenceModelManager, self).create(**kwargs)
        # Dispatching Signal
        reference_created.send(
            reference.__class__, 
            reference=reference
        )
        #
        return reference

"""Proxypay References Model"""

class Reference(models.Model):

    ###
    ## Model Attributes
    #

    # reference id
    key                 = models.CharField(max_length=125, unique=True, editable=False, null=True, default=None)
    reference           = models.IntegerField(verbose_name=_('Reference'), editable=False)
    amount              = models.DecimalField(verbose_name=_('Amount'), max_digits=12, decimal_places=2, editable=False)
    entity              = models.CharField(verbose_name=_('Entity'), max_length=100, null=True, default=None, editable=False)
    fields              = models.JSONField(default=dict)
    # reference payment status: paid, expired, waiting
    status              = models.CharField(max_length=10, default=PAYMENT_STATUS_WAITING, editable=False)
    payment             = models.JSONField(default=None, null=True)

    is_paid    = models.BooleanField(default=False)
    paid_at    = models.DateTimeField(default=None, null=True)
    # date
    expires_in = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Update At'), auto_now=True)


    ###
    ##  Manager
    #

    objects = ReferenceModelManager()

    # --------------------------------------------------------------------------------------------
    ###
    ##  Methods
    #

    def delete(self):

        """Delete payment reference from Proxypay and Database"""

        # deleting from proxypay
        deleted = api.delete_reference(self.reference)
        # 
        if deleted:
            return super(Reference, self).delete()

        raise ProxypayException('Error when trying to delete the reference in the Proxypay')

    def paid(self, payment_data):

        """
        Update reference payment status to paid
        Suitable for use with Proxypay's Webhook
        """

        if not self.payment:
            
            # passando os dados de pagamento na instancia
            self.payment = payment_data
            self.status = PAYMENT_STATUS_PAID
            self.is_paid = True

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
            # check from api
            payment = api.check_reference_payment(self.reference)
            # case already paid
            if payment:
                self.paid(payment)
            # returns payment data or false
            return payment
        # returning the payment data already registered
        return self.payment
    

    def update(self):
        if self.expired:
            data        = get_validated_data(float(self.amount), self.fields)
            datetime    = data.pop('datetime')
            # updating
            if api.create_or_update_reference(self.reference, data=data):
                self.expires_in = datetime.replace(hour=23,minute=59,second=59)
                self.save()
                return True
        return False
            
    # --------------------------------------------------------------------------------------------
    ###
    ##  Property Methods
    #

    @property
    def expired(self):
        if self.expires_in:
            return self.expires_in < now()
        return False

    # --------------------------------------------------------------------------------------------
    ###
    ##  Class Methods
    #

    def __str__(self):
        return f"Proxypay Reference: {self.reference}"

    def __repr__(self):
        return f"Proxypay Reference: {self.reference}"

    # --------------------------------------------------------------------------------------------
    ###
    ##  Signals
    #

    def __dispatch_paid_signal(self):
        # Dispatching Signal
        reference_paid.send(
            self.__class__, 
            reference=self
        )
        