django-proxypay
=================

Django Proxypay is a [Django Framework](https://www.djangoproject.com/) application/library that facilitates the integration of your Django project with the [Proxypay](https://proxypay.co.ao/) [API](https://developer.proxypay.co.ao/v2/). Allowing to generate referrals, recognize payments and look through Proxypay's webhooks.

> If you are looking for a Python alternative that doesn't use any framework, maybe [proxypay-py](https://pypi.org/project/proxypay-py/) could be useful. [proxypay-py](https://pypi.org/project/proxypay-py/) is the official Proxypay library maintained by [TimeBoxed](http://timeboxed.co.ao/)

----------------------------------------------------------------------------------

### Some Features

The Django Proxypay really comes to facilitate the integration to the Proxypay API, leaving all interaction with Proxypay totally out of the box. Letting you focus more on data validation and / or the Frontend

* Generate references and store them in the database
* Verify payment directly from a reference instance
* Acknowledge payment
* Recognize payments automatically using Proxypay webhooks
* Mock Payment, for development tests
* Of course, Signals, notifying you when a payment is recognized or a reference is created or updated.

------------------------------------------------------------------------------------------------------------------

## Installation

Simple **django-proxypay** can be installed with ``pip``:

    pip install django-proxypay

Or from this repository:

    pip install -e git+https://github.com/txiocoder/django-proxypay.git@master#egg=django-proxypay

#### Requirements

* Python ``3.8; ``
* Django ``3.0;``
* requests ``2.23``
* django-admin-display

These are the officially supported python and package versions. Other versions will probably work

## Configurations

As stated above, Django Proxypay is a Django Application. To configure your project you simply need to add ``proxypay`` to your ``INSTALLED_APPS`` and configure the ``PROXYPAY`` variable in the ``settings.py`` file

for more details on how to configure the PROXYPAY variable, access the proxypay.conf file

Like the example below, file ``settings.py``:

```python
# Your project applications
INSTALLED_APPS = [
    'proxypay',
]

# Proxypay Configurations
PROXYPAY = {
    # (str) Your Proxypay authorization token key
    'PRIVATE_KEY': os.environ.get('PP_PRIVATE_KEY'),
    # (int) Your Proxypay Entity ID
    'ENTITY': os.environ.get('PP_ENTITY'),
    # (int) Optional, Default: 1 
    # days to expire a reference
    'REFERENCE_LIFE_TIME_IN_DAYS': os.environ.get('PP_REFERENCE_LIFE_TIME_IN_DAYS'),
    # (bool) Optional, default: False
    # If True, proxypay.payments.watch will return status 200
    # if a payment confirmation is sent whose reference has not been registered
    'ACCEPT_UNRECOGNIZED_PAYMENT': os.environ.get('PP_ACCEPT_UNRECOGNIZED_PAYMENT'),
    # (bool) Optional, default: True
    # If true, in sandbox env mode fictitious payments will be processed automatically without the proxypay webhook.
    # Useful if you want to test local payments without configuring the endpoint watch payments on proxypay
    'ACKNOWLEDGE_MOCK_PAYMENT_LOCALLY_AUTOMATICALLY': os.environ.get('PP_ACKNOWLEDGE_MOCK_PAYMENT_LOCALLY_AUTOMATICALLY')
    # (str) Optional, the proxypay api environment to use
    # If not set, by default Proxypay will use the sandbox environment if settings.DEBUG is True 
    # and produnction if is False
    # If set, the value must be sandbox or production
    'ENV': os.environ.get('PP_ENV'),
    # (tuple) Optional
    # fees
    # fee must be a tuple in this order: Fee Name, Fee Percent, Min Amount, Max Amount
    'PROXYPAY_FEE': ('Proxypay', 0.25, 50, 1000),
    'BANK_FEE': (None, 0, 0, 0),
}
```

**Note**: That's all, make sure to run the database migrations. Using the commands ``python manage.py makemigrations`` and ``python manage.py migrate`` to generate a table of References in the database

## Basic use

### Creating references and verifying payments

Use the `` proxypay.references.create`` method to create new references. This method will return an instance of `` proxypay.models.Reference``. Which you can use to verify payment and other data such as related entity, reference id and more

```python
from proxypay.references import create

###
## Creating References
#

# simple like that
reference = create(1780.78)

# or
reference2 = create(
    # the reference amount
    amount=3500,
    # (dict) Optional, custom_fields to add to refence instance and proxypay payment data
    # Make sure to use just strings
    fields={
        'product': 'some',
        'service': 'some service name'
    },
    # (int) Optional, Number of days to expire the reference
    days=3,
)

# Check if a reference was paid / Acknowledge Payment for this reference
# will return False or the payment data from Proxypay API in a dict structure
payment = reference.check_payment() 
```

### Proxypay Webhooks, watching for payments

You can avoid manually checking for paid references. Django Proxypay comes with a view ready to keep an eye on the Proxypay API Webhooks. This view will check the signature, find the related `` proxypay.models.Reference`` instance and update as paid. At the end it will trigger the `` reference_paid`` signal.

To use, you only need to add the endpoint that will be used by the Proxypay API. As in the example below. In your `` urls.py`` file:

```python
# django stuffs
from django.urls import path
from django.contrib import admin

# proxypay watch payments view
from proxypay.views import watch_payments

urlpatterns = [
    path( "admin/", admin.site.urls),
    # Note, the URL name can be whatever you want
    path('proxypay-payments', watch_payments),
]
```

**Note**: Don't forget to configure the endpoint in your Proxypay account

### Working with Signals

Signals are the best way to keep an eye on new reference or new payments. So, in your ``signals.py`` file:

```python
from django.dispatch import receiver
from proxypay.signals import reference_paid, reference_created

# receive a paid reference
@receiver(reference_paid)
def handle_paid_reference(sender, reference, **kwargs):
    # will print out the reference
    print(f"Reference {reference.reference} was paid!")
    # You can also check the payment data received  from Proxypay
    print('(dict) Payment Data: ', reference.payment)

# receive a created reference
@receiver(reference_created)
def handle_created_reference(sender, reference, **kwargs):
    print(f"Reference {reference.reference} was created!")
```

## Mock Payment

In development mode, you can create fictitious payments to test your application. Using Django's ``manage.py`` in your terminal like below:

```bash

# reference ID or key
python manage.py proxypay pay 123902092

```

This command will search for the reference in the database, if found and has not yet been paid, it will make the payment. This time, the signal will be triggered, and you will be able to simulate it as if the payment confirmation came from Proxypay's Webhooks. To perform desired operations

------------------------------------------------------------------------------------------------------------------

## API Reference

Okay, let's see how far django-proxypay can help you...
