###
##  Django Proxypay Signals
#

# django stuffs
import django.dispatch
from django.dispatch import receiver 

# =============================================================================

###
##  Dispatching Signals
#

reference_paid = django.dispatch.Signal([
    'reference'
])

# =============================================================================

