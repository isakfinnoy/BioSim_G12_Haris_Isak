# LEGGER MAPPET MIDLERTIDIG INN I DENNE FILEN:


from biosim.landscape import Highland, Lowland, Desert, Sea
from biosim.animals import Herbivore, Carnivore
import textwrap

import numpy as np


def check_length(strings):
    strings = list(map(len, strings))
    if strings.count(strings[0]) == len(strings):
        return True


class Island:
    cell_types = {'H': Highland,
                  'L': Lowland,
                  'D': Desert,
                  'W': Sea}

    def __init__(self, insert_map, init_animals):
        """
        Constructor for Island class
        :param maps: List, nested list as a matrix describing the layout of the island geography
        :param init_animals: ,
        """

        self.map = self.set_map_coordinates(insert_map)
        self.place_population(init_animals)
        self.year = 0

    #        y, x = loc
    #        cell_left = (y, x-1)
    #        cell_right = (y, x+1)
    #        cell_up = (y+1, x)
    #        cell_down = (y-1, x)
    #        destination_cells = [cell_left, cell_right, cell_up, cell_down]

    #        self.destinations = destination_cells

    #        self.len_x_coord = None
    #        self.len_y_coord = None

    @property
    def year(self):
        return self.year

    @property
    def num_animals(self):
        """
        Returns the total number of animals on the island.
        :return: int >= 0
        """
        num_animals = 0
        for cell in self.map.values():
            num_animals += cell.n_herbivores + cell.n_carnivores
        return num_animals

    @property
    def num_animals_per_species(self):
        """
        Returns a dictionary with number of herbivores and carnivores.
        :return:
        """

        num_animals_per_species = {'n_herbs': 0, 'n_carns': 0}
        for cell in self.map.values():
            num_animals_per_species['n_herbs'] += cell.n_herbivores
            num_animals_per_species['n_carns'] += cell.n_carnivores
        return num_animals_per_species

    def check_map(self, map_input):
        stringmap = map_input.strip()
        strings = stringmap.split('\n')

        if not check_length(strings):
            raise ValueError('Every line in stringmap must be of equal length')

        for elems in str([strings[0] + strings[-1]])[2:-2]:
            if elems != 'W':
                raise ValueError('Not island, island must be surrounded by water'
                                 ', error on southside or northside')

        for elems in strings:
            if not elems.startswith('W'):
                raise ValueError('Not island, island must be surrounded by water,'
                                 ' error on westside')

        for elems in strings:
            if not elems.endswith('W'):
                raise ValueError('Not island, island must be surrounded by water, '
                                 'error on eastside')

        return strings

    def set_map_coordinates(self, map_input):

        #        strings = self.check_map(map)
        #
        #        map_island = {}
        #        self.len_x_coord = len(strings[0])
        #        self.len_y_coord = len(strings)

        strings_island_map = self.check_map(map_input)
        coordinates_map = {}
        for y_index, line in enumerate(strings_island_map):
            for x_index, cell in enumerate(line):
                cell_instance = self.cell_types[cell]()
                coordinates_map[(y_index, x_index)] = cell_instance
        return coordinates_map

    def procreate_cells_map(self):
        for cell in self.map.values():
            cell.birth_cycle()


    def feed_cells(self):
        """
        Method that updates the fodder in the cell,
        and makes all the animals it contains eat.
        :return:
        """
        for landscape in self.map.values():
            landscape.feed_all()

    def age_in_cells(self):
        """
        Method that ages the animals in the cell by one year.
        :return:
        """
        for cell in self.map.values():
            cell.age_animals()

    def weightloss_island(self):
        """
        Method that makes it so that animals in the cell loses
        weight.
        :return:
        """
        for cell in self.map.values():
            cell.weight_loss_cell()

    def place_population(self, init_pop):
        water = self.cell_types['W']
        print(water)
        for position in init_pop:
            loc = position['loc']
            print(loc)
            if loc not in self.map.keys():
                raise ValueError('nonexistent loc in the map provided')
            print(self.map[loc])
            if not self.map[loc].migrate_to:  # IKKE SIKKERT DENNE FUNGERER
                raise ValueError('Animal can not live in water')
            pop = position['pop']
            self.map[loc].place_animals(pop)

    def migrate(self):
        pass

    # I FUNKSJONEN UNDER SKAL VI KALLE PÅ FUNKSJONER FRA ISLAND CELLEN FOR Å KJØRE GJENNOM ETT ÅR
    def run_function_one_year(self):
        pass


if __name__ == "__main__":
    ini_herbs = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]
    ini_carns = [{'loc': (10, 10),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(40)]}]
    default_population = ini_herbs + ini_carns

    default_maps = """
    WWWWWWWWWWWWWWWWWWWWW
    WWWWWWWWHWWWWLLLLLLLW
    WHHHHHLLLLWWLLLLLLLWW
    WHHHHHHHHHWWLLLLLLWWW
    WHHHHHLLLLLLLLLLLLWWW
    WHHHHHLLLDDLLLHLLLWWW
    WHHLLLLLDDDLLLHHHHWWW
    WWHHHHLLLDDLLLHWWWWWW
    WHHHLLLLLDDLLLLLLLWWW
    WHHHHLLLLDDLLLLWWWWWW
    WWHHHHLLLLLLLLWWWWWWW
    WWWHHHHLLLLLLLWWWWWWW
    WWWWWWWWWWWWWWWWWWWWW"""

    default_maps = textwrap.dedent(default_maps)

    i = Island(default_maps, default_population)
    i.procreate_cells_map()
    print(i.total_animals)

    