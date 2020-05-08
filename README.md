django-proxypay
=================

Django Proxypay is a [Django Framework](https://www.djangoproject.com/) application/library that facilitates the integration of your Django project with the [Proxypay](https://proxypay.co.ao/) [API](https://developer.proxypay.co.ao/v2/). Allowing to generate referrals, recognize payments and look through Proxypay's webhooks

----------------------------------------------------------------------------------

### Some Features

The Django Proxypay really comes to falicilar the integration to the Proxypay API, leaving all interaction with Proxypay totally out of the box. Letting you focus more on data validation and / or the Frontend

* Generate references and store them in the database
* Verify payment directly from a reference instance
* Acknowledge payment
* Recognize payments automatically using Proxypay webhooks
* Mock Payment, for development tests
* Of course, Signals, notifying you when a payment is recognized or a reference is created or updated.

---------------------------------------------------------------------------

## Installation

At the moment the Django Proxybay is in development and **outside** [Pypi](https://pypi.org/). But soon you will be able to install it simply and practice using the ``pip``:

    pip install django-proxypay

#### Requirements

* Python ``3.7; 3.8``
* Django ``2.2; 3.0``
* requests ``2.23``

hese are the officially supported python and package versions.  Other versions
will probably work

## Configuations

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
    'REFERENCE_DAYS': os.environ.get('PROXYPAY_REFERENCE_DAYS')
}

```

**Note**: That's all, make sure to run the database migrations. Using the commands ``python manage.py makemigrations`` and ``python manage.py migrate``

## Base Usage

