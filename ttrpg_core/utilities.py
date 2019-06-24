def parse_d_notation(d_string):
    """

        Takes a system agnostic d-notation string and breaks it out it's respective 
        parts.  This breakdown can be used to instantiate dice-pools

        e.g. 3d6 == 3 six-sided dice 
        4f  == 4 fudge/fate dice
    """

    if 'd' in d_string:
        # Standard notation
        num_of_dice, sides_of_dice = d_string.split('d')
        if num_of_dice:
            type_of_dice = 'polyhedral'
            return {'Number_of_Dice': int(num_of_dice), 
                   'Number_of_Sides': int(sides_of_dice), 
                          'Die_Type': type_of_dice}
        else:
            raise Exception('Number of dice not specified '+str(d_string))

    elif 'f' in d_string:
        # Fudge dice notation
        # Ignores trailing characters
        num_of_dice = d_string.split('f')[0]
        sides_of_dice = 6
        type_of_dice = 'fudge'
        return {'Number_of_Dice': int(num_of_dice), 
               'Number_of_Sides': int(sides_of_dice), 
                      'Die_Type': type_of_dice}
    elif isinstance(d_string, list):
        temp = []
        for d in d_string:
            temp.append(parse_d_notation(d))
        return temp
    else:
        # Format not recognized
        raise Exception('Unrecognized dice notation')

