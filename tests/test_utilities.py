import pytest
from Dice_Statistics.utilities import parse_d_notation

class TestUtilities(object):
    """
        Cases To-Write:
        - iterations of malformed dice formats
        - expand supported formats
        - 
    """


    def test_basic_parse_d_notation(self):
        d_string = '3d6'
        parse_result = parse_d_notation(d_string)
        assert parse_result == {'Number_of_Dice':3,
                                'Number_of_Sides':6,
                                'Die_Type':'polyhedral'}

    def test_fudge_parse_d_notation(self):
        d_string = '8f'  # Note only 4 are normally used but the parsing code isn't concerned with that
        parse_result = parse_d_notation(d_string)
        assert parse_result == {'Number_of_Dice':8,
                                'Number_of_Sides': 6,
                                'Die_Type':'fudge'}

    def test_check_exception(self):
        d_string = 'test'
        with pytest.raises(Exception) as not_known:
            parse_results = parse_d_notation(d_string)
            assert 'Unrecognized dice notation' in str(not_known.value)
