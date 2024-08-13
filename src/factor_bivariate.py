from sage.all import *
import re
import sys
import json

def convert_polynomial_to_list(polynomial):
    # Split the polynomial string into terms
    terms = polynomial.split(' + ')
    result = []

    # Regular expression patterns for matching terms
    x_pattern = re.compile(r'x(?:\^(\d+))?')
    y_pattern = re.compile(r'y(?:\^(\d+))?')

    for term in terms:
        # Extract exponents of x and y
        x_match = x_pattern.search(term)
        y_match = y_pattern.search(term)

        # Determine the exponent values, default to 0 if not found
        if x_match:
            x_exp = x_match.group(1) if x_match.group(1) else '1'
        else:
            x_exp = '0'

        if y_match:
            y_exp = y_match.group(1) if y_match.group(1) else '1'
        else:
            y_exp = '0'

        if 'x' in term and 'y' in term:
            # Both x and y present
            formatted_term = f"x{x_exp}.y{y_exp}"
        elif 'x' in term:
            # Only x present
            formatted_term = f"x{x_exp}"
        elif 'y' in term:
            # Only y present
            formatted_term = f"y{y_exp}"
        else:
            # Neither x nor y present (constant term)
            formatted_term = "i"

        result.append(formatted_term)

    return result
# def convert_polynomial_to_list(polynomial):
#     # Split the polynomial string into terms
#     terms = polynomial.split(' + ')
#     result = []
#
#     # Regular expression patterns for matching terms
#     x_pattern = re.compile(r'x\^(\d+)')
#     y_pattern = re.compile(r'y\^(\d+)')
#
#     for term in terms:
#         # Extract exponents of x and y
#         x_match = x_pattern.search(term)
#         y_match = y_pattern.search(term)
#
#         # Determine the exponent values, default to 0 if not found
#         x_exp = x_match.group(1) if x_match else '0'
#         y_exp = y_match.group(1) if y_match else '0'
#
#         if 'x' in term and 'y' in term:
#             # Both x and y present
#             formatted_term = f"x{x_exp}.y{y_exp}"
#         elif 'x' in term:
#             # Only x present
#             formatted_term = f"x{x_exp}"
#         elif 'y' in term:
#             # Only y present
#             formatted_term = f"y{y_exp}"
#         else:
#             # Neither x nor y present (constant term)
#             formatted_term = "i"
#
#         result.append(formatted_term)
#
#     return result

def factorise(P,l,m):

    F = GF(2)

    # Step 2: Define the polynomial ring over GF(2) with variables x and y
    R = PolynomialRing(F, ['x', 'y'])
    x, y = R.gens()

    # Define the ideals generated by x^l - 1 and y^m - 1
    I_x = R.ideal(x**l - 1)
    I_y = R.ideal(y**m - 1)

    # Step 4: Create the quotient ring
    Q = R.quotient(I_x + I_y)

    # Step 5: Define a polynomial in the original ring
    #p = x**2 + x**5 * y + y + 1
    p = 0
    for pow in P:
        p+=(x**int(pow[0]))*(y**int(pow[1]))

    # Step 6: Factorize the polynomial in the original ring
    factors = p.factor()

    # Print the polynomial and its factors in the original ring
    # print(f"Polynomial in original ring: {p}")
    # print(f"Factors in original ring: {factors}")

    # Step 7: Map the factors into the quotient ring
    Q_factors = [(Q(f), multiplicity) for f, multiplicity in factors]
    #print(Q_factors)
    # Print the factors in the quotient ring
    f_list=[]
    for factor, multiplicity in Q_factors:
        f=str(factor).replace("bar", "")
        pf=convert_polynomial_to_list(f)
        f_list.append((pf, multiplicity))

    #print(f_list)
    return f_list

def main():
    # Get the input terms from the command line argument
    P_str = sys.argv[1]
    l_str = sys.argv[2]
    m_str = sys.argv[3]

    print(P_str)
    print(l_str)
    print(m_str)
    print(type(P_str))
    # Deserialize the JSON string to get the terms
    P = json.loads(P_str)
    print(f"p after: {P}")
    print(type(P))
    # Convert the second argument to an integer
    l = int(l_str)
    # Convert the third argument to a float
    m = int(m_str)

    # Convert the terms to a polynomial and print with the integer and float
    f = factorise(P, l, m)
    print(f)


if __name__ == "__main__":
    main()