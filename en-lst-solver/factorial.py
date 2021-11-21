import os
import subprocess


def factorial(n):

    if not isinstance(n, int):
        raise ValueError("n must be type of int")
    if not (n >= 1):
        raise ValueError("n must be >= 1")

    folder_bin = os.path.join(os.path.split(__file__)[0], "bin")
    filename_factorial = os.path.join(folder_bin, "factorial")
    command = [filename_factorial, str(n)]
    output = subprocess.check_output(command)
    result = int(output)
    return result
