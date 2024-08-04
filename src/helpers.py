import numpy as np
from ldpc.mod2 import reduced_row_echelon, rank
from copy import deepcopy


## ----------------- QEC Specific Functions ----------------- ##


def generators(G_standard):
    G1=G_standard[:][:G_standard.shape[1]//2]
    G2=G_standard[:][G_standard.shape[1]//2:]
    H_x = G1[ ~ np.all(G1 == 0, axis=1)]
    H_z = G2[ ~ np.all(G2 == 0, axis=1)]
    return H_x, H_z


def standard_form(H_x, H_z):
    G = make_block_diagonal(H_x, H_z)
    n, m = G.shape[1] // 2, G.shape[0]

    G1 = G[:, :n]
    G2 = G[:, n:]
    G1_rref, r, G1_transform_rows, G1_transform_cols = reduced_row_echelon(G1)
    G2 = (G1_transform_rows@G2@G1_transform_cols)%2

    E = G2[r:,r:]
    E_rref, s, E_transform_rows, E_transform_cols = reduced_row_echelon(E)
    D = ( E_transform_rows @ G2[r:,:r] ) % 2
    C = ( G2[:r,r:] @ E_transform_cols ) % 2

    A = ( G1_rref[:r,r:] @ E_transform_cols ) % 2

    G1_rref[:r,r:] = A
    G2[r:,r:] = E_rref
    G2[r:,:r] = D
    G2[:r,r:] = C

    G_complete = np.hstack((G1_rref, G2))
    G_standard = G_complete[ ~ np.all(G_complete == 0, axis=1)]
    return G_standard


def find_logical_generators(G_standard, rank_x: int) -> list[np.ndarray]:
    n = G_standard.shape[1] // 2
    k = n - G_standard.shape[0]

    A2 = deepcopy(G_standard[: rank_x, n - k: n])
    E  = deepcopy(G_standard[rank_x:, n + n - k:])
    C  = deepcopy(G_standard[: rank_x, n + n - k:])

    zero_l = np.zeros((k, rank_x), dtype=int)
    zero_m = np.zeros((k, n - k - rank_x), dtype=int)
    zero_r = np.zeros((k, k), dtype=int)

    identity = np.eye(k)

    Lx = np.hstack((zero_l, E.T, identity, C.T, zero_m, zero_r))
    Lz = np.hstack((zero_l, zero_m, zero_r, A2.T, zero_m, identity))

    return Lx, Lz


## ----------------- Polynomial Helpers ----------------- ##


def _construct_expression(x_power: int, y_power: int):
    if x_power == 0 and y_power == 0:
        return "i"
    if x_power == 0:
        return f"y{y_power}"
    if y_power == 0:
        return f"x{x_power}"
    return f"x{x_power}.y{y_power}"


def _construct_powers(monomial: str, l: int, m: int):
    x_power = 0
    y_power = 0
    for mu in monomial.split("."):
        if mu[0] == "x":
            x_power += int(mu[1:])
        if mu[0] == "y":
            y_power += int(mu[1:])

    return x_power % l, y_power % m


def construct_expression_from_powers(S : list[(int, int)], l: int, m: int):
    return [_construct_expression(x_power, y_power) for x_power, y_power in S]


def construct_powers_from_expression(polynomial_expression: list[str], l: int, m: int):
    return [_construct_powers(monomial, l, m) for monomial in polynomial_expression]


def multiply_m1_and_m2_inverse(m1: str, m2: str, l: int, m: int):
    x_power = 0
    y_power = 0

    for mu in m1.split("."):
        if mu[0] == "x":
            x_power += int(mu[1:])
        if mu[0] == "y":
            y_power += int(mu[1:])

    for mu in m2.split("."):
        if mu[0] == "x":
            x_power -= int(mu[1:])
        if mu[0] == "y":
            y_power -= int(mu[1:])

    return x_power % l, y_power % m


def multiply_polynomials_mod_2(poly1: list[str], poly2: list[str], l: int, m: int):
    result = []
    for value1 in poly1:
        for value2 in poly2:
            multiplicands = value1.split(".") + value2.split(".")
            x_power = 0
            y_power = 0

            for mu in multiplicands:
                if mu[0] == "x":
                    x_power += int(mu[1:])
                if mu[0] == "y":
                    y_power += int(mu[1:])

            x_power %= l
            y_power %= m

            answer = _construct_expression(x_power, y_power)
            if answer in result:
                result.remove(answer)
            else:
                result.append(answer)

    return result


## ----------------- Matrix Helpers ----------------- ##

def display(M, middle_line = False):
    size = len(M[0])

    h_line = "--" * size
    print(h_line)

    for row in M:
        print("[ ", end = "")
        for i in range(size):
            print(row[i], end = " ")
            if middle_line and i == size / 2:
                print("|", end = " ")
        print("]")

    print(h_line)
    pass


def hamming_weight(vector: list[int]):
    # hamming weight for a CSS src logical operator (length = 2n)
    n = len(vector) // 2
    weight = sum([1 if vector[i] == 1 or vector[i + n] == 1 else 0 for i in range(n)])
    return weight


def make_block_diagonal(H_x, H_z):
    G = np.block([
        [H_x, np.zeros((H_x.shape[0], H_z.shape[1]), dtype=int)],
        [np.zeros((H_z.shape[0], H_x.shape[1]), dtype=int), H_z]
    ])
    return G


def create_matrix_S(size):
    S = np.eye(size, dtype=int, k=1)
    S[size - 1][0] = 1
    return S


def binary_rank(A):
    return rank(A)


## ----------------- Miscellaneous ----------------- ##

