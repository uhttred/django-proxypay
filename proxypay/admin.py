from django.contrib import admin
from proxypay.models import Reference
from django.utils.translation import ugettext_lazy as _

class ReferenceAdmin(admin.ModelAdmin):
    
    list_display = ( 
        'reference',
        'entity', 
        'amount', 
        'paid', 
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
            
    paid.description = _('Paid')

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