from django.contrib import admin
from proxypay.models import Reference
from django.utils.translation import ugettext_lazy as _

class ReferenceAdmin(admin.ModelAdmin):

    # --------------------------------------------------------------------------------------------
	###
	## Settings Properties
	#
    
    list_display = ( 
        'reference',
        'amount', 
        'entity', 
        'payment_local',
        'payment_tarminal',
        'paid_at',
        'created_at',
        'updated_at',
        'expires_in',
        'expired',
        'is_paid', 
    )

    ordering         = ('-created_at', 'updated_at', 'amount')
    search_fields    = ('reference', 'amount')
    list_filter      = ('is_paid', 'entity')

    date_hierarchy   = 'created_at'


    ###
    ## 
    #

    def expired(self, obj):
        return obj.expired

    def payment_local(self, obj):
        if obj.payment:
            return obj.payment.get('terminal_location')
        return None

    def payment_tarminal(self, obj):
        if obj.payment:
            return obj.payment.get('terminal_type')
        return None
            
    expired.boolean = True
    payment_local.short_description = _('Paid In')
    payment_tarminal.short_description = _('Paid With')

    ###
    ## Permissions
    #

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False

admin.site.register(Reference, ReferenceAdmin)