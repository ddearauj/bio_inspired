import numpy as np
from random import randint

class N_Queens_Naive(object):
    """docstring for N_Queens"""
    def __init__(self, size, board=None):
        self.size = size
        if board is None:
            self._create_random_board_state()
        else:
            self.board = board

    def __repr__(self):
        return self.__class__.__name__ + "\n" + str(self.board)


    def _place_queen(self):
        """ There might be a better way but since the matrix is super sparse, i think this is fine """
        
        queen_placed = False
        while not queen_placed:
            queen_placement = (randint(0, self.size -1), randint(0, self.size -1))
            if  self.board[queen_placement[0]][queen_placement[1]] == 0:
                self.board[queen_placement[0]][queen_placement[1]] = 1
                queen_placed = True


    def _create_random_board_state(self):
        self.board = np.zeros((self.size, self.size))
        for i in range(self.size):
            self._place_queen()


    def calculate_fitness(self):
        """ 
        For every extra queen in the line of attack, we subtract one on the fitness.
        If there is 3 queens in a line, we subtract two, in order to make the calculatins simple
        Another fitness function could be the number of attacks, which, in the case of 3 queens in
        a single row would be -3 (A->B, A->C and B->C). I might compare the two later on
        """

        extras_in_row = np.sum(self.board, axis=1)
        extras_in_row = extras_in_row[extras_in_row > 1] - 1
        n_extras = extras_in_row.sum()


        extras_in_col = np.sum(self.board, axis=0)
        extras_in_col = extras_in_col[extras_in_col > 1] - 1
        n_extras += extras_in_col.sum()

        # diagonal check

        for i in range(-self.size+1, self.size):
            diag_extras = np.trace(self.board, offset=i)
            if diag_extras > 0:
                n_extras += diag_extras - 1

        # reverse diagonal check

        rev = self.board[:, ::-1]
        for i in range(-self.size+1, self.size):
            rev_diag_extras = np.trace(rev, offset=i)
            if rev_diag_extras > 0:
                n_extras += rev_diag_extras - 1


        self.fitness = (-1)*n_extras
        

    def mutate(self):

        """
        Switches the position of a random selected queen
        """

        # find the queens coordinates
        queens_coordinates = np.argwhere(self.board > 0)
        mutated_queen_coordinate = queens_coordinates[randint(0, self.size - 1)]
        self.board[mutated_queen_coordinate[0]][mutated_queen_coordinate[1]] = 0
        self._place_queen()


    def crossover(self, other):

        """
        Crossover 2 boards.
        Randomly select the point of crossover
        Check for unique values before crossing
        """

        parent1_coords = np.argwhere(self.board  > 0)
        parent2_coords = np.argwhere(other.board > 0)

        # we want to crossover only on the unique values.
        # so first, we find the coordinates present in both parents

        both_coords = np.vstack([parent1_coords, parent2_coords])
        unique_rows, count = np.unique(both_coords, axis=0, return_counts=True)
        dupl_coords = unique_rows[count > 1]

        # now, we will remove the dupl_coords from the parents

        parent1_coords_set = set([tuple(row) for row in parent1_coords])
        parent2_coords_set = set([tuple(row) for row in parent2_coords])
        dupl_coords_set    = set([tuple(row) for row in dupl_coords])


        # parents now have no overlapping coordinates
        parent1_coords = np.array([row for row in parent1_coords_set if row not in dupl_coords_set])
        parent2_coords = np.array([row for row in parent2_coords_set if row not in dupl_coords_set])

        if parent2_coords.shape[0] > 1 :

            crossover_point = randint(1, parent2_coords.shape[0] - 1)

            child1_coords = np.vstack([dupl_coords, parent1_coords[:crossover_point], parent2_coords[crossover_point:]])
            child2_coords = np.vstack([dupl_coords, parent2_coords[:crossover_point], parent1_coords[crossover_point:]])

            # generate boards

            child1_board = np.zeros((self.size,self.size))
            for coord in child1_coords:
                child1_board[coord[0]][coord[1]] = 1

            child2_board = np.zeros((self.size,self.size))
            for coord in child2_coords:
                child2_board[coord[0]][coord[1]] = 1

            return N_Queens_Naive(self.size, board=child1_board), N_Queens_Naive(self.size, board=child2_board) 

        else:
            # parents are identical or have one different position (so no sense in changing it)
            return self, other



