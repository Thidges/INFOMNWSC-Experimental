"""
This file is meant for making a .cmd file that let's the algorithm several times.
"""
import os

def float_to_string(number: float):
    return str(number).replace('.', 'p')

def generate_commandline(inputFileName: str, cutoff_iterations: float = 0.01, cutoff_phases: float = 0.0):
    return (f"./biLouvain/src/biLouvain -i input/{inputFileName} -d \",\" -ci {cutoff_iterations} -cp {cutoff_phases} -o " +
            f" output/ResultsCt{float_to_string(cutoff_iterations)}Cp{float_to_string(cutoff_phases)}")

print(generate_commandline("test.txt"))
