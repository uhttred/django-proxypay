from django.contrib import admin
from proxypay.models import Reference

class ReferenceAdmin(admin.ModelAdmin):
    
    list_display = ( 'reference', 'amount', 'paid' )

    def paid(self, obj):
        return True if obj.payment else False

admin.site.register(Reference, ReferenceAdmin)