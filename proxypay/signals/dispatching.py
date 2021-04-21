###
##  Django Proxypay Signals
#

# django stuffs
import django.dispatch

# =============================================================================

###
##  Dispatching Signals
#

reference_paid = django.dispatch.Signal([
    'reference'
])

reference_created = django.dispatch.Signal([
    'reference'
])

# =============================================================================

