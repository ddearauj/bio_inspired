from random import randint
from random import sample as random_sample

class Population(object):
    """docstring for Pouplation"""
    def __init__(self, population, mutation_prob, crossover_prob, crossover_type="sexual"):
        self.population = population
        self.size = len(population)
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.crossover_type = crossover_type

    def calculate_fitness(self):
        for individual in self.population:
            individual.calculate_fitness()


    def mutate(self):
        for individual in self.population:
            if randint(0, 100) <= self.mutation_prob:
                individual.mutate()


    def crossover(self, selection_params, keep_parents):

        children = []
        
        if self.crossover_type == "sexual":

            # here we will generate a new population
            while len(children) < self.size:
                
                parent1 = self.select(selection_params)
                parent2 = self.select(selection_params)

                # if they are selected for a crossover, do it
                # otherwise, just add the parents to the next population (the childern list)
                if randint(0, 100) <= self.crossover_prob:
                    child1, child2 = parent1.crossover(parent2)
                    children.append(child1)
                    children.append(child2)
                    if keep_parents:
                        children.append(parent1)
                        children.append(parent2)
                else:
                    children.append(parent1)
                    children.append(parent2)

        else:

            # here we will generate a new population
            while len(children) < self.size:
                
                parent = self.select(selection_params)

                # if they are selected for a crossover, do it
                # otherwise, just add the parents to the next population (the childern list)
                if randint(0, 100) <= self.crossover_prob:
                    child  = parent.assexual_crossover()
                    children.append(child)
                    if keep_parents:
                        children.append(parent)
                else:
                    children.append(parent)

        return children


    def reproduction(self, selection_params, keep_parents=False, keep_n_best=0):

        children = self.crossover(selection_params, keep_parents)

        self.calculate_fitness()
        self.sort_pop()
 
        if keep_n_best > 0:
            children.extend(self.population[:keep_n_best])

        self.population = children
        self.calculate_fitness()    

        # supress pop size to its maximum
        self.sort_pop()
        self.population = self.population[:self.size -1]



    def _tournament(self, params):

        competitors = random_sample(self.population, params['n_competitors'])

        fitness_to_beat = competitors[0].fitness
        winner = competitors[0]

        for competitor in competitors:
            if competitor.fitness > fitness_to_beat:
                winner = competitor

        return winner


    def select(self, selection_params):


        if selection_params["type"] == "tournament":
            return self._tournament(selection_params)


    def sort_pop(self):
        self.population.sort(key=lambda x: x.fitness, reverse=True)

