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
            'create_time': entry.creation_timestamp,
            'generated_date': entry.date_output_generated,
            'is_uploaded': entry.is_uploaded
        }

        if entry.sim_model is not None:
            sim['simulation_model'] = entry.sim_model

        # Add this simulation entry to the list
        sim_list.append(sim)

    template = loader.get_template('home/simulation.html')
    context = {
        'simulation_model_list': sim_list,
        'nbar': 'display_simulations'
    }

    return HttpResponse(template.render(context, request))
