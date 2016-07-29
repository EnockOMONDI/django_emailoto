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

```
pip install git+git://github.com/qdonnellan/django_emailoto.git@master
```

## Configuration

As a bare-minimum, just provide emailoto with your MailGun API information
in your django project's `settings.py` file.

```
EMAILOTO = {
    'mailgun_api_key': # Your mailgun API key,
    'mailgun_api_url': # The mailgun API url,
    'sender': 'Your Name <you@yourdomain>'
}
```

- `mailgun_api_key` should look something like `key-BlaBLaLbaFakeKey`
- `mailgun_api_url` should look something like `https://api.mailgun.net/v3/soMesecretSauCE.mailgun.org`

Additionally, you can override default settings in the same `EMAILOTO` dict:

```
EMAILOTO = {
    'redis_host': 'localhost',
    'redis_port': 6379,
    'redis_db': 2,
    'expiration': 1,
    'mailgun_api_key': # Your mailgun API key,
    'mailgun_api_url': # The mailgun API url,
    'sender': 'Your Name <you@yourdomain>',
    'template': 'yourapp/email_template.html',
    'ratelimit': '10/h'
}
```