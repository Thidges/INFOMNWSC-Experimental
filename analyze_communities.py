"""
This file is for analyzing the communities from one of the testcases.
"""
import ast
import os
import requests

# File with the highest modularity
file_name = 'output/ResultsCt0p01Cp0p0\uf00d_ResultsCommunities.txt'
community_file = open(file_name, encoding="utf-8-sig").read().splitlines()

# helper function
def get_family_name(genus):
    url = f"https://api.gbif.org/v1/species?name={genus}"
    response = requests.get(url)
    data = response.json()

    if data['results']:
        for result in data['results']:
            if 'family' in result:
                return result['family']

    return None

community_list = []

# skip all the pollinator communities, we're not interested in those
index = 0
while community_file[index].split(":")[0][-2] == "1":
    index += 1

community = []
# while the plant communities are selected
while community_file[index] != "":
    line = []
    if community_file[index][:9] == "Community":
        if len(community) > 0:
            community_list.append(community)
        community = []
        line = community_file[index].split(':')[1][1:].split(',')
    else:
        line = community_file[index][1:].split(',')
    for plant in line:
        community.append(plant)
    index += 1

# create dictionary -> done only once, so the API won't be overloaded by our requests,
all_genera = set()
for community in community_list:
    for plant in community:
        genus = plant.split(' ')[0]
        all_genera.add(genus)


dictionary_genus_family = dict()
genus_name = "analyzed_results/genus_dictionary.txt"

# If false, there will be done a lot of requests to an API
dictionary_already_created = True
if not dictionary_already_created:
    for genus in all_genera:
        family_name = get_family_name(genus)
        dictionary_genus_family.update({genus: family_name})

    if os.path.exists(genus_name):
        os.remove(genus_name)
    genus_file = open(genus_name, "a")
    genus_file.write(str(list(dictionary_genus_family.items())))
    genus_file.close()

else:
    dict_string = open(genus_name).read()
    dictionary_genus_family = dict(ast.literal_eval(dict_string))

community_list_families = community_list.copy()
for c_index in range(len(community_list_families)):
    for p_index in range(len(community_list_families[c_index])):
        genus = community_list_families[c_index][p_index].split(' ')[0]
        community_list_families[c_index][p_index] = dictionary_genus_family.get(genus)


# TODO Comparing of the plant families
