"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Model tests
Subpart: Cart tests
"""
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import TestCase
from django.test.client import Client
from doppler.shift.catalog.models import MULTIPLE_PRICES
from doppler.shift.checkout.models import Cart, CartItem
from ..factories import UserFactory, ProductFactory, PriceFactory, CartItemFactory, CartFactory

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
        self.assertEqual(len(Cart.get_items(self.request)), 0)
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
        self.assertEqual(len(Cart.get_items(self.request)), 0)
        sample_product = ProductFactory()
        another_product = ProductFactory()
        cart = Cart.get_cart(self.request, create_if_not_exist=True)
        self.assertRaises(AssertionError, cart.insert_item, sample_product, 1)
        self.assertEqual(len(Cart.get_items(self.request)), 0)
        if MULTIPLE_PRICES:
            PriceFactory(product=sample_product)
            PriceFactory(product=another_product)
        self.assertRaises(AssertionError, cart.insert_item, sample_product, 0)
        cart.insert_item(sample_product, 1)
        self.assertEqual(len(Cart.get_items(self.request)), 1)
        cart_item_added = Cart.get_items(self.request)[0]
        self.assertEqual(cart_item_added.product, sample_product)
        self.assertEqual(cart_item_added.quantity, 1)
        cart.insert_item(sample_product, 1)
        self.assertEqual(len(Cart.get_items(self.request)), 1)
        cart_item_added = Cart.get_items(self.request)[0]
        self.assertEqual(cart_item_added.product, sample_product)
        self.assertEqual(cart_item_added.quantity, 2)
        cart.insert_item(another_product, 1)
        self.assertEqual(len(Cart.get_items(self.request)), 2)
        cart_item_added = Cart.get_items(self.request)[0]
        self.assertEqual(cart_item_added.product, sample_product)
        self.assertEqual(cart_item_added.quantity, 2)
        cart_item_added = Cart.get_items(self.request)[1]
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
        self.assertEqual(len(Cart.get_items(self.request)), 0)
        sample_product = ProductFactory()
        another_product = ProductFactory()
        cart = Cart.get_cart(self.request, create_if_not_exist=True)
        if MULTIPLE_PRICES:
            PriceFactory(product=sample_product)
        cart.insert_item(sample_product, 1)
        cart_item_added = Cart.get_items(self.request)[0]
        self.assertEqual(cart_item_added.product, sample_product)
        self.assertEqual(cart_item_added.quantity, 1)
        self.assertRaises(AssertionError, cart.update_quantity, sample_product, 0)
        self.assertRaises(AssertionError, cart.update_quantity, another_product, 0)
        self.assertRaises(AssertionError, cart.update_quantity, another_product, 1)
        if MULTIPLE_PRICES:
            PriceFactory(product=another_product)
        self.assertRaises(AssertionError, cart.update_quantity, another_product, 0)
        self.assertRaises(CartItem.DoesNotExist, cart.update_quantity, another_product, 1)
        cart.update_quantity(sample_product, 10)
        cart_item_added = Cart.get_items(self.request)[0]
        self.assertEqual(cart_item_added.product, sample_product)
        self.assertEqual(cart_item_added.quantity, 10)

    def test_changing_cart_product_quantity_by_authorized_user(self):
        """
        Testing changing cart product quantity by authorized user
        """
        self.request.user = UserFactory()
        self.test_changing_cart_product_quantity_by_unauthorized_user()

    def test_removing_cart_product_by_unauthorized_user(self):
        """
        Testing removing cart product by authorized user
        """
        self.assertEqual(len(Cart.get_items(self.request)), 0)
        sample_product = ProductFactory()
        another_product = ProductFactory()
        cart = Cart.get_cart(self.request, create_if_not_exist=True)
        if MULTIPLE_PRICES:
            PriceFactory(product=sample_product)
        cart.insert_item(sample_product, 1)
        cart_item_added = Cart.get_items(self.request)[0]
        self.assertEqual(cart_item_added.product, sample_product)
        self.assertEqual(cart_item_added.quantity, 1)
        cart.remove_product(another_product)#shouldn't raise any exception
        cart.remove_product(sample_product)
        self.assertEqual(len(Cart.get_items(self.request)), 0)

    def test_removing_cart_product_by_authorized_user(self):
        """
        Testing removing cart product by unauthorized user
        """
        self.request.user = UserFactory()
        self.test_removing_cart_product_by_unauthorized_user()

    def test_clear_cart_by_authorized_user(self):
        """
        Testing clearing cart by authorized user
        """
        self.assertEqual(len(Cart.get_items(self.request)), 0)
        sample_product = ProductFactory()
        another_product = ProductFactory()
        cart = Cart.get_cart(self.request, create_if_not_exist=True)
        if MULTIPLE_PRICES:
            PriceFactory(product=sample_product)
        cart.insert_item(sample_product, 1)
        cart_item_added = Cart.get_items(self.request)[0]
        self.assertEqual(cart_item_added.product, sample_product)
        self.assertEqual(cart_item_added.quantity, 1)
        cart.clear()
        self.assertEqual(len(Cart.get_items(self.request)), 0)

    def test_clear_cart_by_unauthorized_user(self):
        """
        Testing clearing cart by unauthorized user
        """
        self.request.user = UserFactory()
        self.test_removing_cart_product_by_unauthorized_user()

    def test_cart_item_total_price_calculation(self):
        """
        Testing cart item total price calculation
        """
        sample_product = ProductFactory()
        cart = Cart.get_cart(self.request, create_if_not_exist=True)
        if MULTIPLE_PRICES:
            cart_item = CartItemFactory(product=sample_product, cart=cart, price=PriceFactory(product=sample_product))
        self.assertEqual(cart_item.total_price, cart_item.product.price * cart_item.quantity)

    def test_cart_total_price_calculation(self):
        """
        Testing cart total price calculation
        """
        self.assertEqual(len(Cart.get_items(self.request)), 0)
        sample_product = ProductFactory()
        another_product = ProductFactory()
        cart = Cart.get_cart(self.request, create_if_not_exist=True)
        self.assertEqual(len(Cart.get_items(self.request)), 0)
        if MULTIPLE_PRICES:
            PriceFactory(product=sample_product)
            PriceFactory(product=another_product)
        cart.insert_item(sample_product, 1)
        self.assertEqual(len(Cart.get_items(self.request)), 1)
        cart_item_added = Cart.get_items(self.request)[0]
        self.assertEqual(cart_item_added.product, sample_product)
        self.assertEqual(cart_item_added.quantity, 1)
        cart.insert_item(sample_product, 1)
        self.assertEqual(len(Cart.get_items(self.request)), 1)
        cart.insert_item(another_product, 1)
        self.assertEqual(len(Cart.get_items(self.request)), 2)
        cart_items = Cart.get_items(self.request)
        self.assertEqual(sample_product.price * cart_items[0].quantity, cart_items[0].total_price)
        self.assertEqual(another_product.price * cart_items[1].quantity, cart_items[1].total_price)
        self.assertEqual(sample_product.price * cart_items[0].quantity + another_product.price * cart_items[1].quantity, cart.total_price)
        self.assertEqual(cart_items[0].total_price + cart_items[1].total_price, cart.total_price)

    def test_cart_total_quantity_calculation(self):
        """
        Testing cart total quantity calculation
        """
        self.assertEqual(len(Cart.get_items(self.request)), 0)
        sample_product = ProductFactory()
        another_product = ProductFactory()
        cart = Cart.get_cart(self.request, create_if_not_exist=True)
        self.assertEqual(len(Cart.get_items(self.request)), 0)
        if MULTIPLE_PRICES:
            PriceFactory(product=sample_product)
            PriceFactory(product=another_product)
        cart.insert_item(sample_product, 20)
        self.assertEqual(len(Cart.get_items(self.request)), 1)
        cart_item_added = Cart.get_items(self.request)[0]
        self.assertEqual(cart_item_added.product, sample_product)
        self.assertEqual(cart_item_added.quantity, 20)
        cart.insert_item(sample_product, 1)
        self.assertEqual(len(Cart.get_items(self.request)), 1)
        cart.insert_item(another_product, 100)
        self.assertEqual(len(Cart.get_items(self.request)), 2)
        cart_items = Cart.get_items(self.request)
        self.assertEqual(cart.total_quantity, 121)
        self.assertEqual(cart.total_distinct_quantity, 2)

class ReservingTestCase(TestCase):
    """
    Tests for product reserving feature
    """
    def setUp(self):
        """
        Initialization
        """
        self.product = ProductFactory()
        PriceFactory(product=self.product, enabled=True, remainder=100)

    def test_normal_case(self):
        """
        Testing product reserving works fine in normal case
        """
        self.assertEquals(self.product.remainder, 100)
        self.assertEquals(self.product.reserved, 0)
        self.product.reserve_quantity(2)
        self.assertEquals(self.product.remainder, 98)
        self.assertEquals(self.product.reserved, 2)
        self.product.release_reserved(2)
        self.assertEquals(self.product.remainder, 100)
        self.assertEquals(self.product.reserved, 0)

    def test_edges(self):
        """
        Testing product reserving works predictable on edge cases
        """
        self.assertRaises(AssertionError, self.product.reserve_quantity, -1)
        self.assertRaises(AssertionError, self.product.reserve_quantity, 101)
        self.assertRaises(AssertionError, self.product.release_reserved, 1)

    def test_cart_item_creation(self):
        """
        Testing cart item creation cares about product remainder and reserving
        """
        CartItem.create()