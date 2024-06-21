"""
Used for identifying the communities from one of the output files and generating the statistical analysis values.
"""
import ast
import os
import requests
import numpy as np
import sklearn.metrics as sk

# File with the highest modularity
file_name = 'output/ResultsCt0p01Cp0p0\uf00d_ResultsCommunities.txt'
community_file = open(file_name, encoding="utf-8-sig").read().splitlines()


# helper functions
def get_family_name(genus):
    url = f"https://api.gbif.org/v1/species?name={genus}"
    response = requests.get(url)
    data = response.json()

    if data['results']:
        for result in data['results']:
            if 'family' in result:
                return result['family']

    return None

def contains(list: list, item: any) -> bool:
    """If the 'list' contains at least one element equal to 'item', return True."""
    for li in list:
        if li == item:
            return True
    return False


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

#%% create dictionary -> done only once, so the API won't be overloaded by our requests,
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

else: # otherwise just read in the dictionary, what should normally happen
    dict_string = open(genus_name).read()
    dictionary_genus_family = dict(ast.literal_eval(dict_string))

# make a copy of the communities, replace all plants with the families for comparing
community_list_families = community_list.copy()
for c_index in range(len(community_list_families)):
    for p_index in range(len(community_list_families[c_index])):
        genus = community_list_families[c_index][p_index].split(' ')[0]
        community_list_families[c_index][p_index] = dictionary_genus_family.get(genus)


# Comparing of the plant families
all_families_set = set()
for _, family in dictionary_genus_family.items():
    all_families_set.add(family)

print("Amount of families in the dataset:", len(all_families_set))

#%% for remembering the most dominant community for each family
count_community_nr_dict = dict()
for family in all_families_set:
    count_community_nr_dict.update({family: (0, -1)})

for index, community in enumerate(community_list_families):
    count_community_families = dict()

    # count how many times each family is presented in this community
    for family in community:
        family_value = count_community_families.get(family)
        if family_value == None:
            count_community_families.update({family: 1})
        else:
            count_community_families.update({family: family_value + 1})

    # for each family, check if this community has more family members than before
    for family, amount in count_community_families.items():
        old_count, _ = count_community_nr_dict.get(family)
        if old_count < amount:
            count_community_nr_dict.update({family: (amount, index)})

#%% for each community, write down what the dominant families they have
community_dominant_families = []
for _ in range(len(community_list_families)):
    community_dominant_families.append([])

for family, (_, community_nr) in count_community_nr_dict.items():
    community_dominant_families[community_nr].append(family)

#%% Counting for the confusion matrix
def flatten_list_of_lists(xss):
    return [x for xs in xss for x in xs]

y_pred = []
y_true = []
for index, community in enumerate(community_list_families):
    for member in community:
        y_pred.append(index)
        _, actual = count_community_nr_dict.get(member)
        y_true.append(actual)

accuracy = sk.accuracy_score(y_true, y_pred)
precision = sk.precision_score(y_true, y_pred, average='macro')
recall = sk.recall_score(y_true, y_pred, average='macro')
f1_score = sk.f1_score(y_true, y_pred, average='macro')

print("Accuracy:", accuracy)
print("Macro Precision:", precision)
print("Macro Recall:", recall)
print("Macro F1_score:", f1_score)

accuracy = sk.accuracy_score(y_true, y_pred)
precision = sk.precision_score(y_true, y_pred, average='weighted')
recall = sk.recall_score(y_true, y_pred, average='weighted')
f1_score = sk.f1_score(y_true, y_pred, average='weighted')

print("Accuracy:", accuracy)
print("Average Precision:", precision)
print("Average Recall:", recall)
print("Average F1_score:", f1_score)

#%% For checking the community sizes %%#
count_list = np.sort(np.array([len(com) for com in community_list_families]))[::-1]
print("Community sizes:", count_list)
print("Average community size:", sum(count_list) / len(count_list))
print("Amount of communities:", len(count_list))
