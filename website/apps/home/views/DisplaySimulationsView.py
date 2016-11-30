from django.http.response import HttpResponse
from django.template import loader

from website.apps.home.models import Simulation


# View for the table of simulations and models (at /home url)
def display_simulations(request):

    # Get all the simulations
    all_simulations = Simulation.objects.exclude(historical=True)

    sim_list = []

    # For each simulation in all_simulations
    for entry in all_simulations:
        sim = {
            'simulation_id': str(entry.id),
            'simulation_name': entry.name,
            'model_name': entry.model_name,
            'create_time': entry.creation_timestamp
        }

        # Add this simulation entry to the list
        sim_list.append(sim)

    template = loader.get_template('home/simulation.html')
    context = {
        'simulation_model_list': sim_list,
        'nbar': 'display_simulations'
    }

    return HttpResponse(template.render(context, request))
