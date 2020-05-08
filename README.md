django-proxypay
=================

Django Proxypay is a [Django Framework](https://www.djangoproject.com/) application/library that facilitates the integration of your Django project with the [Proxypay](https://proxypay.co.ao/) [API](https://developer.proxypay.co.ao/v2/). Allowing to generate referrals, recognize payments and look through Proxypay's webhooks

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

At the moment the Django Proxypay is in development and outside [Pypi](https://pypi.org/). But soon you will be able to install it simply and practice using the ``pip``:

    pip install django-proxypay

#### Requirements

* Python ``3.7; 3.8``
* Django ``2.2; 3.0``
* requests ``2.23``

these are the officially supported python and package versions. Other versions will probably work

## Configurations

As stated above, Django Proxypay is a Django Application. To configure your project you simply need to add ``proxypay`` in the installed applications and configure the ``PROXYPAY`` variable in the ``settings.py`` file

Like the example below, file ``settings.py``:

```python

# Your project applications
INSTALLED_APPS = [
    'proxypay',
]

# Proxypay Configurations
PROXYPAY = {
    # (str) Your Proxypay authorization token key
    'PRIVATE_KEY': os.environ.get('PROXYPAY_PRIVATE_KEY'),
    # (int) Your Proxypay Entity ID
    'ENTITY': os.environ.get('PROXYPAY_ENTITY'),
    # (int) Optional, Default days to expire a reference
    'REFERENCE_DAYS': os.environ.get('PROXYPAY_REFERENCE_DAYS'),
    # (str) Optional, the proxypay api environment to use
    # If not set, by default Proxypay will use the sandbox environment if settings.DEBUG is True 
    # and produnction if is False
    # If set, the value must be sandbox or production
    'ENV': os.environ.get('PROXYPAY_ENV')
}

```

**Note**: That's all, make sure to run the database migrations. Using the commands ``python manage.py makemigrations`` and ``python manage.py migrate`` to generate a table of References in the database

## Base Usage

Use the `` proxypay.references.create`` method to create new references. This method will return an instance of `` proxypay.models.Reference``

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
        'product_type': 'some'
    },
    # (int) Optional, Number of days to expire the reference
    days=3,
)

# Check if a reference was paid / Acknowledge Payment for this reference
# will return False or the payment data from Proxypay API in a dict structure
payment = reference.check_payment() 

```

## Mock Payment

In development mode, you can create fictitious payments to test your application. Using Django's ``manage.py`` in your terminal like below:

```bash

# 123902092 a reference id
python manage.py proxypay pay 123902092

```

This command will search for the reference in the database, if found and has not yet been paid, it will make the payment. This time, the signal will be triggered, and you will be able to simulate it as if the payment confirmation came from Proxypay's Webhooks. To perform desired operations

------------------------------------------------------------------------------------------------------------------

## API Reference

Okay, let's see how far django-proxypay can help you...
