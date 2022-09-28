import random
from main import Building, Town, Street
from datetime import datetime
import copy

last_random_num = -1

town_names = [
    "Muddier Town", "Muddiest Town",
    "New Muddy Town", "Extra Mini Town",
    "Springfield", "South Park", "Quahog",
    "Denver", "Scranton"
]

building_names = [
    "North", "North West",
    "West", "South", "South West",
    "South East", "East", "North East"
]

street_names = [
    "St.", "Ave.", "Boul.", "Ln."
]


# For Testing purposes
def print_town_test(town):
    print(f"{town.name}")
    print(f"Number of Buildings: {len(town.buildings)}")
    print(f"Example Building: {town.buildings[1].address}")
    print(f"Number of Streets: {len(town.streets)}")
    print(f"Example Street: [{town.streets[1].paving_cost}, \"{town.streets[1].src.address}\", \"{town.streets[1].dest.address}\"]")


def create_buildings(town, num_buildings):
    building_list = []
    for i in range(num_buildings):
        building = Building(str(random.randint(1000, 9999)) + " " + random.choice(building_names) + " " + random.choice(street_names))
        building_list.append(building)

        town.add_building(building)

    return building_list


def create_connected_town(num_buildings, num_streets):
    min_buildings = 2
    min_num_streets = num_buildings - 1
    max_num_streets = (num_buildings * (num_buildings - 1)) / 2

    if num_buildings < min_buildings or num_streets < min_num_streets or num_streets > max_num_streets:
        raise Exception("Error, invalid number of buildings or streets")

    town = Town(random.choice(town_names))

    building_list = create_buildings(town, num_buildings)
    all_buildings = {}

    for i in range(0, len(building_list)-1):
        all_buildings[building_list[i].address] = i
    town.buildings = []

    # Set up our first building
    current_building_index = get_pseudorandom_number(num_buildings)
    current_building = building_list[current_building_index]
    current_building.index = len(town.buildings)
    town.add_building(current_building)

    current_building.non_neighbors = copy.deepcopy(all_buildings)
    building_list.pop(current_building_index)

    try:
        del current_building.non_neighbors[current_building.address]
    except:
        pass

    num_buildings -= 1

    build_neighbors(
        town,
        current_building,
        num_buildings,
        num_streets,
        building_list,
        all_buildings
    )

    # for cases when number of streets is > min
    connect_streets(town, num_streets)

    return town


def build_neighbors(town, current_building, num_buildings, num_streets, building_list, all_buildings):
    # establishing connectivity
    while num_buildings > 0:
        # Build a neighbor
        neighbor_building_index = get_pseudorandom_number(num_buildings)
        neighbor_building = building_list[neighbor_building_index]
        # Remove current and neighbor from each other's non_neighbor set
        neighbor_building.non_neighbors = copy.deepcopy(all_buildings)

        try:
            del neighbor_building.non_neighbors[current_building.address]
        except:
            pass
        try:
            del current_building.non_neighbors[neighbor_building.address]
        except:
            pass

        neighbor_building.index = len(town.buildings)
        town.add_building(neighbor_building)
        town.building_index_dict[neighbor_building.address] = neighbor_building.index

        building_list.pop(neighbor_building_index)

        street = Street(get_pseudorandom_number(20) + 1)
        street.buildings = [current_building, neighbor_building]

        current_building.streets.append(street)
        neighbor_building.streets.append(street)
        town.add_street(street)

        num_streets -= 1
        num_buildings -= 1

        current_building = neighbor_building

    return current_building


def connect_streets(town, num_streets):
    while num_streets > 0:
        current_building_index = get_pseudorandom_number(len(town.buildings))

        # if the current building is already connected to every other building, try again
        if len(town.buildings[current_building_index].non_neighbors) == 0:
            continue

        # current building = a random building with disconnected immediate neighbors
        current_building = town.buildings[current_building_index]
        # neighbor building = a random building among those not yet connected buildings
        neighbor_building = town.get_building(random.choice(tuple(current_building.non_neighbors)))

        try:
            del neighbor_building.non_neighbors[current_building.address]
        except:
            pass
        try:
            del current_building.non_neighbors[neighbor_building.address]
        except:
            pass

        street = Street(get_pseudorandom_number(20) + 1)
        street.buildings = [current_building, neighbor_building]

        current_building.streets.append(street)
        neighbor_building.streets.append(street)
        town.streets.append(street)
        num_streets -= 1


def get_pseudorandom_number(max_number):
    global last_random_num
    if last_random_num == -1:
        last_random_num = (datetime.now().timestamp())
    last_random_num = (25214903918 * last_random_num + 11) % ((2**48) + 1)

    return int(last_random_num+0.5) % max_number
