#! /usr/bin/env python
from rpg_system import CoC_7th
from die import dice_pool

import sys
import traceback
import pandas as pd
from random import randint

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description='Runner for dice system tools')

    misc = parser.add_argument_group('Misc','Miscellaneous')
    exclusive = parser.add_mutually_exclusive_group()

    exclusive.add_argument('-d','--dice-pool',dest='d_note', action='store', help='Roll some dice, e.g. 3d12')
    exclusive.add_argument('-s','--system',dest='system',action='store',help='Specify what ttrpg system to use')

    misc.add_argument('-v','--verbose', dest='verbose', action='store_true', help='Print debugging information')
    misc.add_argument('-t','--test',dest='test',action='store_true',help='Run the test block')

    parser.add_argument('--name', default='', dest='name', action='store', help='Name used as an id in various parts of the code')
    parser.add_argument('--notes', default='', dest='notes', action='store', help='Misc notes about what you are trying to do')

    args = parser.parse_args()

    return args

def main(args):

    results = []

    if args.test:
        # This is just random stuff I'm doing to test what ever code I've just written
        iterations = 100
        dice_table = CoC_7th()

        for i in range(1,iterations):
            results.append(dice_table.skill(skill_level=randint(1,100)))

    elif args.d_note:
        # Lets roll some dice
        dp = dice_pool(d_notation=args.d_note, name=args.name,notes=args.notes)
        results = dp.roll()
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
