import csv
import io

from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.generic.base import TemplateView

from website.apps.home.models import Data


class MapView(TemplateView):
    template_name = "home/map.html"

    def get_context_data(self, **kwargs):

        sim_id = kwargs.get('sim_id')

        info = Data.objects.filter(location__municipality_code='05001', simulation_id=sim_id).values('date')

        date_info = []

        for d in info:
            date_info.append(str(d['date']))

        date_arg = None

        if kwargs.get('inquery_date'):
            date_arg = kwargs.get('inquery_date')
        else:
            date_arg = date_info[-1]

        # Copied from choropleth_map_view
        passjspath = reverse('home.csv_for_map', kwargs={"inquery_date": date_arg, "sim_id": sim_id})

        print(passjspath)
        context = {
            "date_arg": date_arg,
            "date_list": date_info,
            "sim_id": sim_id,
            'generatefilepath': passjspath
        }
        return context


def csv_for_map_view(request, inquery_date, sim_id):
    allinfo = Data.objects.filter(date=inquery_date, simulation_id=sim_id)
    if not allinfo:
        return HttpResponseBadRequest()
    else:
        output = io.StringIO()

        tricky_codes = ['05001', '05002', '05004', '05021', '05030', '05031', '05034', '05036', '05038', '05040', '05042',
                        '05044',
                        '05045', '05051', '05055', '05059', '05079', '05086', '05088', '05091', '05093', '05101', '05107',
                        '05113',
                        '05120', '05125', '05129', '05134', '05138', '05142', '05145', '05147', '05148', '05150', '05154',
                        '05172',
                        '05190', '05197', '05206', '05209', '05212', '05234', '05237', '05240', '05250', '05264', '05266',
                        '05282',
                        '05284', '05306', '05308', '05310', '05313', '05315', '05318', '05321', '05347', '05353', '05360',
                        '05361',
                        '05364', '05368', '05376', '05380', '05390', '05400', '05411', '05425', '05440', '05467', '05475',
                        '05480',
                        '05483', '05490', '05495', '05501', '05541', '05543', '05576', '05579', '05585', '05591', '05604',
                        '05607',
                        '05615', '05628', '05631', '05642', '05647', '05649', '05652', '05656', '05658', '05659', '05660',
                        '05664',
                        '05665', '05667', '05670', '05674', '05679', '05686', '05690', '05697', '05736', '05756', '05761',
                        '05789',
                        '05790', '05792', '05809', '05819', '05837', '05842', '05847', '05854', '05856', '05858', '05861',
                        '05873',
                        '05885', '05887', '05890', '05893', '05895', '08001', '08078', '08137', '08141', '08296', '08372',
                        '08421',
                        '08433', '08436', '08520', '08549', '08558', '08560', '08573', '08606', '08634', '08638', '08675',
                        '08685',
                        '08758', '08770', '08832', '08849']

        writer = csv.writer(output)
        writer.writerow(['ID_ESPACIA', 'value'])
        for data_point in allinfo:
            if data_point.location.municipality_code in tricky_codes:
                data_point.location.municipality_code = data_point.location.municipality_code[1:]
                writer.writerow([data_point.location.municipality_code, data_point.value_mid])
            else:
                writer.writerow([data_point.location.municipality_code, data_point.value_mid])

        return HttpResponse(output.getvalue())
