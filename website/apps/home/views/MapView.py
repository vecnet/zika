from django.template import loader
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from website.apps.simulation.models import Data


class MapView(TemplateView):
    template_name = "home/map.html"

    def get_context_data(self, **kwargs):

        sim_id = kwargs.get('sim_id')

        info = Data.objects.filter(location__municipality_code='05001', simulation_id=sim_id).values('date')

        date_info = []

        for d in info:
            date_info.append(str(d['date']))

        date_arg = None
        if (kwargs.get('inquery_date')):
            date_arg = kwargs.get('inquery_date')
        else:
            date_arg = date_info[-1]

        # Coped from choropleth_map_view
        passjspath = reverse('home.csv_for_map', kwargs={"inquery_date": date_arg, "sim_id": sim_id})
        #template = loader.get_template('home/choropleth_map.html')
        # context = {'generatefilepath': passjspath, 'inquery_date': date_arg, 'sim_id': sim_id}

        context = {
            "date_arg": date_arg,
            "date_list": date_info,
            "sim_id": sim_id,
            'generatefilepath': passjspath
        }
        return context

