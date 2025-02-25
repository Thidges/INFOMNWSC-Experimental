"""
This file is used for making a .sh (bash) file that runs the algorithm several times (all the testcases).
"""
import os

#%% Some constants  %%#
commands_file_name = "execute_all_cases.sh"
input_file_name = "pollinator_edges.txt"
all_cutoff_iterations = [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1]
all_cutoff_phases = [0.0, 0.001]


#%% The functions needed for making the bash file %%#
def float_to_string(number: float) -> str:
    return str(number).replace('.', 'p')


def generate_commandline(inputFileName: str, cutoff_iteration: float = 0.01, cutoff_phase: float = 0.0) -> str:
    test_prefix = "Test" if inputFileName == "test.txt" else ""
    return (
                f"./biLouvain/src/biLouvain -i input/{inputFileName} -d \",\" -ci {cutoff_iteration} -cp {cutoff_phase} -o " +
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
