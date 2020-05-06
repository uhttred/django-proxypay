

class ProxypayException(Exception):

    def __init__(self, message, prefix='ProxypayError'):
        #
        self.message = message 
        self.prefix  = prefix

    def __str__(self):
        #
        return f"{self.prefix}: {self.message}"
