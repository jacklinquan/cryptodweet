# cryptodweet
[![PyPI version](https://badge.fury.io/py/cryptodweet.svg)](https://badge.fury.io/py/cryptodweet) [![Downloads](https://pepy.tech/badge/cryptodweet)](https://pepy.tech/project/cryptodweet)

A simple python package for the free dweet service with encryption.

Dweet is a simple machine-to-machine (M2M) service from https://dweet.io/ .
The free service is public and any data is accessible by anyone.
This package adds encryption to it and make it a bit more secure.
Only the minimal APIs are supported.
Only bytes and str types are supported.

Please consider [![Paypal Donate](https://github.com/jacklinquan/images/blob/master/paypal_donate_button_200x80.png)](https://www.paypal.me/jacklinquan) to support me.

## Installation
`pip install cryptodweet`

## Usage
```
>>> from cryptodweet import CryptoDweet
>>> cd = CryptoDweet('YOUR KEY')
>>> cd.dweet_for('YOUR THING', {'YOUR DATA': 'YOUR VALUE'})
{u'content': {u'8c94428bc640de621c7c3ceea1d00b96': u'05d6f2dbc1ce3afa7e6072c0c4
c6f6a7'}, u'thing': u'9ee9b47833d5a13043c5f47e8802596a', u'transaction': u'd45a
1e08-fc5c-49b6-a9c5-7ee87713c059', u'created': u'2019-02-10T21:59:34.270Z'}
>>> cd.get_latest_dweet_for('YOUR THING')
[{u'content': {u'YOUR DATA': u'YOUR VALUE'}, u'thing': u'YOUR THING', u'created
': u'2019-02-10T21:59:34.270Z'}]
```
