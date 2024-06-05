"""
This file is meant for making a .cmd file that let's the algorithm several times.
"""
import os

def generate_commandline(inputFileName: str, cutoff_iterations: float = 0.01, cutoff_phases: float = 0.0):
    return f"./biLouvain -i {inputFileName}, id \",\" -ci {cutoff_iterations} -cp {cutoff_phases}"

