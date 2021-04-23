from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from proxypay.api import api
from proxypay.references import get
from proxypay.configs import conf

# =====================================================================================================================

class Command(BaseCommand):

    help = _('For testing payments with Proxypay in the development environment')

    def add_arguments(self, parser):
        parser.add_argument('command', nargs='+', type=str)

    def handle(self, *args, **options):
        args = options.pop('command')
        # test payment
        if args[0] == 'pay':
            if api.env != conf.SANDBOX_ENV:
                raise Exception(_('It is only possible to make fictitious payments in a sandbox environment'))
            
            reference = get(key=args[1], reference_id=args[1])
            r = api.post('/payments', data={
                'amount': float(reference.amount),
                'reference_id': reference.reference
            })

            if r.status_code == 200:
                self.stdout.write(self.style.SUCCESS(_("Reference: '%s', paid successfully") % reference.reference))
                if conf.ACKNOWLEDGE_MOCK_PAYMENT_LOCALLY_AUTOMATICALLY:
                    payment = r.json()
                    reference.paid(payment)
                    api.acknowledge_payment(payment.get('id'))
                    self.stdout.write(self.style.SUCCESS(_('Mock payment acknowledged automatically')))
            else:
                self.stdout.write(self.style.ERROR(
                    _("Proxypay returns '%d' status code from API") % r.status_code
                ))