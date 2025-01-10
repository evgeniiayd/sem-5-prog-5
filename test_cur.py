import unittest
from main import CurrenciesLst


class TestCur(unittest.TestCase):
    """Тест для класса CurrienciesLst"""
    def setUp(self):
        self.rst = CurrenciesLst()
        self.rst._ids_lst = ['R999', 'R01010']

    def test_ids(self):
        first_currency = self.rst.get_currencies()[0]
        self.assertIn('AUD', first_currency)

    def test_singleton_property(self):
        """Проверяем, что два экземпляра класса CurrenciesLst - это один и тот же объект"""
        instance1 = CurrenciesLst()
        instance2 = CurrenciesLst()
        self.assertIs(instance1, instance2, "Должны быть одинаковыми экземплярами")

    def test_singleton_unique_id_list(self):
        # Проверяем, что изменения в одном экземпляре отражаются в другом экземпляре
        instance1 = CurrenciesLst()
        instance1._ids_lst = ['R999', 'R01010']

        instance2 = CurrenciesLst()
        self.assertEqual(instance2._ids_lst, ['R999', 'R01010'], "Списки идентификаторов должны совпадать")

    def test_singleton_initialization(self):
        # Проверяем, что инициализация происходит только один раз
        instance1 = CurrenciesLst()
        instance1._ids_lst = ['R999']

        instance2 = CurrenciesLst()
        self.assertEqual(instance2._ids_lst, ['R999'], "Инициализация должна произойти только один раз")




