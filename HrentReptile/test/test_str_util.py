import datetime
import unittest

from HrentReptile.utils.str_util import get_date


class MyTest(unittest.TestCase):  # 继承unittest.TestCase
    def test_get_date(self):
        now = datetime.datetime.now()
        self.assertEqual((now - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), get_date('1天前'))
        self.assertEqual((now - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"), get_date('2小时前'))
        self.assertEqual((now - datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"), get_date('3分钟前'))
