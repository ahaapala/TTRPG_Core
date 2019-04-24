from Dice_Statistics.die import die, fudge_die, planer_die, dice_pool
from pytest import fixture

class TestDie(object):
    """
        Should Add:
        - Tests for checking multiple rolls
        - Take advantage of pandas/bokeh?
    """
    d_sides   = 12
    d_type    = 'polyhedral'
    d_notes   = 'Automated TestDie:'
    d_verbose = True

    def test_die(self):
        my_die = die(sides = self.d_sides,
                   d_type  = self.d_type,
                   notes   = self.d_notes+' test_die()',
                   verbose = self.d_verbose)

        assert str(my_die) == '{"sides":'+str(self.d_sides)+', "die_type":'+str(self.d_type)+', "notes":'+str(self.d_notes+' test_die()')+'}'

    def test_die_roll(self):
        my_die = die(sides   = self.d_sides,
                  d_type  = self.d_type,
                  notes   = self.d_notes+' test_die_roll()',
                  verbose = self.d_verbose)
        roll_results = my_die.roll()
        assert roll_results['Result'] <= self.d_sides and roll_results['Result'] >= 1


class TestFudgeDie(object):
    """
        Additional testing
        - Should test every mapping but will just do the A mapping for now
    """
    d_type    = 'fudge'
    d_notes   = 'Automated TestFudgeDie'
    d_verbose = True
    d_sides   = 6

    def test_fudge_die(self):
        my_die = fudge_die(notes   = self.d_notes+' test_fudge_die()',
                           verbose = self.d_verbose)
        assert str(my_die) == '{"sides":'+str(self.d_sides)+', "die_type":'+str(self.d_type)+', "notes":'+str(self.d_notes+' test_fudge_die()')+'}'

    def test_fudge_roll(self):
        my_die = fudge_die(notes   = self.d_notes+' test_fudge_roll()',
                           verbose = self.d_verbose)
        roll_results = my_die.roll()
        result = roll_results['Result']
        assert result == '-' or result == ' ' or result == '+'

    def test_interpret_a(self):
        # For mapping A
        my_die = fudge_die(notes=self.d_notes+' test_interpret_a()',verbose=self.d_verbose)
        assert my_die.interpret(side=1) == '+'
        assert my_die.interpret(side=2) == '-'
        assert my_die.interpret(side=3) == '-'
        assert my_die.interpret(side=4) == ' '
        assert my_die.interpret(side=5) == '+'
        assert my_die.interpret(side=6) == ' '

class TestPlanerDie(object):

    d_notes = 'Automated TestPlanerDie'
    d_verbose = True
    d_sides = 6
    d_type = 'planer'

    def test_planer_die(self):
        my_die = planer_die(notes=self.d_notes+' test_planer_die()',verbose=self.d_verbose)
        assert str(my_die) == '{"sides":'+str(self.d_sides)+', "die_type":'+str(self.d_type)+', "notes":'+str(self.d_notes+' test_planer_die()')+'}'


    def test_planer_roll(self):
        my_die = planer_die(notes=self.d_notes+' test_planer_roll()',verbose=self.d_verbose)
        roll_results = my_die.roll()['Result']
        assert roll_results == "" or roll_results == "Chaos" or roll_results == "Plane"
        

    def test_interpret(self):
        my_die = planer_die(notes=self.d_notes+' test_interpret()',verbose=self.d_verbose)
        assert my_die.interpret(1) == 'Chaos'
        assert my_die.interpret(2) == ''
        assert my_die.interpret(3) == ''
        assert my_die.interpret(4) == ''
        assert my_die.interpret(5) == ''
        assert my_die.interpret(6) == 'Plane'
   

class TestDicePool(object):

    d_notation = ['5d8']
    d_name     = 'Test Pool'
    d_notes    = 'Automated TestDicePool'
    d_verbose  = True

    @fixture 
    def my_pool(self):
        test_pool = dice_pool(d_notation=self.d_notation,
                                    name=self.d_name,
                                   notes=self.d_notes,
                                 verbose=self.d_verbose)
        test_pool.roll()
        return test_pool

    def test_pool(self,my_pool):
        pool_string = str(my_pool)
        assert self.d_name in pool_string
        for i in self.d_notation:
            assert i in pool_string
        assert self.d_notes in pool_string

    def test_pool_roll(self,my_pool):
        results = my_pool.roll()
        assert isinstance(results,list)
        assert len(results) == (len(my_pool.dice)+1)
        for i in results:
            assert isinstance(i,dict)
            assert 'Results' in i or 'Name' in i
        

    def test_add_to_pool(self,my_pool):
        """
            - The add method needs to support mixed dice pools
            - This method supports multiple types as a legit param.  Should
            test for each branch
        """
        old_len = len(my_pool.dice)
        old_d_notation = my_pool.d_note
        new_d_notation = '2d12'
        my_pool.add_to_pool(new_d_notation)
        old_v_new = my_pool > old_len
        assert old_v_new
        

    def test_remove_from_pool(self,my_pool):
        old_len = len(my_pool.dice)
        my_pool.remove_from_pool(2)   # Specify the index of pool.dice[] to remove
        assert old_len > my_pool

    def test_list_pool(self, my_pool):
        # This method also prints the indexes to screen
        dice = my_pool.list_pool()
        assert isinstance(dice,list)
        assert len(dice) == my_pool

    def test_get_results(self, my_pool):
        my_pool.roll()
        short_results = my_pool.get_results()
        assert isinstance(short_results, list)
        assert my_pool == len(short_results)
        assert 'Results' not in short_results
