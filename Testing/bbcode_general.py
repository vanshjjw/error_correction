from src.core_general import BBCodeGeneral

def raw_codes(codes: dict):
    codes["0"] = {
        "gen": ['x', 'y'],
        "rel": ['x3', 'y2', 'x.y-1.x.y'],
        "a": ['i', 'x', 'y.x2'],
        "b": ['i', 'y', 'x.y'],
        "answer": [12, 2, 2]
    }
    codes["1"] = {
        "gen": ['x', 'y'],
        "rel": ['y4', 'x6', 'y-1.x.y.x'],
        "a": ['i', 'x'],
        "b": ['i', 'y', 'x6', 'y3.x', 'y.x7', 'y3.x5'],
        "answer": [72, 8, 9]
    }
    codes["2"] = {
        "gen": ['x', 'y'],
        "rel": ['y5', 'x8', 'x-1.y.x.y'],
        "a": ['i', 'y.x4'],
        "b": ['i', 'x', 'x2', 'y', 'y3.x', 'y2.x6'],
        "answer": [80,8,10]
    }
    codes["3"] = {
        "gen": ['x', 'y'],
        "rel": ['y3', 'x16', 'x-1.y.x.y'],
        "a": ['i', 'x', 'y', 'x14'],
        "b": ['i', 'x2', 'y.x4', 'x11'],
        "answer": [96,8,12]
    }
    codes["4"] = {
        "gen": ['x', 'y'],
        "rel": ['y3', 'x14', 'x-1.y.x.y'],
        "a": ['i', 'x7', 'y.x10', 'x8'],
        "b": ['i', 'y', 'y2.x13', 'x5'],
        "answer": [82,10,9]
    }
    codes["5"] = {
        "gen": ['x', 'y'],
        "rel": ['y4', 'x12', 'y-1.x.y.x'],
        "a": ['i', 'y', 'x9', 'y.x'],
        "b": ['i', 'x7', 'y2.x9', 'x2'],
        "answer": [96,10,12]

    }
    codes["6"] = {
        "gen": ['x', 'y'],
        "rel": ['y6', 'x8', 'x-1.y.x.y'],
        "a": ['i', 'x', 'y3.x2', 'y2.x3'],
        "b": ['i', 'x', 'y4.x6', 'y5.x3'],
        "answer": [96,12,10]
    }
    codes["7"] = {
        "gen": ['x', 'y'],
        "rel": ['y4', 'x10', 'x.y.x.y'],
        "a": ['i', 'y.x5', 'x5', 'y.x6'],
        "b": ['i', 'y2', 'x', 'y2.x3'],
        "answer": [80, 9, 9]
    }
    return codes


def display_code(code, n, k, d):
    print(f"Generators: {code['gen']}")
    print(f"Relators: {code['rel']}")
    print(f"A: {code['a']}")
    print(f"B: {code['b']}")
    print(f"Obtained code: [{n}, {k}, {d}]")
    print(f"Known code: {code['answer']}")
    return


def run_bbcode_general_examples():
    Main = {}
    distance_method = 3
    distance_margin = 1.15 # 15% margin of error

    Main = raw_codes(Main)

    for i in range(7, len(Main)):
        example = Main[str(i)]
        code = BBCodeGeneral(example["gen"], example["rel"], safe_mode=True).set_expression(example["a"], example["b"])

        n, k, d = code.generate_bb_code(distance_method=distance_method)
        n_known, k_known, d_known = example["answer"]

        passed = n == n_known and k == k_known and d_known <= d * distance_margin

        if passed:
            print(f"Code {i} passed.")
        else:
            print(f"\n\nCode {i} failed. Details:")
            display_code(example, n, k, d)
            print("\n\n")



if __name__ == "__main__":
    run_bbcode_general_examples()
