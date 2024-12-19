from decimal import Decimal
import time
from functools import wraps


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def rate_limiter(seconds=1):
    """
    Декоратор для ограничения частоты вызовов функции.

    :param seconds: Время в секундах, которое должно пройти между вызовами функции.
    """

    def decorator(func):
        last_called = [0.0]  # Используем список для хранения времени последнего вызова

        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            if current_time - last_called[0] >= seconds:
                last_called[0] = current_time
                return func(*args, **kwargs)
            else:
                print(f"Функция {func.__name__} вызвана слишком часто. Пожалуйста, подождите.")

        return wrapper

    return decorator


class DecStr(Decimal):
    def __init__(self, number):
        self.number = Decimal(number)

    def __str__(self):
        return f"{self.number.__str__()}"


class CurrenciesLst(metaclass=Singleton):
    def __init__(self):
        self.cur_lst: dict = {}
        self._ids_lst: list = []

    def set_ids(self, ids_lst):
        self._ids_lst = ids_lst

    @rate_limiter(seconds=1)
    def get_currencies(self) -> list:
        import requests
        from xml.etree import ElementTree as ET

        cur_res_str = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        result = []

        root = ET.fromstring(cur_res_str.content)
        valutes = root.findall("Valute")
        double_of_ids = self._ids_lst.copy()

        for _v in valutes:
            valute_id = _v.get('ID')
            valute = {}
            if str(valute_id) in double_of_ids:
                valute_cur_name, valute_cur_val = _v.find('Name').text, _v.find('Value').text
                valute_cur_val = DecStr(valute_cur_val.replace(',', '.'))
                valute_nominal = int(_v.find('Nominal').text)
                valute_charcode = _v.find('CharCode').text
                if valute_nominal != 1:
                    valute[valute_charcode] = (valute_cur_name, valute_cur_val.__str__(), valute_nominal)
                else:
                    valute[valute_charcode] = (valute_cur_name, valute_cur_val.__str__())
                result.append(valute)
                self.cur_lst.__setitem__(valute_cur_name, valute_cur_val)
                double_of_ids.remove(str(valute_id))
        for id in double_of_ids:
            invalid_id = {f'{id}': None}
            result.append(invalid_id)
        return result

    def __del__(self):
        print('Уничтожение произошло.')

    def visualize_currencies(self):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        currencies = []
        values = []
        for name in self.cur_lst:
            currencies.append(name)
            values.append(self.cur_lst.__getitem__(name))

        plt.scatter(currencies, values)
        plt.title('Курсы')
        plt.savefig('currencies.jpg')

        plt.show()


if __name__ == '__main__':
    enter_codes = ['R01035', 'R01335', 'R01700J']
    res = CurrenciesLst()
    res._ids_lst = enter_codes
    print(res.get_currencies())
    res.get_currencies() # будет проигнорировано, потому что запрос отправлен меньше, чем через секунду
    time.sleep(1)
    print(res.get_currencies())
    res.visualize_currencies()
    two = CurrenciesLst()
    if res is two:
        print('Singleton is working!')
    del res

