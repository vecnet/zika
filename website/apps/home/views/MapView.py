# -*- coding: utf-8 -*-
#
# This file is part of the VecNet Zika modeling interface.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/zika
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import csv

import io
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.generic.base import TemplateView

from website.apps.home.models import Data, Simulation


class MapView(TemplateView):
    template_name = "home/map_leaflet.html"

    def get_context_data(self, **kwargs):

        sim_id = kwargs.get('sim_id')
        model_id = kwargs.get('model_id')
        municipality_code = kwargs.get('municipality_code')

        data_items = Data.objects.filter(simulation_id=sim_id).values('date').distinct()

        date_info = []

        for d in data_items:
            date_info.append(str(d['date']))

        date_arg = date_info[-1]

        # Copied from choropleth_map_view
        passjspath = reverse('home.csv_for_map', kwargs={'inquery_date': date_arg, 'sim_id': sim_id})

        all_sim_with_model = Simulation.objects.filter(sim_model__id=model_id)\
            .values('id', 'sim_model', 'date_output_generated', 'name')\
            .exclude(historical=True).order_by('-date_output_generated')

        current_simulation = Simulation.objects.get(id=sim_id, sim_model__id=model_id)

        all_sim_list = []
        for item in all_sim_with_model:
            list_item = item
            date_string = str(item['date_output_generated'].year) + '-' + str(item['date_output_generated'].month) + \
                          '-' + str(item['date_output_generated'].day)
            list_item['date_output_generated'] = date_string
            all_sim_list.append(list_item)

        current_sim_index = 0
        i = 0
        while i < len(all_sim_list):
            if all_sim_list[i]['id'] == current_simulation.id:
                current_sim_index = i
                break
            else:
                i += 1

        if municipality_code:
            municipality_code = municipality_code.zfill(5)
            iframe_src = reverse(
                'simulation.chart',
                kwargs={'simulation_id': current_simulation.id, 'municipality_code': municipality_code})
        else:
            iframe_src = reverse('home.countrytotalchart', kwargs={"simulation_id": current_simulation.id})

        sim_data = Data.objects.filter(simulation_id=sim_id, date=current_simulation.date_output_generated)\
            .values('id', 'location__municipality_code', 'value_mid')

        # Create dictionary with municipality code as key. municipality_code == ID_ESPACIA
        map_data_dict = {}
        for item in sim_data:
            key = item["location__municipality_code"]
            map_data_dict[key] = item

        context = {
            "date_arg": date_arg,
            "all_sim_with_model": all_sim_with_model,  # allows us to use datetime objects
            "current_sim": current_simulation,
            "all_sim_with_model_list": all_sim_list,  # dates are a string for passing into JS function,
            "current_index": current_sim_index,
            "length_all_sim_with_model_list": len(all_sim_list)-1,
            "municipality_code": municipality_code,
            "iframe_src": iframe_src,
            'map_data': map_data_dict
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
