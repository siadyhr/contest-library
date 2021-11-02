from linalg import Vector

def dot(v, w):
    return sum(x*y for x, y in zip(v, w))

def cross(v, w):
    assert v.dim == w.dim == 3, "Cross product only works in dimension 3"
    return Vector([
        v[1]*w[2] - v[2]*w[1],
        v[2]*w[0] - v[0]*w[2],
        v[0]*w[1] - v[1]*w[0]
        ])
