""" simulation mode helpers """
from contextlib import contextmanager

from base import green_print, log_exception


@contextmanager
def simulation_wall(simulation):
    """" context manager to print simulate mode message """
    simulation_mode_disclaimer(simulation)
    with log_exception():
        yield
    simulation_mode_disclaimer(simulation)


def simulation_mode_disclaimer(simulation):
    """ Prints simulation mode disclaimer """
    if simulation:
        green_print("****************************************************")
        green_print("* This script is been executed in Simulation MODE. *")
        green_print("*                                                  *")
        green_print("* The gcloud commands used in the script will be   *")
        green_print("* generated and printed on the shell but they will *")
        green_print("* NOT be executed.                                 *")
        green_print("*                                                  *")
        green_print("* To actually execute the script, run it with the  *")
        green_print("* flag --no-simulation                             *")
        green_print("****************************************************")
