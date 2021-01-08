HISTORY
=======

> Insert new release notes below this line

## 1.2.0 ( 8, Fev, 2021 )

* Checking the status (unpaid, not expired) of the reference before creating

## 1.1.2 ( 26, Oct, 2020 )

* Updating expired reference from reference instance
* Best acknowledge payment on mock payment

## 1.1.1 ( 26, Oct, 2020 )

* added paid_at field on Model Reference 

## 1.1.0 ( 25, Oct, 2020 )

* added is_paid field on Model Reference 
* Upgrade django dependenci to version 3
* Added JSONField on Reference Model to payment and fields (proxypay custom fields)

## 1.0.2 ( 21, May, 2020 )

* Add ``expires_in`` property on ``proxypay.models.Reference`` model

## 1.0.1 ( 11, May, 2020 )

* Just update the docs

## 1.0.0 ( 11, May, 2020 )

* Initial release
* Creating Reference
* Watch payments from Proxypay API Webhooks
* Mock Payment, for development tests
* Admin base management, just listing the references