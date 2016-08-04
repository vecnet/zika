from django.conf.urls import url
from website.apps.home.views import load_locations
from website.apps.home.views import testview

urlpatterns = [
    url(r'^$', testview),
    url(r'^(?P<department_name>[A-Z, a-z, _]+)/$', load_locations),
]