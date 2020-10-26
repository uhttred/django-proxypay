###
##  Django Proxypay Payment Test
#

# django stuff
from django.core.management.base import BaseCommand

# proxypay stuff
from proxypay.api import api
from proxypay.models import Reference
from proxypay.conf import PP_CONFIG_DEFAULT_DEVELOPMENT_ENV

# =====================================================================================================================

class Command(BaseCommand):

    help = 'For testing payments with Proxypay in the development environment'

    def add_arguments(self, parser):
        parser.add_argument('command', nargs='+', type=str)

    def handle(self, *args, **options):

        # command
        args = options.pop('command')

        # test payment
        if args[0] == 'pay':

            if api.env != PP_CONFIG_DEFAULT_DEVELOPMENT_ENV:
                raise Exception('It is only possible to make fictitious payments in a sandbox environment')

            # getting the reference id from args
            reference_id = int(args[1])
            # get Reference model instance
            reference = Reference.objects.get(reference=reference_id)
            # paying
            r = api.post('/payments', data={
                'amount': float(reference.amount),
                'reference_id': reference.reference
            })
            # r status
            if r.status_code == 200:
                # paid successfully
                payment = r.json()
                #
                reference.paid(payment)
                # 
                self.stdout.write(self.style.SUCCESS(f"Reference: <{reference.reference}>, paid successfully"))
                #
                api.acknowledge_payment(payment.get('id'))
            else:
                self.stdout.write(self.style.ERROR(f"Proxypay returns {r.status_code} status code from API"))