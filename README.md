# django_emailoto

Django authentication via one-time-only emailed tokens. 

## License
The MIT License (MIT)
Copyright (c) 2016 Quentin Donnellan

See LICENSE file for full license.

## Pre-requisites
`django_emailoto` uses [Redis](http://redis.io/) to store authentication tokens and [MailGun](http://www.mailgun.com/) to send
those tokens to your users. You need to make sure you have Redis running on the
same machine as your django project, and you need to have a valid MailGun account.

## Installation

'''
pip install git+git://github.com/qdonnellan/django_emailoto.git@master
'''

## Configuration

