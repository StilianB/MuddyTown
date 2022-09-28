from queue import Queue


class PavingPlan:

    def __init__(self, town):
        self.name = ''
        self.paved_streets = []
        self.total_cost = 0
        self.minimum_cost = 0
        self.buildings = []
        self.town = town

        self.building_index_dict = {}

    def add_street(self, street):
        self.paved_streets.append(street)

    def add_building(self, building):
        self.buildings.append(building)
        index = len(self.buildings) - 1
        self.add_building_to_index_dict(building.address, index)

    def add_building_to_index_dict(self, address, index):
        self.building_index_dict[address] = index

    def get_building_index(self, address):
        try:
            return self.building_index_dict[address]
        except:
            return None

    def get_building(self, address):
        try:
            building_index = self.get_building_index(address)
            return self.buildings[building_index]
        except:
            return None

    def get_or_create_building(self, address):
        building = self.get_building(address)
        if building is None:
            building = Building(address, len(self.buildings))
            self.add_building(building)

        return building

    def print_paving_plan(self):
        print(f"Name: {self.name} Total Cost: {self.total_cost}")
        for street in self.paved_streets:
            print(street)

    def write_paving_plan(self, filepath):
        w = open(filepath, 'w')
        w.write(f"{self.name}\n")
        # Removing brackets and single quotes
        for street in self.paved_streets:
            x, y = str(street).split(",")
            x = x.replace('[', '').replace('\'', '').replace(']', '')
            y = y.replace('[', '').replace('\'', '').replace(']', '')
            w.write(f"{x},{y.lstrip()}\n")

    def read_paving_plan(self, filepath):
        with open(filepath) as f:
            lines = f.readlines()
            self.name = lines[0].strip('\n')
            self.paved_streets = lines[1:len(lines)]
            self.buildings = self.get_buildings

    def find_total_cost(self, town):
        self.total_cost = 0
        for paved_street in self.paved_streets:
            for street in town.streets:
                src_address, dest_address = str(paved_street).split(",")
                if (street.buildings[0].address == src_address) and (street.buildings[1].address == dest_address.lstrip()):
                    self.total_cost += int(street.paving_cost)
        return self.total_cost

    def get_buildings(self):
        for paved_street in self.paved_streets:
            paved_street.buildings[0], paved_street.buildings[1] = paved_street.split(",")

    def adj_list(self):
        buildings = self.buildings
        streets = self.paved_streets
        adj_list = {}

        for building in buildings:
            adj_list[building] = []
            for street in streets:
                if street.buildings[0] == building:
                    if street.buildings[1] not in adj_list[building]:
                        adj_list[building].append(
                            street.buildings[1])
                elif street.buildings[1] == building:
                    if street.buildings[0] not in adj_list[building]:
                        adj_list[building].append(
                            street.buildings[0])
        return adj_list

    def verify_coverage_plan(self):
        visited = {}
        parent = {}
        output = []
        queue = Queue()
        counter = 0
        for building in self.town.buildings:
            for p_building in self.buildings:
                if building.address == p_building.address:
                    counter += 1
                    break
        if counter < len(self.town.buildings):
            return False
        adj_list = self.adj_list()

        for building in adj_list.keys():
            visited[building] = False
            parent[building] = None

        s = list(adj_list.keys())[0]
        visited[s] = True
        queue.put(s)

        while not queue.empty():
            adj_building = queue.get()
            output.append(adj_building)

            for building in adj_list[adj_building]:
                if not visited[building]:
                    visited[building] = True
                    parent[building] = adj_building
                    queue.put(building)
        if len(output) < len(self.buildings):
            return False
        return True

    def evaluate_paving_plan(self):
        print(self.name)
        print('Connected: ' + str(self.verify_coverage_plan()))
        print('Total Cost: ' + str(self.find_total_cost(self.town)))
        self.verify_paving_plan(self.town)
        print('Optimal: ' + str(self.minimum_cost))

    # Adapted from Skeina's implementation of Kruskal's algorithm
    def verify_paving_plan(self, town):
        is_min_cost = False
        result = []
        total_buildings = len(town.buildings)
        i = 0
        e = 0
        town.streets = sorted(town.streets, key = lambda street: street.paving_cost)

        parent = []
        rank = []

        for building in range(total_buildings):
            parent.append(building)
            rank.append(0)
    
        minimum_cost = 0
        while e < total_buildings - 1:
            weight = town.streets[i].paving_cost
            u = town.streets[i].buildings[0].index
            v = town.streets[i].buildings[1].index
            i = i + 1
            x = find_parent(parent, u)
            y = find_parent(parent, v)
            if x != y:
                e = e + 1
                result.append([town.buildings[u].address, town.buildings[v].address])
                union_find(parent, rank, x, y)
                minimum_cost += weight
        self.paved_streets = result.copy()
        self.minimum_cost = minimum_cost

        return is_min_cost


def find_parent(parent, i):
    if parent[i] == i:
        return i
    return find_parent(parent, parent[i])


def union_find(parent, rank, x, y):
    x_root = find_parent(parent,x)
    y_root = find_parent(parent,y)
    if rank[x_root] < rank[y_root]:
        parent[x_root] = y_root
    elif rank[x_root] > rank[y_root]:
        parent[y_root] = x_root
    else:
        parent[y_root] = x_root
        rank[x_root] += 1


class PavedStreet:
    def __init__(self):
        self.buildings = []

    def __str__(self):
        return f"{self.buildings[0].address},{self.buildings[1].address}"

    def print_street_a(self):
        print(
            f"{self.buildings[0].index + 1} {self.buildings[1].index + 1}")


class Building:

    def __init__(self, address, index=None):
        self.address = address
        self.index = index
        self.streets = []
        self.non_neighbors = []
        self.visited = False

    def print_building_a(self):
        print(f"  [{self.index + 1}] {self.address}")


def paving_plan_from_file(filepath, town):
    with open(filepath) as f:
        lines = f.readlines()
        paving_plan = PavingPlan(lines[0].strip('\n'))
        paving_plan.town = town

        paving_plan.name = lines[0].strip('\n')
        paved_streets = lines[1: len(lines)]
        for paved_street in paved_streets:
            src_address, dest_address = paved_street.split(",")
            src = paving_plan.get_or_create_building(src_address.strip('\n'))
            dest = paving_plan.get_or_create_building(dest_address.strip('\n'))
            s = PavedStreet()
            s.buildings.append(src)
            s.buildings.append(dest)
            paving_plan.add_street(s)
        return paving_plan
