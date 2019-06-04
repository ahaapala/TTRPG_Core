from random import randint
from utilities import parse_d_notation
from datetime import datetime

"""
    NOTES:
        - Might want to add some logic to manage roll "memory" so it doesn't get unmanageble over time
        - 
"""

class die:
    """
        An individual die.  Needs to keep track of what kind it is, how many sides, should be rollable, and 
        keeps a history of its results.
    """

    verbose = False

    def __init__(self, sides = 6, d_type = "polyhedral",notes = "", verbose = False):
        print('__init__ die.py: ') if self.verbose else None
        self.sides    = sides
        self.die_type = d_type
        self.notes = notes
        self.results = []
        self.verbose = verbose

    def __str__(self):
        return '{"sides":'+str(self.sides)+', "die_type":'+str(self.die_type)+', "notes":'+str(self.notes)+'}'

    def __eq__(self, other):
        if self.result['Result']:
            return self.result['Result'] == other
        else:
            raise Exception('Die has no results yet.  Unable to compare __eq__')

    def __gt__(self, other):
        if self.resul['Result']:
            return self.result['Result'] > other
        else:
            raise Exception('Die has no results yet.  Unable to compare __gt__')

    def get_sides(self):
        return self.sides

    def get_type(self):
        return self.die_type

    def roll(self):
        """
            Roll the die and store the results
        """
        self.result = {}
        rando = randint(1,int(self.sides))
        dt_stamp = str(datetime.now())
        self.result = {'Result': rando,
                       'Date_Time': dt_stamp}
        self.results.append(self.result)

        return self.result

class fudge_die(die):
    """
        Fudge dice are d6s used in 2-pair or 4f.  Their sides only show +, -, or <blank> so while
        it's really just rolling 4d6 the results need to be interpretted.  There's three different, but
        equivalent, ways a 1d6 can be mapped.  
    """
    mappings = {'a' : [1,-1,-1,0,1,0],     # Fudge dice have 3 ways they can be mapped to a d6
                'b' : [-1,-1,1,0,1,0],     # They should be statistically the same
                'c' : [-1,0,-1,1,1,0],
                '-1': "-",
                '0' : " ",
                '1' : "+"}  

    def __init__(self,mapping='a', notes="", verbose = False):
        self.mapping = mapping
        self.sides = 6
        super().__init__(d_type="fudge",notes=notes,verbose=verbose)

    def roll(self):
        result = super().roll()
        fudge_result = self.interpret(result['Result'])
        self.result = {'Result': fudge_result,
                       'Date_Time': result['Date_Time']}

        self.results.append(self.result)
        return self.result
        
    def interpret(self, side):
        return self.mappings[str(self.mappings[self.mapping][int(side-1)])]

class planer_die(die):
    """
        This kind of die is actually for MtG planechase
        It determines if you move onto another plane, get the chaos effect, or do nothing
    """

    mappings = {'1': "Chaos",
                '2': "",
                '3': "",
                '4': "",
                '5': "",
                '6': "Plane"}

    def __init__(self, notes="",verbose=False):
        self.sides = 6
        super().__init__(d_type='planer',notes=notes,verbose=verbose)

    def roll(self):
        result = super().roll()
        planer_result = self.interpret(result['Result'])
        self.result = {'Result': planer_result,
                       'Date_Time': result['Date_Time']}

        self.results.append(self.result)
        return self.result

    def interpret(self, roll):
        return self.mappings[str(roll)]

class dice_pool():
    """
        - Do I want to add reroll functionality or something to help 
        deal with bonus/penalty dicei (present in both CoC and D&D 5th)?
    """

    verbose = False

    def __init__(self, d_notation=[], name="NAME", notes="", verbose = False):
        """
            Should probably have an auto-generated/informative name default 
        """
        print('dice_pool __init__: '+d_notation) if self.verbose else None
        self.dice = []
        self.name = name
        self.d_note = d_notation
        self.d_note_parsed = []
        self.notes = notes
        self.verbose = verbose
        self.__get_dice_pool(self.d_note)
        self.results = []

    def __get_dice_pool(self,d_note):
        """
            This is a "private" method to instantiate the dice from dice notation
        """
        self.dice = []

        if isinstance(d_note,list):
            for d in d_note:
                if isinstance(d,die):
                    self.dice.append(d)
                else:
                    # Assume it's a string 
                    self.d_note_parsed.append(parse_d_notation(d))
        else:
            if isinstance(d_note,die):
                self.dice.append(d_note)
            else:
                self.d_note_parsed.append(parse_d_notation(d_note))

        print(str(self.d_note_parsed)) if self.verbose else None

        for d in self.d_note_parsed:
            print(d)
            for n in range(0,d['Number_of_Dice']):
                if d['Die_Type'] == 'polyhedral':
                    self.dice.append(die(sides=d['Number_of_Sides']))
                elif d['Die_Type'] == 'fudge':
                    self.dice.append(fudge_die())


    def __lt__(self, other):
        length = len(self.dice)

        if isinstance(other,int):
            return length < other
        elif isinstance(other,str):
            return length < int(other)
        elif isinstance(other,dice_pool):
            return length < len(other.dice)
        else:
            return length < len(other.dice)

    def __gt__(self, other):
        length = len(self.dice)
        print('in __gt__')
        if isinstance(other,int):
            print('isinstance of int '+str(length)+'>'+str(other))
            return length > other
        elif isinstance(other,str):
            return length > int(other)
        elif isinstance(other,dice_pool):
            return length > len(other.dice)
        else:
            return length > len(other.dice)

    def __eq__(self,other):
        length = len(self.dice)

        if isinstance(other,int):
            return length == other
        elif isinstance(other, str):
            return length == int(other)
        elif isinstance(other,dice_pool):
            return length == len(other.dice)
        else:
            return length == len(other.dice)

    def __str__(self):
        return str(self.name+','+str(self.d_note)+','+self.notes+','+str(self.dice))

    def __len__(self):
        return len(self.dice)

    def roll(self):
        """
            Roll all the dice in the pool and record the results
        """
        self.result = {}
        temp_result = {}
        temp_results = []

        temp_results.append({'Name':self.name,'Notation': self.d_note, 'Notes': self.notes})

        print('Dice_Pool:'+str(self.dice)) if self.verbose else None

        for d in self.dice:
            temp_result = d.roll()
            print(temp_result) if self.verbose else None
            temp_results.append({'Results': temp_result['Result'], 'Date_Time': temp_result['Date_Time']})

        self.result = temp_results
        self.results.append(self.result)

        return temp_results

    def add_to_pool(self, dice):
        """
            Add dice to the established pool
            Can accept either d-notation or a die object or a mixed list
        """
        if isinstance(dice,list):
            # We have a list of something
            for d in dice:
                if isinstance(d,die):
                   # It's a die object, add to the pool
                   self.dice.append(d.copy())
                elif isinstance(d,str):
                    self.__get_dice_pool(d)    # This method appends new dice so nothing further needs to be done
                else:
                    # Not sure what this is a list of 
                    raise(Exception('Not sure what is being passed to add_to_pool'))

        elif isinstance(dice, die):
            # This is an externally instantiated die
            self.dice.append(dice)
            
        elif isinstance(dice,str):
            # Assume this to be d-notation
            self.__get_dice_pool(dice)
        else:
            raise(Exception('Note sure what was passed to add_to_pool'))

    def list_pool(self):
        # I need to specify the __repr__ method for die class
        for d in range(0,len(self.dice)):
            print('Index: '+str(d)+' Die: '+str(self.dice[d])) if self.verbose else None

        return self.dice

    def remove_from_pool(self,index):
        """
            This kinda needs to be used with list_pool to know what index to pass in.
        """
        obj = self.dice[index]
        self.dice.remove(obj)

    def get_sides(self):
        """
            Returns the side(s) of the dice in the pool.  Returns an int if a single type of die.  
            Returns an array if there are multiple types.
        """
        sides = []
        for d in self.dice:
            side = d.get_sides()
            if side not in sides:
                sides.append(side)
        if len(sides) == 1:
            return sides[0]
        else:
            return sides

    def get_results(self):
        """
            Get a shorter result-only summary of the pool result
        """
        temp_array = []
        for d in self.result:
            for k,v in d.items():
                if k == 'Results' :
                    temp_array.append(v)

        return temp_array
