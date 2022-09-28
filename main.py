class Town:
    name = ""
    streets = []
    buildings = []

    def __init__(self, name):
        self.name = name
        self.streets = []
        self.buildings = []
        self.building_index_dict = {}

    def add_street(self, street):
        self.streets.append(street)

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

    def write_town(self, write_file):
        w = open(write_file, 'w')
        w.write(self.name + "\n")
        for street in self.streets:
            w.write(str(street) + "\n")

    def print_town_s(self):
        print(self.name)
        for s in self.streets:
            print(s)

    def print_town_s_formatted(self):
        print(self.name)
        print("{: <12} {: <25} {: <25} ".format("Paving cost", "Src", "Dest"))
        for s in self.streets:
            print("{: <12} {: <25} {: <25} ".format(s.paving_cost, s.buildings[0].address, s.buildings[1].address))

    def print_town_a(self):
        print(self.name)
        building_arr = []

        # Print Each Building Address
        for i in range(0, len(self.streets)):
            src = self.streets[i].buildings[0].address
            dest = self.streets[i].buildings[1].address

            if src not in building_arr:
                building_arr.append(src)
            if dest not in building_arr:
                building_arr.append(dest)

        for i in building_arr:
            print(i)

        # Print each street and associated cost
        for i in range(0, len(self.streets)):
            src = self.streets[i].buildings[0].address
            dest = self.streets[i].buildings[1].address
            paving_cost = self.streets[i].paving_cost
            print(f"{src},{dest},{paving_cost}")

    def print_town_a_new(self):
        print(f"Town: {self.name}")
        print(f"Number of Buildings: {len(self.buildings)}")

        # Print Each Building Index and Address
        for building in self.buildings:
            building.print_building_a()

        print("=====")
        print(f"{len(self.buildings)} {len(self.streets)}")

        # Print each street and associated cost
        for street in self.streets:
            street.print_street_a()


class Street:
    def __init__(self, paving_cost):
        self.paving_cost = paving_cost
        self.buildings = []

    def __str__(self):
        return f"{self.paving_cost},{self.buildings[0].address},{self.buildings[1].address}"

    def print_street_a(self):
        print(f"{self.buildings[0].index + 1} {self.buildings[1].index + 1} {self.paving_cost}")

    @property
    def src(self):
        return self.buildings[0]

    @src.setter
    def src(self, building):
        if len(self.buildings) > 0:
            self.buildings[0] = building
        else:
            self.buildings.append(building)

    @property
    def dest(self):
        return self.buildings[1]

    @dest.setter
    def dest(self, building):
        if len(self.buildings) > 1:
            self.buildings[1] = building
        elif len(self.buildings) > 0:
            self.buildings.append(building)
        else:
            self.buildings.append(None)
            self.buildings.append(building)


class Building:

    def __init__(self, address, index=None):
        self.address = address
        self.index = index
        self.streets = []
        self.non_neighbors = []

    def print_building_a(self):
        print(f"[{self.index + 1}] {self.address}")


def build_town_from_file(filepath):
    with open(filepath) as f:
        lines = f.readlines()
        town_name = lines[0]
        streets = lines[1:len(lines)]

        town = Town(town_name.strip('\n'))

        for street in streets:
            path_length_str, src_address, dest_address = street.split(",")
            path_length = int(path_length_str)

            src = town.get_or_create_building(src_address.strip('\n'))
            dest = town.get_or_create_building(dest_address.strip('\n'))
            s = Street(path_length)
            s.buildings.append(src)
            s.buildings.append(dest)
            town.add_street(s)

        return town


if __name__ == '__main__':
    build_town_from_file("static/town.txt")
