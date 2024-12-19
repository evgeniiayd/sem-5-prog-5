import unittest
from main import CurrenciesLst


class TestCur(unittest.TestCase):
    """Тест для класса CurrienciesLst"""

    def test_ids(self):
        rst = CurrenciesLst()
        rst._ids_lst = ['R999', 'R01010']
        self.assertEqual(rst.get_currencies(), [{'AUD': ('Австралийский доллар', '64.3897')}, {'R999': None}])


