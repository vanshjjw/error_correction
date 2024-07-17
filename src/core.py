import numpy as np
import src.helpers as helper
import src.validators as vd
import src.distance_brute_force as dbf
import src.distance_from_generators as dfg


def create_matrix_S(size):
    S = np.eye(size, dtype=int, k=1)
    S[size - 1][0] = 1
    return S


class BBCode:
    def __init__(self, l: int, m: int, A_expression:list[str], B_expression: list[str], debug = False):
        self.l = l
        self.m = m
        self.A_expression = A_expression
        self.B_expression = B_expression
        self.debug_mode = debug

    def create_parity_check_matrices(self):
        S_l = create_matrix_S(self.l)
        S_m = create_matrix_S(self.m)

        # Make x and y matrices
        x = np.kron(S_l, np.eye(self.m, dtype=int))
        y = np.kron(np.eye(self.l, dtype=int), S_m)

        # Make A and B matrices
        p = self.l * self.m
        A = np.zeros((p, p), dtype=int)
        B = np.zeros((p, p), dtype=int)

        for elem in self.A_expression:
            var, val = elem[0], int(elem[1:])
            A += np.linalg.matrix_power(x, val) if var == 'x' else np.linalg.matrix_power(y, val)

        for elem in self.B_expression:
            var, val = elem[0], int(elem[1:])
            B += np.linalg.matrix_power(x, val) if var == 'x' else np.linalg.matrix_power(y, val)

        H_x = np.concatenate((A, B), axis=1)
        H_z = np.concatenate((B.T, A.T), axis=1)

        if self.debug_mode:
            vd.validate_x_y_matrices(x)
            vd.validate_x_y_matrices(y)
            vd.validate_A_B_matrices(A, self.A_expression)
            vd.validate_A_B_matrices(B, self.B_expression)
            vd.validate_parity_matrix(H_x, H_z)
            print(f"H_x shape: {H_x.shape}")
            print(f"H_z shape: {H_z.shape}")
            print("\nParity matrices created successfully")

        return H_x, H_z

    def generate_bb_code(self):
        H_x, H_z = self.create_parity_check_matrices()

        rank_H_x = helper.calculate_rank_GF2(H_x)
        rank_H_z = helper.calculate_rank_GF2(H_z)

        if self.debug_mode:
            vd.validate_rank(rank_H_x, rank_H_z)

        # src parameters
        num_physical : int = 2 * self.l * self.m
        num_logical : int = num_physical - 2 * rank_H_x

        distance : int = dfg.calculate_distance(H_x, H_z, num_physical, num_logical, rank_H_x, rank_H_z, status_updates=True)
        # distance : int = dbf.calculate_distance_brute_force(H_x, H_z, num_physical, num_logical, status_updates=True)

        return num_physical, num_logical, distance



def single_run():
    A = {
        "l": 4,
        "m": 3,
        "a": ["x0", "x1"],
        "b": ["y0", "y1"],
    }

    l = A["l"]
    m = A["m"]
    a = A["a"]
    b = A["b"]

    print(f"l: {l}, m: {m}")
    print(f"A: {a}")
    print(f"B: {b}")

    code = BBCode(l, m, a, b, debug=False)
    n, k, d = code.generate_bb_code()

    print(f"\nRequired BB code: [{n}, {k}, {d}]")
    if "answer" in A:
        print(f"answer: {A['answer']}")


def single_run_2():
    A = {
        "l": 9,
        "m": 6,
        "a": ["x3", "y1", "y2"],
        "b": ["y3", "x1", "x2"],
        "answer": [108, 8, 10]
    }

    l = A["l"]
    m = A["m"]
    a = A["a"]
    b = A["b"]

    code = BBCode(l, m, a, b, debug=False)
    n, k, d = code.generate_bb_code()

    print(f"\nRequired BB code: [{n}, {k}, {d}]")
    if "answer" in A:
        print(f"answer: {A['answer']}")



if __name__ == "__main__":
    single_run()





