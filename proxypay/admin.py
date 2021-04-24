from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django_admin_display import admin_display as d

from proxypay.utils import str_to_datetime
from proxypay.models import Reference
from proxypay.references import create

# --------------------------------------------------------------------------------------------

LIST_REFERENCE = ('key', 'reference', 'entity')
LIST_BANK_AMOUNT_AND_FEES = (
    'bank_name',
    'bank_fee_percent',
    'bank_fee_amount',
    'bank_fee_min_amount',
    'bank_fee_max_amount',
    'bank_fee',
    'bank_net_amount',
)
LIST_PROXYPAY_AMOUNT_AND_FEES = (
    'proxypay_fee_percent',
    'proxypay_fee_amount',
    'proxypay_fee_min_amount',
    'proxypay_fee_max_amount',
    'proxypay_fee',
    'proxypay_net_amount',
)
LIST_AMOUNT_AND_FEES = (
    'amount',
    'net_amount',
    'fees_expense'
)
LIST_PRODUCT_AND_SERVICE = (
    'product',
    'service'
)
LIST_PAYMENT = (
    'payment_product_id',
    'payment_location',
    'payment_tarminal_type',
    'payment_tarminal_id',
    'payment_transaction_id',
    'payment_period_id',
    'payment_period_end_datetime',
    'payment_period_start_datetime'
)
LIST_DATE = (
    'created_at',
    'updated_at',
    'expires_in',
    'paid_at'
)
LIST_STATUS = (
    'expired',
    'is_paid',
    'status'
)
LIST_RAW_DATA = (
    'fields',
    'payment',
    'data'
)

# --------------------------------------------------------------------------------------------

class AddForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ('amount', 'days')
    
    days = forms.IntegerField(max_value=45, initial=1, label=_('Days'),help_text=_('days for expiration'))

    def save(self, *args, **kwargs):
        super().save(commit=False)
        return create(
            amount=float(self.cleaned_data.get('amount')),
            days=self.cleaned_data.get('days')
        )

# --------------------------------------------------------------------------------------------

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):

    # --------------------------------------------------------------------------------------------
	###
	## Settings Properties
	#
    
    list_display = ( 
        'reference',
        'entity', 
        'amount',
        'net_amount',
        'fees_expense',
        'bank_fee',
        'proxypay_fee',
        'created_at',
        'paid_at',
        'key',
        'expired',
        'is_paid'
    )

    readonly_fields = (
        LIST_REFERENCE +
        LIST_AMOUNT_AND_FEES +
        LIST_PRODUCT_AND_SERVICE +
        LIST_PROXYPAY_AMOUNT_AND_FEES +
        LIST_BANK_AMOUNT_AND_FEES +
        LIST_PAYMENT +
        LIST_DATE +
        LIST_STATUS +
        LIST_RAW_DATA
    )

    ordering         = ('-created_at', 'updated_at', 'amount')
    search_fields    = ('key', 'reference', 'amount')
    list_filter      = ('status', 'entity')
    fieldsets = (
        (_('Reference'), {'fields': LIST_REFERENCE }),
        (_('Amount and Fees'), {'fields': LIST_AMOUNT_AND_FEES }),
        (_('Related Product and Service'), {'fields': LIST_PRODUCT_AND_SERVICE }),
        (_('Proxypay Amount and Fee'), {'fields': LIST_PROXYPAY_AMOUNT_AND_FEES }),
        (_('Bank Amount and Fee'), {'fields': LIST_BANK_AMOUNT_AND_FEES }),
        (_('Proxypay Payment Details'), {'fields': LIST_PAYMENT }),
        (_('Dates'), {'fields': LIST_DATE }),
        (_('Status'), {'fields': LIST_STATUS }),
        (_('Raw Data'), {'fields': LIST_RAW_DATA }),
    )

    date_hierarchy   = 'created_at'
    form = AddForm

    # --------------------------------------------------------------------------------------------
    # Payment Details

    @d(short_description=_('Period ID'))
    def payment_period_id(self, obj):
        return obj.payment_data.get('period_id')
    
    @d(short_description=_('Payment Period Start At'))
    def payment_period_start_datetime(self, obj):
        return str_to_datetime(
            obj.payment_data.get('period_start_datetime')
        )
    
    @d(short_description=_('Payment Period End At'))
    def payment_period_end_datetime(self, obj):
        return str_to_datetime(
            obj.payment_data.get('period_end_datetime')
        )

    @d(short_description=_('Payment Location'))
    def payment_location(self, obj):
        return obj.payment_data.get('terminal_location')

    @d(short_description=_('Payment Terminal Type'))
    def payment_tarminal_type(self, obj):
        return obj.payment_data.get('terminal_type')
    
    @d(short_description=_('Payment Terminal ID'))
    def payment_tarminal_id(self, obj):
        return obj.payment_data.get('terminal_id')
    
    @d(short_description=_('Payment Transaction ID'))
    def payment_transaction_id(self, obj):
        return obj.payment_data.get('transaction_id')
    
    @d(short_description=_('Payment Product ID'))
    def payment_product_id(self, obj):
        return obj.payment_data.get('product_id')

    # --------------------------------------------------------------------------------------------
    # Prouct and Service Details

    @d(short_description=_('Product'))
    def product(self, obj):
        return obj.fields.get('product')
    
    @d(short_description=_('Service'))
    def service(self, obj):
        return obj.fields.get('service')

    # --------------------------------------------------------------------------------------------
    # Bank Details

    @d(short_description=_('Bank Name'))
    def bank_name(self, obj):
        return obj.bank_fee_data.get('name')
    
    @d(short_description=_('Bank Net Amount'))
    def bank_net_amount(self, obj):
        return obj.bank_fee_data.get('net_amount')
    
    @d(short_description=_('Bank Fee Percentage'))
    def bank_fee_percent(self, obj):
        return obj.bank_fee_data.get('applied_fee')
    
    @d(short_description=_('Bank Fee Amount'))
    def bank_fee_amount(self, obj):
        return obj.bank_fee_data.get('fee_amount')
    
    @d(short_description=_('Bank Applied Min Amount'))
    def bank_fee_min_amount(self, obj):
        return obj.bank_fee_data.get('applied_min_amount') or _('Not Applied')
    
    @d(short_description=_('Bank Applied Max Amount'))
    def bank_fee_max_amount(self, obj):
        return obj.bank_fee_data.get('applied_max_amount') or _('Not Applied')
    
    # --------------------------------------------------------------------------------------------
    # Proxypay Details
    
    @d(short_description=_('Net Amount'))
    def proxypay_net_amount(self, obj):
        return obj.proxypay_fee_data.get('net_amount')
    
    @d(short_description=_('Fee Percentage'))
    def proxypay_fee_percent(self, obj):
        return obj.proxypay_fee_data.get('applied_fee')
    
    @d(short_description=_('Fee Amount'))
    def proxypay_fee_amount(self, obj):
        return obj.proxypay_fee_data.get('fee_amount')
    
    @d(short_description=_('Applied Min Amount'))
    def proxypay_fee_min_amount(self, obj):
        return obj.proxypay_fee_data.get('applied_min_amount') or _('Not Applied')
    
    @d(short_description=_('Applied Max Amount'))
    def proxypay_fee_max_amount(self, obj):
        return obj.proxypay_fee_data.get('applied_max_amount') or _('Not Applied')

    # --------------------------------------------------------------------------------------------
    ###
    ## Base Permissions
    #

    def get_readonly_fields(self, request, obj=None):
        if not obj: # editing an existing object
            return tuple((field for field in self.readonly_fields if field not in ('amount', 'days')))
        return self.readonly_fields
    
    def get_fieldsets(self, request, obj = None):
        if not obj:
            return (
                (_('Creating Proxypay Payment Reference'), {'fields': ('amount', 'days')}),
            )
        return super().get_fieldsets(request, obj=obj)

    # --------------------------------------------------------------------------------------------
    ###
    ## Base Permissions
    # 

    # def has_add_permission(self, *args, **kwargs):
    #     return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False