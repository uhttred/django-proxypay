###
##  Django Proxypay Exceptions
#

class ProxypayException(Exception):
    pass

class ProxypayKeyError(KeyError):
    pass

class ProxypayValueError(Exception):
    pass