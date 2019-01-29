from population import Population
from n_queens import N_Queens
import time
import numpy as np

def evolutionary_algorithm(Pop, iterations, cross_over_params):
    for i in range(iterations):
        Pop.calculate_fitness()
        if i%10 == 0:
            # print(i)
            Pop.sort_pop()
            if Pop.population[0].fitness > -1.0:
                break
            # else:
                # print(Pop.population[0].fitness)
        Pop.crossover(cross_over_params)
        Pop.mutate()
    Pop.calculate_fitness() # if no solution is found after all iterations
    return Pop, i



# there might be a better way to create a simulate function
# maybe one in which you can pass the object constructor as a function to
# generate the population
# for now, as I have no internet connection, let's use this approach

def simulate_N_Queens(N_simulations, pop_size, n_evo_iterations, mutation_prob, crossover_prob, cross_over_params, board_size, output_file_name):

    simulation_results = []
    simulation_results_headers = ['N_Queens', 'fitness', 'iterations', 'time_in_seconds']
    simulation_results.append(simulation_results_headers)
    for simulation_number in range(N_simulations):
        t = time.process_time()

        # create new population
        population = []
        for i in range(pop_size):
            population.append(N_Queens(board_size))

        Pop = Population(population, mutation_prob, crossover_prob)
        Pop, i = evolutionary_algorithm(Pop, n_evo_iterations, cross_over_params)
        elapsed_time = time.process_time() - t

        sim_result = [board_size, Pop.population[0].fitness, i, elapsed_time]
        simulation_results.append(sim_result)
        print(simulation_number, end="-")
        print(Pop.population[0].fitness, end=" i=")
        print(i, end=" sec:")
        print(elapsed_time)


    np.savetxt((str(output_file_name) + ".csv"), simulation_results, delimiter=',', fmt='%s')


if __name__ == '__main__':

    N_simulations     = 400
    pop_size          = 300
    n_evo_iterations  = 5000
    mutation_prob     = 30
    crossover_prob    = 80
    cross_over_params = {"type":"tournament", "n_competitors": 30}
    board_size        = 100
    output_file_name  = "simulation_" + str(board_size) + "Queens_PopSize" + str(pop_size) + "_MutProb" + str(mutation_prob) + "CrossProb" + str(crossover_prob) + "SelectionType" + str(cross_over_params["type"])
    print(output_file_name)
    simulate_N_Queens(N_simulations, pop_size, n_evo_iterations, mutation_prob, crossover_prob, cross_over_params, board_size, output_file_name)



