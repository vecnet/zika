# FUNCTIONS TO TEST
# class Utils(TestCase):
#     # import fixtures
#     fixtures = ['simulation_data.json']
#
#     # Test that load simulation file passes with both parameters
#     def test_load_simulation_file_pass(self):
#         myfile = io.StringIO('name,output_generate_date,value_mid,value_high,disease,model_name,department, municipality_code,municipality,department_code,date,value_low,id,population')
#         simulation_name = 'test simulation'
#
#         load_simulation_file(myfile, simulation_name)
#
#         simulation = Simulation.objects.filter(name=simulation_name)
#
#         self.assertEqual(simulation.count(), 1)
#         self.assertEqual(simulation[0].name, 'test simulation')
#
#     # Test if simulation name is None
#     def test_load_simulation_file_fail_none_sim_name(self):
#         myfile = io.StringIO('name,output_generate_date,value_mid,value_high,disease,model_name,department,municipality_code,municipality,department_code,date,value_low,id,population')
#         simulation_name = None
#
#         self.assertRaises(TypeError, load_simulation_file, (myfile, simulation_name))
#
#     # Test if no simulation name provided
#     def test_load_simulation_file_fail_no_sim_name(self):
#         myfile = io.StringIO(
#             'name,output_generate_date,value_mid,value_high,disease,model_name,department,municipality_code,municipality,department_code,date,value_low,id,population')
#
#         self.assertRaises(TypeError, load_simulation_file, myfile)
#
#     # Test if file is None
#     def test_load_simulation_file_fail_none_file(self):
#         myfile = None
#         simulation_name = "test 4"
#
#         self.assertRaises(TypeError, load_simulation_file, (myfile, simulation_name))
#
#     # Test if no file provided
#     def test_load_simulation_file_fail_no_file(self):
#         simulation_name = "test 4"
#
#         self.assertRaises(TypeError, load_simulation_file, simulation_name)
