"""
This file is meant to make the original network graph, into one that we can use for biLouvain.
"""
import os

#%% Delete, create and open the input files %%#
pollinator_edges_name = "input/pollinator_edges.txt"
if os.path.exists(pollinator_edges_name):
    os.remove(pollinator_edges_name)

edge_file = open(pollinator_edges_name, "a")
data = open("input/CPC_PollinatorDatabase_Result_2024-05-28.csv", encoding="utf-8-sig").read().splitlines()


#%% Helper functions %%#
def contains(list: list, item: any) -> bool:
    """If the 'list' contains at least one element equal to 'item', return True."""
    for li in list:
        if li == item:
            return True
    return False


def remove_optional_quotes(word: str) -> str:
    """If the element 'word' begins with a quote(\"), delete that one and the last character (which should also be a quote) """
    if word[0] == '"':
        return word[1:-1]
    return word


#%% Generating of all the pollinator edges %%#
# Header information:
# [(0, 'pollinator_name'), (1, 'pollinator_scientific'), (2, 'plant_name'), (3, 'plant_scientific'), (4, 'association_type'),
# (5, 'reference_link'), (6, 'reference'), (7, 'source_type'), (8, 'reference_text'), (9, 'pollinator_group')]
# The assiciation types:
# ['"Floral Visitor"', '"Suspected Pollinator Floral"', '"Confirmed Pollinator"', '"Pollen Robber"', '', '"Nectar Robber"']
edge_set = set()
pollinator_set = set()
plant_set = set()
invalid = 0
refused = 0
not_a_plant = 0
for line in data[1:]:
    line_parts = line.split(',')
    # if the line is invalid
    if len(line_parts) < 5 or line_parts[1] == "" or line_parts[3] == "" or line_parts[4] == "":
        invalid += 1
        continue
    # if the insect is of the right type for the plant
    if not contains(['"Confirmed Pollinator"', '"Pollen Robber"', '"Nectar Robber"'], line_parts[4]):
        refused += 1
        continue
    # if the plant does not exist out of (at least) 2 words
    if not contains(line_parts[3], " "):
        not_a_plant += 1
        continue

    # format the names
    pollinator_sci = remove_optional_quotes(line_parts[1])
    plant_sci = remove_optional_quotes(line_parts[3])
    edge_name = f"{pollinator_sci},{plant_sci}"

    # add to the sets
    edge_set.add(edge_name)
    pollinator_set.add(pollinator_sci)
    plant_set.add(plant_sci)

# write to the input file "pollinator_edges.txt"
for edge_line in edge_set:
    edge_file.write(edge_line + "\n")

# Print some general stats/information
print("Amount of edges:", len(edge_set))
print("Amount of pollinators:", len(pollinator_set))
print("Amount of plants:", len(plant_set))
print("Invalid lines:", invalid)
print("Refused Visitor:", refused)
print("Invalid sci plant name:", not_a_plant)
