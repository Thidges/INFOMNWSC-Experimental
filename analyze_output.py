"""
This file is meant to analyze the output, generated by the biLouvain algorithm.
"""
import os

output_files = os.listdir("output")

for file_name in output_files:
    if file_name[-21:] == "ResultsModularity.txt":
        "ResultsCt0p0001Cp0p001_ResultsModularity.txt"

# TODO: modularity uitlezen

header = ["Iteration cutoff", "Phase cutoff", "Murata+ Modularity", "Willen we hier nog meer?"]
output_data = [[0.01, 0.0, 0.4555, "iets ofzo"], [0.01, 0.001, 0.3955, "iets ofzo"], [0.025, 0.0, 0.5842, "iets ofzo"],
               [0.025, 0.001, 0.4842, "iets ofzo"]] # Iedere index in output_data heeft de informatie van de header, nu met mock data


#%% Graphs %%#
print(list(enumerate(header))) # zodat je makkelijk kan zien welke index je nodig hebt


#%% LaTeX Table %%#

