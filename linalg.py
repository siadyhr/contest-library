class SingularMatrixException(Exception):
    pass

class Vector:
    def __init__(self, coordinates):
        self.coordinates = tuple(coordinates)
        self.dim = len(self.coordinates)

    def __repr__(self):
        return str(self.coordinates)

    def __iter__(self):
        return iter(self.coordinates)

    def __getitem__(self, indices):
        if isinstance(indices, int):
            return self.coordinates[indices]
        return Vector(self.coordinates[indices])
    
    def __add__(self, other):
        return Vector(x+y for x,y in zip(self, other))

    def __rmul__(self, other):
        if type(other) is Matrix:
            return mat_mult(other, self)
        return Vector(other*x for x in self)

    def __mul__(self, scalar):
        return Vector(scalar*x for x in self)

    def append(self, other):
        return Vector(self.coordinates + other.coordinates)

class Matrix:
    def __init__(self, matrix):
        self.matrix = list(list(x) for x in matrix)
        self.size = len(self.matrix), len(self.matrix[0])
        self.by_rows = [Vector(row) for row in self.matrix]
        self.by_cols = [Vector(row[i] for row in self.matrix) for i in range(self.size[1])]

    def __repr__(self):
        return ("%s×%s-matrix\n" % self.size) + "\n".join(" ".join(str(x) for x in line) for line in self.matrix)

    def __getitem__(self, indices):
        if all(isinstance(index, int) for index in indices):
            return self.matrix[indices[0]][indices[1]]
        if isinstance(indices[0], int) and isinstance(indices[1], slice):
            return self.by_rows[indices[0]][indices[1]]
        elif isinstance(indices[0], slice) and isinstance(indices[1], int):
            return self.by_cols[indices[0]][indices[1]]

    def __iter__(self):
        return iter(self.by_rows)

    def __matmul__(self, other):
        return mat_mul(self, other)

    def __rmul__(self, scalar):
        return Matrix([
            scalar * row for row in self.by_rows
            ])

    def __rtruediv__(self, scalar):
        return scalar * matrix_inverse(self)

    def rref(self):
        return RREF(self)

    def swaprows(self, i, j, update=True):
        self.by_rows[i], self.by_rows[j] = self.by_rows[j], self.by_rows[i]
        if update:
            pass

    def multrow(self, i, a, update=True):
        self.by_rows[i] *= a
        if update:
            pass

    def addrow(self, i, v, update=True):
#        print(">addrow")
#        print(self.by_rows[i])
#        print(v)
        self.by_rows[i] += v
        if update:
            pass
#        print("<addrow")

def mat_mul(A, B):
    return Matrix([
            [sum(A[i, k] * B[k, j] for k in range(B.size[0])) for j in range(B.size[1])]
            for i in range(A.size[0])
        ])

def RREF(A):
    for n_iter in range(min(A.size)):
#        print(A.by_rows)
        for good_row in range(n_iter, A.size[0]):
            if A.by_rows[good_row][n_iter] != 0:
                break
            if good_row == A.size[0] - 1:
                raise SingularMatrixException
        if good_row != n_iter:
            A.swaprows(good_row, n_iter, update=False)
#            print("Bytter række %s med række %s" % (good_row, n_iter))
#            print(A.by_rows)
        A.multrow(n_iter, 1/A.by_rows[n_iter][n_iter], update=False)
#        print("Gang række %s med %s" % (n_iter, 1/A.by_rows[n_iter][n_iter]))
#        print(A.by_rows)
        for other_row in range(A.size[0]):
            if other_row == n_iter:
                continue
#            print(2*A[n_iter,:])
            A.addrow(other_row, -1*A.by_rows[other_row][n_iter]*A[n_iter,:], update=False)
#            print("Lægger -række %s til række %s" % (n_iter, other_row))
            #print(A.by_rows)
#    print("Eliminated!")
#    print(A)
#    print(A.by_rows)
    return Matrix(
            row for row in A.by_rows
            )

def standard_basis_element(dimension, i):
    return Vector(1 * (j == i) for j in range(dimension))

def matrix_inverse(A):
    total_matrix = Matrix(
            row.append(standard_basis_element(A.size[1], i)) for i, row in enumerate(A.by_rows)
    )
    return Matrix(
            row[A.size[1]:] for row in RREF(total_matrix)
        )
