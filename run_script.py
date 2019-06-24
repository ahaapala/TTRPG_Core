#! /usr/bin/env python
from ttrpg_core.rpg_system import CoC_7th
from ttrpg_core.die import dice_pool

import sys
import traceback
#import pandas as pd
from random import randint
import numpy as np
import matplotlib.pyplot as plt

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description='Runner for dice system tools')

    misc = parser.add_argument_group('Misc','Miscellaneous')
    exclusive = parser.add_mutually_exclusive_group()

    exclusive.add_argument('-d', '--dice-pool', dest='d_note', action='store', help='Roll some dice, e.g. 3d12')
    exclusive.add_argument('-s', '--system', dest='system', action='store', help='Specify what ttrpg system to use')

    misc.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Print debugging information')
    misc.add_argument('-t', '--test', dest='test', action='store_true', help='Run the test block')
    misc.add_argument('-g', '--graph', dest='graph', action='store_true', help='Graph the results of the operation')

    parser.add_argument('--name', default='', dest='name', action='store', help='Name used as an id in various parts of the code')
    parser.add_argument('--notes', default='', dest='notes', action='store', help='Misc notes about what you are trying to do')


    args = parser.parse_args()

    return args

def main(args):

    results = []
    only_results = []

    if args.test:
        # This block is just random stuff I'm doing to test what ever code I've just written
        iterations = 100
        dice_table = CoC_7th()

        for i in range(1,iterations):
            result = dice_table.skill(skill_level=randint(1,100))
            results.append(result)
            only_results.append(result['Roll Result'])

        #print(only_results)
        

        if args.graph:
            narray = np.array(only_results)
            fig, ax = plt.subplots()
            ax.hist(narray, bins=100)
            fig.suptitle('Histogram of Test CoC Rolls')
            ax.set_ylabel('Counts')
            plt.show()
            
    elif args.d_note:
        # Lets roll some dice
        dp = dice_pool(d_notation=args.d_note, name=args.name,notes=args.notes)
        results = dp.roll()
        if args.graph:
            dp_sides = dp.get_sides()
            if isinstance(dp_sides, list):
                print('Multiple dice sizes in pool')
            else:
                narray = np.array(dp.get_results())
                fig, ax = plt.subplots()
                ax.hist(narray, bins=dp_sides)
                fig.suptitle('Histogram of Roll '+str(narray))
                ax.set_ylabel('counts')
                plt.show()
        else:
            print(dp.get_results())

    elif args.system:
        # Parse the systems and generate the correct type of table
        if args.system == 'CoC_7th':
            # Do CoC things
            pass
        elif args.system == 'DnD_5th':
            # Do D&D things
            pass
    else:
        results = "Not a recognized option or argument"

    print(str(results))

    return 0

if __name__ == "__main__":
    try:
        args = parse_args()
        main(args)
    except Exception as e:
        print('Script Error:'+str(e))
        traceback.print_exc()
