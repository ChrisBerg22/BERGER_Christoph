"""Bullseye

Write a proper docstring here such that:
    - if the flag `--seed SEED` is provided, the seed SEED should be used to generate random numbers
    - if the flag `--games GAMES` is provided, the program should run GAMES number of games

Have a look at https://docopt.org on how to do this


Usage: 
    bullseye [--seed=<SEED>] [--games=<GAMES>]
"""


import numpy as np
import random 
import statistics
import math
from docopt import docopt

__version__ = "0.2.0"

def get_opts():
    """get the options passed to the program via docopt

        Returns:
            options (dict): a dictionary with the options
    """
    opts = docopt(__doc__)
    print(opts)
    return opts

def update(x, y, r):
    """Update the radius according to the rules of the game.

    If the hit is on the disk, i.e. :math:`x_i**2+y_i**2 <= r_i**2`, the new radius
    :math:`r_{i+1}` will be the length of the side opposing
    :math:`\sphericalangle O-\left(x,y\right)-B` in the right triangle :math:`\Delta
    O-\left(x,y\right)-B`, where :math:`O` is the origin of the circle,
    :math:`\left(x, y\right)` the position the dart hit and :math:`B` the point
    intersecting the circle and the line perpendicular to
    :math:`\vec{O\left(x,y\right)}`.

    Args:
      x (float): x coordinate of the dart
      y (float): y coordinate of the dart
      r (float): the radius of the dart board

    Returns:
        (float): the new radius
    """
    
    try:
        r = math.sqrt(r**2 - (x**2 + y**2))
        return r
    except:
        raise AssertionError

def game():
    """One game of hitting the dart board until we miss

    First, we set the radius to 1 and the score to 0.
    Then, as long as we hit the board, add 1 to the scores for each dart thrown, throw to a random
    (x,y) coordinate, update the new radius or end the game if we missed.
    Finally return the number of scores.

    Returns:
      score (int): the number of darts thrown.
    """
    r = 1
    score = 1
    it = 0

    while True and it <= 1e5:
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        if (x**2 + y**2) <= r**2:
            r = update(x,y,r)
            score += 1
            continue
        else:
            break
    return score

def main(opts, games):
    """for a given number of games, record the scores, then return the mean and
    of the scores
    If the options contain a seed for the random number generartor, pass this seed to numpy
    If the options contain a number of games to be played, play the game this many times

    Args:
      games (int): the number of games to play.

    Returns:
      mean (float):  the mean value of the scores
    """
    #if opts["--seed"]:
    #    random_seed = int(opts["--seed"])
     #   random.seed(random_seed)
    #elif opts["--games"]:
     #   games = int(opts["--games"])
    try:
        random_seed = int(opts["--seed"])
        random.seed(random_seed)
        games = int(opts["--games"])
    except TypeError:
        print("Note: You can specify all --flags")
    

    total_score = []
    start = 1
    while start <= games:
        endscore = game()
        total_score.append(endscore)
        start += 1
    mean = statistics.mean(total_score)
    return mean 


if __name__ == "__main__":
    """This code executes when the program is run from the command line"""
    opts = get_opts()
    mean = main(opts, 100000)
    print(f"exp(pi/4) approx equal to {mean}")
