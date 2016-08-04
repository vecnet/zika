from django.conf.urls import url
from website.apps.home.views import load_locations

urlpatterns = [
    url(r'^wiki/(?P<department_name>[A-Z, a-z, -]+)/$', load_locations),
]