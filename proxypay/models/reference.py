###
##  Django Proxypay Reference Model
#

# python stuff
import json

# django stuff
from django.db import models

# proxypay stuff
from proxypay.api import api
from proxypay.exceptions import ProxypayException
from proxypay.signals import reference_paid

# ==========================================================================================================
 
class Reference(models.Model):

    ###
    ## Model Attributes
    #

    # reference id
    reference           = models.IntegerField(unique=True)
    amount              = models.DecimalField(max_digits=12, decimal_places=2)
    custom_fields_text  = models.TextField(default='')
    # paid status
    paid                = models.BooleanField(default=False)
    # reference payment status: canceled, paid, expired, wait
    payment_status      = models.CharField(max_length=50, default='wait')

    # date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ###
    ##  Methods
    #

    # cancel reference on proxypay and delete instance

    def delete(self):

        """Delete payment reference from Proxypay and Database"""

        # deleting from proxypay
        deleted = api.delete_reference(self.reference)
        # 
        if deleted:
            return super(Reference, self).delete()

        raise ProxypayException('Error when trying to delete the reference in the Proxypay')

    # update reference payment status to paid

    def payment_done(self):

        """update reference payment status to paid"""
        
        # changing fields
        self.paid           = True
        self.payment_status = 'paid'
        # save instance
        self.save()
        # Dispatching Signal
        reference_paid.send(
            self.__class__, 
            reference=self
        )

        # return the instance
        return self



    ###
    ## Property Methods
    #

    @property
    def fields(self):
        return json.loads(self.custom_fields_text)

    ###
    ## Classe Method
    #

    def __str__(self):
        return f"Proxypay Reference: {self.reference}"

    def __repr__(self):
        return f"Proxypay Reference: {self.reference}"

