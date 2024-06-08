"""
This file is meant for making a .cmd file that let's the algorithm several times.
"""
import os

#%% Some constants  %%#
commands_file_name = "execute_all_cases.sh"
input_file_name = "pollinator_edges.txt"
all_cutoff_iterations = [0.0001, 0.001, 0.01, 0.03]
all_cutoff_phases = [0.0, 0.001]

#%% The functions needed for making the bash file %%#
def float_to_string(number: float):
    return str(number).replace('.', 'p')

def generate_commandline(inputFileName: str, cutoff_iteration: float = 0.01, cutoff_phase: float = 0.0):
    test_prefix = "Test" if inputFileName == "test.txt" else ""
    return (f"./biLouvain/src/biLouvain -i input/{inputFileName} -d \",\" -ci {cutoff_iteration} -cp {cutoff_phase} -o " +
            f" output/{test_prefix}ResultsCt{float_to_string(cutoff_iteration)}Cp{float_to_string(cutoff_phase)}")

#%% The deleting of the old bash file and writing all of the command lines %%#
if os.path.exists(commands_file_name):
    os.remove(commands_file_name)

commands_file = open(commands_file_name, "a")

# Looping over all the parameters
for cutoff_iteration in all_cutoff_iterations:
    for cutoff_phase in all_cutoff_phases:
        commands_file.write(generate_commandline(input_file_name, cutoff_iteration, cutoff_phase) + "\n")

commands_file.close()
