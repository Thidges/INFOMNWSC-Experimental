"""
This file is meant to analyze and format the output, generated by the biLouvain algorithm.
The communities however are analyzed in analyze_communities.py.
"""
import os
import matplotlib.pyplot as plt

output_files = os.listdir("output")

def string_to_float(string: str) -> float:
    """Used to translate the header string floats back to normal floats."""
    return float(string.replace('p', '.'))

def readout_modularity_file(file_name: str) -> list:
    name_parts = file_name.split('\uf00d')[0].split('Ct')[1].split('Cp')
    iteration_cutoff_value = string_to_float(name_parts[0])
    phase_cutoff_value = string_to_float(name_parts[1])

    modularity_file = open(f"output/{file_name}", encoding="utf-8-sig").read().splitlines()
    modularity_value = float(modularity_file[-1].split(' ')[-1])
    return [iteration_cutoff_value, phase_cutoff_value, modularity_value]

# Reading the modularities
output_data = []
for file_name in output_files:
    if file_name[-21:] == "ResultsModularity.txt":
        output_data.append(readout_modularity_file(file_name))


# TODO: modularity uitlezen

header = ["Iteration cutoff", "Phase cutoff", "Murata+ Modularity", "Willen we hier nog meer?"]


#%% Graphs %%#
print(list(enumerate(header))) # zodat je makkelijk kan zien welke index je nodig hebt


# Given a phase_cutoff, make a line graph with the iteration cutoff on the x-axis, and Murata+ on the y-axis.
def make_line_plot(phase_cutoff: float, line_colour: str) -> None:
    # Filter to keep only the data with given phase cutoff.
    filtered_data = list(filter(lambda item: (item[1] == phase_cutoff), output_data))
    x_data = [item[0] for item in filtered_data]
    y_data = [item[2] for item in filtered_data]

    #x-axis
    plt.xlabel("Iteration cutoff", fontsize = 22)
    plt.xscale("log")
    x_ticks = [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1]
    plt.xticks(x_ticks, fontsize = 20)

    #y-axis
    plt.ylabel("Murata+ modularity", fontsize = 22)
    #y_ticks = [0.590, 0.595, 0.600, 0.605, 0.610, 0.615, 0.620]
    plt.yticks(fontsize = 22)

    plt.title("Murata+ modularity per iteration cutoff, for two constant phase cutoff values")
    plt.gcf().set_dpi(300)
    line_label = f"Phase cutoff: {phase_cutoff}"
    # Larger text font
    plt.rc('font', size=22)
    plt.plot(x_data, y_data, line_colour, label = line_label)


# Graph 1: phase cutoff = 0.0
make_line_plot(0.0, "blue")
# Graph 2: phase cutoff = 0.001
make_line_plot(0.001, "red")
plt.legend(loc = 'best')
plt.grid(alpha=0.5)
plt.show()

#%% LaTeX Table %%#
table_name = "output/table_LaTeX.txt"
if os.path.exists(table_name):
    os.remove(table_name)

table = open(table_name, "a")
table.write("\\begin{tabular}{ c c c }\n")
table.write("\\hline\n")
# header
table.write("Iteration cutoff & Phase cutoff & Murata+ modularity \\\\\n")
table.write("\\hline\n")
#body
# foreach scenario
for line in output_data:
    table.write(f"{line[0]} & {line[1]} & {line[2]}  \\\\\n")
    #table.write("\\hline\n")

table.write("\\hline\n")
table.write("\\end{tabular}\n")
table.close()
