import math







from random import randint
from random import sample as random_sample
from population import Population

class CobAINet_Population(Population):
    """update constructor to inherit from population"""

    def __init__(self, population, mutation_prob, crossover_prob, crossover_type="sexual", supression_radious):
        self.population = population  # list containing the antibodies objects
        self.size = len(population)
        self.affinity_matrix # this will be a numpy 2D array
        # self.antibodies      # list containing the antibodies objects
        self.supression_radious = supression_radious

    def calculate_fitness(self):
        for individual in self.population:
            individual.calculate_fitness()


    def mutate(self):
        for individual in self.population:
            if randint(0, 100) <= self.mutation_prob:
                individual.mutate()


    def sort_pop(self):
        self.population.sort(key=lambda x: x.fitness, reverse=True)



    def update_affinity(self):
        """ Updates the affinity between each cell in the imuno system """

        total_concentration = 0

        # iterating though a numpy array
        affinity_matrix = np.empty([self.size, self.size])


        # this is wasteful
        # it is a symmetric matrix. I don't need to iterate over all the antibodies...
        # should update to a pythonic version of:
        # 
        # for (i = 0; i < size; i++) {
        #     for (j = i ; j < size; j++) {
        #         affinity_matrix[i][j] = distance(population[i], population[j]);
        #     }
        # }
        #
        # for (j = 0; j < size; j++) {
        #     for (i = j; i < size; i++) {
        #         affinity_matrix[i][j] = affinity_matrix[j][i];
        #     }
        # }
        
        for i,j in np.ndindex(affinity_matrix.shape):
            affinity_matrix[i,j] = population[i].distance(population[j])

        # after we calculate the distance in the antibodies, we update the value 
        # I took this from the PhD dissertation from a guy in the lab. It is in portuguse, though. I believe the english version is this paper:
        # https://ieeexplore.ieee.org/abstract/document/5949758
        # na hora de documentar, colocar o calculo e explicação do que é de fato a afinidade entre duas celulas


        for i,j in np.ndindex(affinity_matrix.shape):
            if (affinity_matrix[i,j] <= self.supression_radious and i != j):
                affinity_matrix[i,j] = self.population[j].concentration * (supression_radious - affinity_matrix[i,j])
            else:
                affinity_matrix[i,j] = 0


        # now we calculate the total affinity of the cell i and all the other cells in the population
        # because I want to reset the values only with new cell_i and not at every i,j loop
        # I will do this loop in a C like fashion. Will look for a pythonic way later
        for i in range(self.size):
            population[i].total_affinity = 0
            total_cell_concentration = 0
            
            for j in range(self.size):
                if (self.population[i].fitness <= self.population[j].fitness and i !=j):
                    population[i].total_affinity += affinity_matrix[i,j]
                    total_cell_concentration += population[j].concentration

            if total_cell_concentration > 0:
                population[i].total_affinity = population[i].total_affinity/somaconcentracao

            else: # in this case the set J is empty, so no affinity between cell i and the population
                population[i].total_affinity = 0




def update_beta(initial_beta, final_beta, iteration, max_iterations):
    """ Returns a updated value for beta, as it decays through the iterations """
    return ((initial_beta - final_beta) / (1 + math.exp((20/max_iterations) * (iteration - max_iterations/2)))) + final_beta





def cob_ai_net(population, initial_beta=3, final_beta=0.001):

    beta = initial_beta
    pop.calculate_fitness()
    affinity()

    for i in iterations:
        
        if i % update_beta_in == 0:
            beta = update_beta()

        clone()
        mutate()
        select()
        fitness()
        affinity()
        update_concentration()
        eliminate()
        affinity()