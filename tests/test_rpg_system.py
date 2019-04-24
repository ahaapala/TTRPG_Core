from pytest import fixture
from Dice_Statistics.rpg_system import system, cee_lo, GURPS, CoC, CoC_7th, DnD, DnD_5th, Fate

class TestRPGSystem(object):
    d_verbose = True

    def test_system_init(self):
        my_system = system(name='TestRPGSystem', types_of_roles=['test1','test2'], types_of_dice=['3d6','4d8'])
        assert my_system.dice == 7

class TestCeeLo(object):
    d_verbose = True

    def test_ceelo_init(self):
        my_system = cee_lo(name='Test Cee Lo')
        assert my_system.dice == 3

class TestGURPS(object):
    d_verbose = True

    def test_gurps_init(self):
        my_system = GURPS(name='Test GURPS')
        assert my_system.dice == 3

class TestCoC(object):
    d_verbose = True

    def test_coc_init(self):
        my_system = CoC(name='Test CoC')
        assert my_system.dice == 2

class TestCoC7th(object):
    """
        Need additional testing for:
        - Testing for rolls with bonus/penalty dice
    """
    d_verbose = True

    @fixture
    def this_system(self):
        return CoC_7th()

    def test_coc_7th_init(self, this_system):
        assert len(this_system.dice) == 2

    def test_calc_hard_diff(self, this_system):
        assert this_system.calc_hard_diff(50) == 25

    def test_calc_extreme_diff(self, this_system):
        assert this_system.calc_extreme_diff(50) == 10

    def test_skill(self,this_system):
        results = this_system.skill(skill_level=50)
        assert 'Roll Result' in results
        assert 'Skill Level' in results

class TestDnD(object):
    d_verbose = True

    def test_dnd_init(self):
        my_system = DnD(name='Test DnD')
        assert my_system.dice == 1

class TestDnD5th(object):
    d_verbose = True

    @fixture
    def my_system(self):
        return DnD_5th(name='Test DnD 5th')

    def test_dnd_5th_init(self, my_system):
        assert my_system.dice == 1

    def test_saving_throw(self, my_system):
        result = my_system.saving_throw(attribute='Strength',DC=13,modifiers=['3'])
        assert result['Result'] == 'Success' or result['Result'] == 'Failure'

class TestFate(object):
    d_verbose = True

    @fixture
    def my_system(self):
        return Fate(name='Test Fate')

    def test_fate_init(self, my_system):
        assert my_system.dice == 4

    def test_skill(self, my_system):
        result = my_system.skill(skill_name='Test', skill_level=3)
        assert isinstance(result,int)
        assert result < 100 and result > -100
