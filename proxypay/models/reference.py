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

# ==========================================================================================================
 
class Reference(models.Model):

    ###
    ## Model Attributes
    #

    reference = models.IntegerField(unique=True)
    amount    = models.DecimalField(max_digits=12, decimal_places=2)
    custom_fields_text = models.TextField(default='')

    # date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

