"""
This file is for analyzing the communities from one of the testcases.
"""

file_name = 'output/ResultsCt0p0001Cp0p001\uf00d_ResultsCommunities.txt'
community_file = open(file_name, encoding="utf-8-sig").read().splitlines()

community_list = []

# skip all the pollinator communities, we're not interested in those
index = 0
while community_file[index].split(":")[0][-2] == "1":
    index += 1

# while the plant communities are selected
while community_file != "":

