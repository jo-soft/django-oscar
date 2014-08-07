from decimal import Decimal as D
from itertools import product
from django.test import TestCase

from oscar.core.prices import Price


class TestPriceObject(TestCase):

    def test_can_be_instantiated_with_tax_amount(self):
        price = Price('USD', D('10.00'), tax=D('2.00'))
        self.assertTrue(price.is_tax_known)
        self.assertEqual(D('12.00'), price.incl_tax)

    def test_can_have_tax_set_later(self):
        price = Price('USD', D('10.00'))
        price.tax = D('2.00')
        self.assertEqual(D('12.00'), price.incl_tax)

    def test_price_equals_reflexivity(self):
        for price in (
            Price('USD', incl_tax=D('10.00')), 
            Price('USD', incl_tax=D('10.00'), tax=D('2.00')),
            Price('USD', icl_tax=D('10.00'), excl_tax=D('8.00')),
            ):
            self.assertEqual(price, price)

    def test_price_equals_formats(self):
        price1 = Price('USD', incl_tax=D('10.00'), tax=D('2.00'))
        price2 = Price('USD', icl_tax=D('10.00'), excl_tax=D('8.00'))
        self.assertEqual(price1, price2)


    def test_price_equals_currency_matters(self):
        price1 = Price('EUR', incl_tax=D('10.00'), tax=D('2.00'))
        price2 = Price('USD', incl_tax=D('10.00'), tax=D('2.00'))
        self.assertNotEquals(price1, price2)
        
    def test_price_equals_transitivity(self):
        prices = (
            Price('EUR', incl_tax=D('10.00'), tax=D('2.00')),
            Price('USD', incl_tax=D('10.00'), tax=D('2.00')),
            Price('USD', icl_tax=D('10.00'), excl_tax=D('8.00')),
            Price('USD', icl_tax=D('10.00'), tax=D('8.00'))
            )
        prices_product = product(prices, prices)
        for price1, price2 in prices_product:
            result1 = price1 == price2
            result2 = price2 == price1
            self.assertEqual(result1, result2)
