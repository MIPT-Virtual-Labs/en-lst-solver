#!/usr/bin/env python

import argparse

from solver_dummy import factorial


def main(n):
    result = factorial(n)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="calculation of factorial(n)")
    parser.add_argument("n", help="number to calculate factorial from", type=int)
    args = parser.parse_args()
    n = args.n
    main(n)
