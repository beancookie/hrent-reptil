import datetime
import unittest

from HrentReptile.utils.str_util import get_date, get_int, get_city_from_url


class MyTest(unittest.TestCase):  # 继承unittest.TestCase
    def test_get_date(self):
        now = datetime.datetime.now()
        self.assertEqual((now - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), get_date('1天前'))
        self.assertEqual((now - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"), get_date('2小时前'))
        self.assertEqual((now - datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"), get_date('3分钟前'))

    def test_get_int(self):
        self.assertEqual(1234, get_int('1234', True))
        self.assertEqual(1234, get_int('1234', False))
        self.assertEqual(-1, get_int('123a', True))
        self.assertEqual(123, get_int('123a', False))
        self.assertEqual(-1, get_int('va', False))

    def test_get_city_from_url(self):
        url = 'http://nj.ziroom.com/z/vr/61868811.html'
        self.assertEqual('南京', get_city_from_url(url))
        self.assertEqual('', get_city_from_url(''))

