from django.conf.urls import url
from website.apps.home.views import load_locations
from website.apps.home.views import testview
from website.apps.home.views import testmap

urlpatterns = [
    url(r'^$', testview),
    url(r'^test/$', testmap),
    url(r'^(?P<department_name>[A-Z, a-z, _]+)/$', load_locations),

]