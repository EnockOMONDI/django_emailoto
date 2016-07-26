from django.conf.urls import patterns, url


urlpatterns = patterns("emailoto.views",
    url(r'^validate/?$', 'validate', name='emailoto-validate')
)
