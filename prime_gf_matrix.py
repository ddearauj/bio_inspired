import numpy as np
from random import randint

### CORRIGIR RETURN, VAI SER ARRAY E NAO MATRIX, VETORIZAR A FUNÇAO DE MODULUS


class Prime_GF_Matrix(object):
	"""Galois Fields of prime orders"""
	def __init__(self, np_array, k):
		self.matrix = np_array
		self.k = k

	def __add__(self, other):
		""" This will only work for matrixes of same shape and prime order"""
		if isinstance(other, Prime_GF_Matrix):
			assert self.p == other.p, "Matrixes have different orders: %s vs %s" %(self.k, other.k)
			assert self.matrix.shape == other.matrix.shape, "Matrixes must be the same shape. %s vs. %s "  %(self.matrix.shape, other.matrix.shape)

			matrix = np.add(self.matrix, other.shape)
			return np.array([xi%k for xi in matrix])

		else:
			return other.__radd__(self)

	def __sub__(self, other):
		""" This will only work for matrixes of same shape and prime order"""
		if isinstance(other, Prime_GF_Matrix):
			assert self.p == other.p, "Matrixes have different orders: %s vs %s" %(self.k, other.k)
			assert self.matrix.shape == other.matrix.shape, "Matrixes must be the same shape. %s vs. %s "  %(self.matrix.shape, other.matrix.shape)

			matrix = np.subtract(self.matrix, other.shape)

			# if the element is negative then element = k + (a - b)

			negative_fixer = lambda t: t if t > 0 else t + self.k
			v_negative_fixer = np.vectorize(negative_fixer)
			matrix = v_negative_fixer(matrix)

			# make sure elements are < then field order

			matrix = np.array([xi%k for xi in matrix])

			return matrix

		else:
			return other.__rsub__(self)


		def __mul__(self, other):
		""" This will only work for matrixes of same shape and prime order"""
		if isinstance(other, Prime_GF_Matrix):
			assert self.p == other.p, "Matrixes have different orders: %s vs %s" %(self.k, other.k)
			assert self.matrix.shape == other.matrix.shape, "Matrixes must be the same shape. %s vs. %s "  %(self.matrix.shape, other.matrix.shape)

			matrix = np.dot(self.matrix, other.shape)
			return np.array([xi%k for xi in matrix])

		else:
			return other.__rsub__(self)


    def random_elementary_row_operation(self):
    	pass


    def _random_invertible_matrix(self, shape=3, n_operations=5):
    	""" 
    	Returns a invertible matrix. To do that, it starts from the identity matrix and cretes intermediary matrixes via elementary operations
		Since elementary matrixes are invertible and the product of invertible matrixes is also invertible, we multiply all those matrixes to arrive 
		in a invertible matrix

		This is could be optimized

    	"""


    	aux_matrixes = []
    	for i in range(n_operations):

    		# create elementary operation
    		# row_i = x_1*row_1 + x_2+row_2 ... + x_shape*row_shape
    		elementary_array = np.random.randint(5, size=shape)

    		# The idea is to multiply the identity matrix by the array that describes the elementary operation
    		# and then add these rows
    		new_row = (np.identity(shape) * elementary_array).sum(axis=0)
    		new_row = np.array([xi%k for xi in new_row])

    		# substitute one row in the identity matrix

    		aux_matrix = np.identity(shape)
    		aux_matrix[randint(0, shape0)] = new_row
    		aux_matrixes.append(aux_matrix)

    	random_invertible_matrix = np.identity(shape)
    	for aux_matrix in aux_matrixes:
    		random_invertible_matrix = random_invertible_matrix @ aux_matrix

    	return random_invertible_matrix



    		



    	



