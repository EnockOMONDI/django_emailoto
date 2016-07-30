from django.conf.urls import patterns, url


urlpatterns = patterns("emailoto.views",
    url(r'^$', 'validate', name='emailoto-validate')
)
