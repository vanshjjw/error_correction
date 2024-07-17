import numpy as np
import code.Helpers as helper
from copy import deepcopy


# Find all possible combinations of logical operators, multiplied by stabilizers
def generate_binary_combinations_for_generators(i:int, num_bits:int, num_stabilizers: int, arr) -> np.ndarray:
    if i == num_bits:
        if sum(arr[num_stabilizers:]) == 0:
            return
        else:
            yield arr
            return

    arr[i] = 0
    yield from generate_binary_combinations_for_generators(i + 1, num_bits, num_stabilizers, arr)
    arr[i] = 1
    yield from generate_binary_combinations_for_generators(i + 1, num_bits, num_stabilizers, arr)


def find_logical_generators(G_standard, rank_x: int, status_updates=False) -> list[np.ndarray]:
    n = G_standard.shape[1] // 2
    k = n - G_standard.shape[0]

    A2 = deepcopy(G_standard[: rank_x, n - k: n])
    E = deepcopy(G_standard[rank_x:, n + n - k:])
    C = deepcopy(G_standard[: rank_x, n + n - k:])
    zero_l = np.zeros((k, rank_x), dtype=int)
    zero_m = np.zeros((k, n - k - rank_x), dtype=int)
    zero_r = np.zeros((k, k), dtype=int)
    identity = np.eye(k)

    Lx = np.hstack((zero_l, E.T, identity, C.T, zero_m, zero_r))
    Lz = np.hstack((zero_l, zero_m, zero_r, A2.T, zero_m, identity))

    return Lx, Lz




def calculate_distance(H_x, H_z, n:int, k: int, rank_x: int, rank_z: int, status_updates=False):
    G_standard = helper.standard_form(helper.pre_process(H_x, H_z))

    # refer Neilson and Chuang, Chapter 10, Eq. 10.111
    #
    #   column size = rank_x | n - k - rank_x | k
    #
    # G_standard    = [ I A1 A2 | B 0 C ]       size = rank_x
    #                 [ 0 0  0  | D I E ]       size = n - k - rank_x ( = rank_z)
    #
    # For BB codes, rank_x = rank_z

    Lx, Lz = find_logical_generators(G_standard, rank_x, status_updates)

    complete_matrix = np.vstack((G_standard, Lx, Lz))

    iterator = generate_binary_combinations_for_generators(0, n + k, n - k, np.zeros(n + k, dtype=int))

    distance=2**(2*n)
    for combination in iterator:
        p = np.zeros((2 * n), dtype=int)
        #print(len(combination))
        for i in range(len(combination)):
            if combination[i] == 1:
                p = [(p[j] + complete_matrix[i][j]) % 2 for j in range(2 * n)]
        d=helper.hamming_weight(p)
        if d < distance:
            distance=d
    
    return distance












