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

Make the following modifications to your `settings.py` file.

### 1. Add `emailoto` to installed apps:
```
INSTALLED_APPS = [
    ...,
    'emailoto'
]
```

### 2. Configure the authentication backend:
```
AUTHENTICATION_BACKENDS = (
    'emailoto.authentication.EmailOtoAuthBackend',
)
```

### 3. Make sure you have the session middleware installed:
```
MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
]
```

### 4. Add your mailgun keys.

EMAILOTO = {
    'mailgun_api_key': # Your mailgun API key,
    'mailgun_api_url': # The mailgun API url,
    'sender': 'Your Name <you@yourdomain>'
}
```

- `mailgun_api_key` should look something like `key-BlaBLaLbaFakeKey`
- `mailgun_api_url` should look something like `https://api.mailgun.net/v3/soMesecretSauCE.mailgun.org`

### 5. Additionally, you can override default settings in the same `EMAILOTO` dict:
```
EMAILOTO = {
    'redis_host': 'localhost',
    'redis_port': 6379,
    'redis_db': 2,
    'expiration': 60 * 10,
    'mailgun_api_key': # Your mailgun API key,
    'mailgun_api_url': # The mailgun API url,
    'sender': 'Your Name <you@yourdomain>',
    'template': 'yourapp/email_template.html',
    'ratelimit': '10/h',
    'login_redirect': '/'
}
```

## Usage
Once your django application is correctly configured, all you need to do is send
an email to your users when they attempt to log in (it's up to you to determine
how a user logs in - i.e. they input their email in a form, or the input their username
in a form and you read their email from a db, only sending an email if it exists, etc.)


Here is an example of sending an authentication email request after a POST from
a form.

```
from emailoto import email

def my_form(request):
    if request.POST:
        email.send(
            request=request,
            email=request.POST.get('email')
        )
```

When a user clicks on the link in their email, they will be authenticated using
the `EmailOtoAuthBackend` and a django user sessions created for them. You can
close their session by logging the user out as you would log out any django user


```
from django.contrib.auth import logout


def my_logout_view(requsest):
    logout(request)
```
