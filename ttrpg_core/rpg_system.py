from ttrpg_core.die import die, fudge_die, dice_pool
"""
    3-tier hierarchy of game objects.
    Individual systems/rolls are implemented here.
"""


class system:
    """
        Generic base class.  System specific implementation should be left to
        children.  Should hold onto all meta info and help coordinate
        the context of the dice rolls
    """

    def __init__(self, name='', types_of_roles=[], types_of_dice=[]):
        self.name = name
        self.types_of_roles = types_of_roles   # Types of rolls in the system
        self.types_of_dice = types_of_dice     # Types of dice the system uses
        self.dice = dice_pool(types_of_dice)   # Dice pool


class cee_lo(system):
    """
        Experimental system based on the game of cee-lo
    """

    def __init__(self, name='', types_of_roles=['action'], types_of_dice=['3d6']):
        super().__init__(name, types_of_roles, types_of_dice)


class GURPS(system):
    """
        Generic Universal Roleplaying System
        - Runs with 3d6 and seems good to model and compare to the cee-lo adaptation I'm
        tinkering with.
    """

    def __init__(self, name='', types_of_roles=['success', 'default', 'contest'], types_of_dice=['3d6']):
        super().__init__(name, types_of_roles, types_of_dice)


class CoC(system):
    # Base CoC class

    def __init__(self, name='', types_of_roles=['attack', 'skill', 'chase', 'opposed'], types_of_dice=[]):
        types_of_dice = [die(sides=10, notes='tens'),
                         die(sides=10, notes='ones')]
        super().__init__(name, types_of_roles, types_of_dice)


class CoC_7th(CoC):
    """
        - It is faithful to the rules but seems like it can be better organized
    """

    def __init__(self, name='Call of Cthulhu 7th Edition'):
        super().__init__(name=name)

    def calc_hard_diff(self, skill_level=0):
        return skill_level / 2

    def calc_extreme_diff(self, skill_level=0):
        return skill_level / 5

    def skill(self, skill_level=0, bonus_die=0, penalty_die=0):

        additional_dice = dice_pool()

        if bonus_die > 0:
            for i in bonus_die:
                additional_dice.add_to_pool(die(sides=10, notes='bonus die'))
        elif penalty_die > 0:
            for i in penaly_die:
                additional_dice.add_to_pool(die(sides=10, notes='penalty die'))

        self.dice.roll()
        additional_dice.roll()

        for d in self.dice.list_pool():
            if 'tens' in d.notes:
                tens = d.result['Result']
            if 'ones' in d.notes:
                ones = d.result['Result']

        add_dice_len = len(additional_dice)

        if add_dice_len > 0 and add_dice_len < 2:
            for d in additional_dice.dice:
                if 'bonus' in additional_die.notes:
                    # Choose the greater of the tens rolls
                    if d > tens:
                        tens = add_die
                else:
                    # It's a penalty die, chose the lesser tens roll
                    if d < tens:
                        tens = add_die

        # We've handled penaly/bonus dice so time to compare to the skill rating and determine degree of success
        roll_result = (tens * 10) + ones

        if tens == 10 and ones == 10:
            roll_result = 100
        elif tens == 10 and ones < 10:
            roll_result = ones

        roll_summary = {'Roll Result': roll_result,
                        'Skill Level': skill_level,
                        'Penalty Dice': penalty_die,
                        'Bonus Dice': bonus_die}

        if roll_result <= skill_level:
            # it's a success, determine success level
            if roll_result <= self.calc_extreme_diff(skill_level):
                if roll_result == 1:
                    roll_summary['Result'] = 'Critical Success'
                else:
                    roll_summary['Result'] = 'Extreme Success'
            elif roll_result <= self.calc_hard_diff(skill_level):
                roll_summary['Result'] = 'Hard Success'
            else:
                roll_summary['Result'] = 'Regular Success'
        else:
            # It's a failure, check for fumble
            if skill_level > 50:
                if roll_result == 100:
                    roll_summary['Result'] = 'Fumble'
            else:
                if roll_result >= 96:
                    roll_summary['Result'] = 'Fumble'
                else:
                    roll_summary['Result'] = 'Failure'

        return roll_summary


class DnD(system):

    def __init__(self, name='', types_of_roles=['attack', 'skill', 'save'], types_of_dice=['1d20']):
        super().__init__(name, types_of_roles, types_of_dice)


class DnD_5th(DnD):

    def __init__(self, name='Dungeons and Dragons 5th Edition'):
        super().__init__(name=name)

    def saving_throw(self, attribute='', DC=10, modifiers=[]):
        roll_result = self.dice.roll()
        result_summary = {'Result': 'Failure'}

        for i in roll_result:
            if 'Results' in i:
                temp_result = i['Results']

                for m in modifiers:
                    temp_result = int(temp_result) + int(m)

                if temp_result >= DC:
                    result_summary = {'Result': 'Success'}

        return result_summary


class Fate(system):
    # Here's some pubished stats for fudge dice rolls
    # https://fate-srd.com/fate-core/taking-action-dice-ladder#the-math-behind-the-dicee
    ladder = {-2: 'Terrible',
              -1: 'Poor',
               0: 'Mediocre',
               1: 'Average',
               2: 'Fair',
               3: 'Good',
               4: 'Great',
               5: 'Superb',
               6: 'Fantastic',
               7: 'Epic',
               8: 'Legendary'}

    def __init__(self, name='', types_of_roles=['skill'], types_of_dice=['4f']):
        self.name = name
        self.types_of_roles = types_of_roles
        self.types_of_dice = types_of_dice
        super().__init__(name=name, types_of_roles=types_of_roles, types_of_dice=types_of_dice)

    def skill(self, skill_name='generic', skill_level=0):

        roll_sum = 0 + skill_level

        temp_results = self.dice.roll()

        for r in temp_results:
            print(r)
            if 'Results' in r:
                if r['Results'] == '+':
                    roll_sum = roll_sum + 1
                elif r['Results'] == ' ':
                    pass
                elif r['Results'] == '-':
                    roll_sum = roll_sum - 1
                else:
                    raise Exception('Unrecognized result in Fate.skill()')

        return roll_sum
