from math import sqrt
import numpy as np
from random import randint


class TSP(object):
    """docstring for TSP"""
    def __init__(self, array_of_cities):
        self.array_of_cities = np.random.permutation(array_of_cities)
        # self.array_of_cities = array_of_cities
        self.n_cities = array_of_cities.shape[0]


    def calculate_fitness(self):
        dist = 0    

        for city1, city2, in zip(self.array_of_cities, np.append(self.array_of_cities[1:],[self.array_of_cities[0]])):
            dist += city1.dist(city2)

        self.fitness = -dist



    def mutate(self):

        # select the random cities
        city1_id = randint(0, self.n_cities - 1)
        city2_id = randint(0, self.n_cities - 1)

        # get the object in the array index

        city1_obj = self.array_of_cities[city1_id]
        city2_obj = self.array_of_cities[city2_id]

        # switch'em

        self.array_of_cities[city1_id] = city2_obj
        self.array_of_cities[city2_id] = city1_obj

    def crossover(self, other):

        """
        The idea for this crossover is as follows:

        Randomly generate the point of crossover.
        (the numbers represent a different city)

        [1 2 3 4 5 6 7]
        [1 2 6 5 4 7 3]

        [1 2 3 4] [5 6 7]
        [1 2 6 5] [4 7 3]

        cross 

        [1 2 3 4] [4 7 3]
        [1 2 6 5] [5 6 7]

        Replace the duplicate values with -1
        [1 2 3 4] [-1  7 -1]
        [1 2 6 5] [-1 -1  7]

        fill the -1 with the values from the respective parent right hand size of the cromossome in order

        [1 2 3 4] [5 7 6]
        [1 2 6 5] [4 3 7]

        """

        crossover_point = randint(1, self.array_of_cities.shape[0] - 1)
        # print(crossover_point)

        parent1_left_side  = self.array_of_cities[:crossover_point]
        parent1_right_side = self.array_of_cities[crossover_point:]

        parent2_left_side  = other.array_of_cities[:crossover_point]
        parent2_right_side = other.array_of_cities[crossover_point:]



        # get the duplicate values on the right hand side and replace with -1
        filter1 = np.isin(parent1_right_side, parent2_left_side)
        filter2 = np.isin(parent2_right_side, parent1_left_side)

        parent1_right_side_filtered = parent1_right_side.copy()
        parent2_right_side_filtered = parent2_right_side.copy()

        parent1_right_side_filtered[filter1] = -1
        parent2_right_side_filtered[filter2] = -1


        # fill the -1 in order
        # using np.place the array we want to place is
        # all the values in the on the other parent right hand side
        # so for the parent 1 right hand side, we will place values
        # from the parent 2 right hand side that are not on it
        # parent2_right_side[~np.isin(parent2_right_side, parent1_right_side)]
        # in the example [4, 3]

        np.place(parent1_right_side_filtered, 
                 parent1_right_side_filtered==-1,
                 parent2_right_side[~np.isin(parent2_right_side, parent1_right_side)])


        np.place(parent2_right_side_filtered, 
                 parent2_right_side_filtered==-1,
                 parent1_right_side[~np.isin(parent1_right_side, parent2_right_side)])


        # stack them horizonatally

        child1 = np.hstack([parent1_left_side, parent2_right_side_filtered])
        child2 = np.hstack([parent2_left_side, parent1_right_side_filtered])

        return TSP(child1), TSP(child2)

    def assexual_crossover(self):
        """ 
        The idea is like the mutation but for chunks of cities.
        It works better than the sexual one as a lot of the cities order change due to duplication

        """

        crossover_point = randint(1, self.array_of_cities.shape[0] - 1)

        parent_left_side  = self.array_of_cities[:crossover_point]
        parent_right_side = self.array_of_cities[crossover_point:]

        child = np.hstack([parent_right_side, parent_left_side])\

        return TSP(child)


    def get_array_of_coordinates(self):
        x = [city.x for city in self.array_of_cities]
        y = [city.y for city in self.array_of_cities]

        # append the first city to close the loop
        x.append(self.array_of_cities[0].x)
        y.append(self.array_of_cities[0].y)
        
        return x, y


class City(object):
    """docstring for City"""
    def __init__(self, x, y):
        self.x   = x
        self.y   = y


    def __repr__(self):
        return self.__class__.__name__ + ": " + "(" + str(self.x) + ", " + str(self.y) + ")"

    def dist(self, other):
        delta_x = self.x - other.x
        delta_y = self.y - other.y

        return sqrt(delta_x**2 + delta_y**2)


        