#!/usr/bin/env python

import argparse

from solver_dummy.functions import square


def main(x):
    result = square(x)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="square some value")
    parser.add_argument("x", help="some value to be squared", type=float)
    args = parser.parse_args()
    x = args.x
    main(x)
