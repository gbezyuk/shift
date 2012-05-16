"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Model tests
Subpart: Cart tests
"""
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.contrib.sessions.models import Session
from django.test import TestCase
from django.test.client import Client
from doppler.shift.catalog.models import MULTIPLE_PRICES
from doppler.shift.checkout.models import Cart
from ..factories import UserFactory, ProductFactory, PriceFactory

class CartTestCase(TestCase):
    """
    Tests for Cart model
    """
    def setUp(self):
        """
        Initialization
        """
        self.client = Client()
        self.request = HttpRequest()
        self.request.session = self.client.session
        self.request.user = AnonymousUser()

    def test_cart_exists_for_unauthorized_user(self):
        """
        Testing cart existance for unauthorized user
        """
        self.assertEqual(Cart.get_cart(self.request), None)
        self.assertEqual(len(Cart.get_cart_items(self.request)), 0)
        self.assertNotEqual(Cart.get_cart(self.request, create_if_not_exist=True), None)

    def test_cart_exists_for_authorized_user(self):
        """
        Testing cart existance for unauthorized user
        """
        self.request.user = UserFactory()
        self.test_cart_exists_for_unauthorized_user()

    def test_adding_product_to_cart_by_unauthorized_user(self):
        """
        Testing adding product to cart by unauthorized user
        """
        self.assertEqual(len(Cart.get_cart_items(self.request)), 0)
        sample_product = ProductFactory()
        another_product = ProductFactory()
        cart = Cart.get_cart(self.request, create_if_not_exist=True)
        self.assertRaises(AssertionError, cart.insert_item, sample_product, 1)
        self.assertEqual(len(Cart.get_cart_items(self.request)), 0)
        if MULTIPLE_PRICES:
            sample_product.prices.add(PriceFactory())
            another_product.prices.add(PriceFactory())
        self.assertRaises(AssertionError, cart.insert_item, sample_product, 0)
        cart.insert_item(sample_product, 1)
        self.assertEqual(len(Cart.get_cart_items(self.request)), 1)
        cart_item_added = Cart.get_cart_items(self.request)[0]
        self.assertEqual(cart_item_added.product, sample_product)
        self.assertEqual(cart_item_added.quantity, 1)
        cart.insert_item(sample_product, 1)
        self.assertEqual(len(Cart.get_cart_items(self.request)), 1)
        cart_item_added = Cart.get_cart_items(self.request)[0]
        self.assertEqual(cart_item_added.product, sample_product)
        self.assertEqual(cart_item_added.quantity, 2)
        cart.insert_item(another_product, 1)
        self.assertEqual(len(Cart.get_cart_items(self.request)), 2)
        cart_item_added = Cart.get_cart_items(self.request)[0]
        self.assertEqual(cart_item_added.product, sample_product)
        self.assertEqual(cart_item_added.quantity, 2)
        cart_item_added = Cart.get_cart_items(self.request)[1]
        self.assertEqual(cart_item_added.product, another_product)
        self.assertEqual(cart_item_added.quantity, 1)

    def test_adding_product_to_cart_by_authorized_user(self):
        """
        Testing adding product to cart by authorized user
        """
        self.request.user = UserFactory()
        self.test_adding_product_to_cart_by_unauthorized_user()

    def test_changing_cart_product_quantity_by_unauthorized_user(self):
        """
        Testing changing cart product quantity by unauthorized user
        """
        self.assertEqual(len(Cart.get_cart_items(self.request)), 0)
        sample_product = ProductFactory()
        cart = Cart.get_cart(self.request, create_if_not_exist=True)
        if MULTIPLE_PRICES:
            sample_product.prices.add(PriceFactory())
        cart.insert_item(sample_product, 1)
        cart_item_added = Cart.get_cart_items(self.request)[0]
        self.assertEqual(cart_item_added.product, sample_product)
        self.assertEqual(cart_item_added.quantity, 1)
        self.assertRaises(AssertionError, cart.update_quantity, sample_product, 0)
        cart.update_quantity(sample_product, 10)
        cart_item_added = Cart.get_cart_items(self.request)[0]
        self.assertEqual(cart_item_added.product, sample_product)
        self.assertEqual(cart_item_added.quantity, 10)

    def test_changing_cart_product_quantity_by_authorized_user(self):
        """
        Testing changing cart product quantity by authorized user
        """
        self.request.user = UserFactory()
        self.test_changing_cart_product_quantity_by_unauthorized_user()
#
#    def test_removing_cart_product_by_authorized_user(self):
#        """
#        Testing removing cart product by authorized user
#        """
#        raise NotImplementedError
#
#    def test_removing_cart_product_by_unauthorized_user(self):
#        """
#        Testing removing cart product by unauthorized user
#        """
#        raise NotImplementedError
#
#    def test_clear_cart_by_authorized_user(self):
#        """
#        Testing clearing cart by authorized user
#        """
#        raise NotImplementedError
#
#    def test_clear_cart_by_unauthorized_user(self):
#        """
#        Testing clearing cart by unauthorized user
#        """
#        raise NotImplementedError
#
#    def test_cart_item_total_price_calculation(self):
#        """
#        Testing cart item total price calculation
#        """
#        raise NotImplementedError
#
#    def test_cart_total_price_calculation(self):
#        """
#        Testing cart total price calculation
#        """
#        raise NotImplementedError
#
#    def test_cart_total_quantity_calculation(self):
#        """
#        Testing cart total quantity calculation
#        """
#        raise NotImplementedError
#
#    def test_cart_distinct_quantity_calculation(self):
#        """
#        Testing cart distinct quantity calculation
#        """
#        raise NotImplementedError