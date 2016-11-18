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

        context = {
            "date_list": date_info,
            "sim_id": sim_id
        }
        return context

