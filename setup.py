from setuptools import setup

setup(
    name="en-lst-solver",
    version="0.1",
    packages=["en-lst-solver"],
    url="https://github.com/MIPT-Virtual-Labs/en-lst-solver.git",
    author="Mikhail Petrov",
    author_email="mikhail.petrov@phystech.edu",
    include_package_data=True,
    package_data={"": ["./bin/*"]},
)
