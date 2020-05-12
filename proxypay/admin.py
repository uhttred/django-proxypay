from django.contrib import admin
from proxypay.models import Reference
from django.utils.translation import ugettext_lazy as _

class ReferenceAdmin(admin.ModelAdmin):
    
    list_display = ( 
        'reference',
        'entity', 
        'amount', 
        'paid', 
        'payment_tarminal',
        'payment_local',
        'expired',
        'expires_in',
        'created_at',
        'updated_at'
    )

    search_fields = (
        'reference',
        'amount',
    )

    ordering = (
        'created_at',
        'updated_at',
        'amount',
    )

    ###
    ## 
    #

    def paid(self, obj):
        return _('Yes') if obj.payment else _('No')

    def expired(self, obj):
        return _('Yes') if obj.expired else _('No')

    def payment_local(self, obj):
        if obj.payment:
            return obj.payment.get('terminal_location')
        return None

    def payment_tarminal(self, obj):
        if obj.payment:
            return obj.payment.get('terminal_type')
        return None
            
    paid.short_description = _('Paid')
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