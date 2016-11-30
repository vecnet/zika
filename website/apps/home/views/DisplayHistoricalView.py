from django.http.response import HttpResponse
from django.template import loader

from website.apps.home.models import Simulation


# View for the table of historical data
def display_historical(request):

    # Get all the simulations
    all_historical = Simulation.objects.exclude(historical=False)

    historical_list = []

    # For each simulation in all_simulations
    for entry in all_historical:
        sim = {
            'simulation_id': str(entry.id),
            'simulation_name': entry.name,
            'model_name': entry.model_name,
            'create_time': entry.creation_timestamp
        }

        # Add this simulation entry to the list
        historical_list.append(sim)

    template = loader.get_template('home/historical.html')
    context = {
        'historical_list': historical_list
    }

    return HttpResponse(template.render(context, request))
