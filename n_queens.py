import numpy as np
from random import randint

class N_Queens(object):
    """docstring for N_Queens"""
    def __init__(self, size, board_model=None):
        self.size = size
        if board_model is None:
            self._create_random_board_model()
        else:
            self.board_model = board_model
            self._create_board_from_model()

    def __repr__(self):
        return self.__class__.__name__ + "\n" + str(self.board)


    def _create_random_board_model(self):
        """
        A more efficient way to model the board for this problem,
        Compared to the naive implementation is a list
        with numbers from 0 to n-1.
        The index represents the column and the value the row in which the queen is placed.
        This way we satisfy the restrictions:
        sum_of_columns = 1
        sum_of_row     = 1

        Now the problem is a combinatory problem, great to be solved by GA's
        """

        board_model      = np.arange(self.size)
        np.random.shuffle(board_model)
        self.board_model = board_model
        self._create_board_from_model()

    def _create_board_from_model(self):

        board = np.zeros((self.size,self.size))
        for column, row in enumerate(self.board_model):
            board[row][column] = 1

        self.board = board



    def calculate_fitness(self):
        """ 
        Only need to check the diagonals. This model restricts the row and column attack
        """
        n_extras = 0

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
        Switches the position of a random selected queen with a another random selected queen
        """

        # select the random columns
        queen1_column = randint(0, self.size - 1)
        queen2_column = randint(0, self.size - 1)

        # get the row values of the random columns
        queen1_row = self.board_model[queen1_column]
        queen2_row = self.board_model[queen2_column]

        # switch'em

        self.board_model[queen1_column] = queen2_row
        self.board_model[queen2_column] = queen1_row

        # update board for fitness
        self._create_board_from_model()


    def crossover(self, other):

        """
        The idea for this crossover is as follows:

        Randomly generate the point of crossover.

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

        crossover_point = randint(1, self.board_model.shape[0] - 1)

        parent1_left_side  = self.board_model[:crossover_point]
        parent1_right_side = self.board_model[crossover_point:]

        parent2_left_side  = other.board_model[:crossover_point]
        parent2_right_side = other.board_model[crossover_point:]



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

        child1_model = np.hstack([parent1_left_side, parent2_right_side_filtered])
        child2_model = np.hstack([parent2_left_side, parent1_right_side_filtered])

        return N_Queens(self.size, board_model=child1_model), N_Queens(self.size, board_model=child2_model)


    def assexual_crossover(self):

        """
        [1 2 3 4 5 6 7]

        [1 2 3 4] [5 6 7]

        [5 6 7] [1 2 3 4] 
        """



        crossover_point = randint(1, self.board_model.shape[0] - 1)

        child_model = hstack([self.board_model[crossover_point:], self.board_model[:crossover_point]])

        return N_Queens(self.size, board_model=child_model)



