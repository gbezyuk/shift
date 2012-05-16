"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Model tests
Subpart: Cart tests
"""
from django.test import TestCase
from doppler.shift.checkout.models import Cart

class CartTestCase(TestCase):
    """
    Tests for Cart model
    """
    def setUp(self):
        """
        Initialization
        """
        pass

    def test_cart_exists_for_unauthorized_user(self):
        """
        Testing cart existance for unauthorized user
        """
        raise NotImplementedError

    def test_cart_exists_for_authorized_user(self):
        """
        Testing cart existance for authorized user
        """
        raise NotImplementedError

    def test_adding_product_to_cart_by_unauthorized_user(self):
        """
        Testing adding product to cart by unauthorized user
        """
        raise NotImplementedError

    def test_adding_product_to_cart_by_authorized_user(self):
        """
        Testing adding product to cart by authorized user
        """
        raise NotImplementedError

    def test_changing_cart_product_quantity_by_unauthorized_user(self):
        """
        Testing changing cart product quantity by unauthorized user
        """
        raise NotImplementedError

    def test_changing_cart_product_quantity_by_authorized_user(self):
        """
        Testing changing cart product quantity by authorized user
        """
        raise NotImplementedError

    def test_removing_cart_product_by_authorized_user(self):
        """
        Testing removing cart product by authorized user
        """
        raise NotImplementedError

    def test_removing_cart_product_by_unauthorized_user(self):
        """
        Testing removing cart product by unauthorized user
        """
        raise NotImplementedError

    def test_clear_cart_by_authorized_user(self):
        """
        Testing clearing cart by authorized user
        """
        raise NotImplementedError

    def test_clear_cart_by_unauthorized_user(self):
        """
        Testing clearing cart by unauthorized user
        """
        raise NotImplementedError

    def test_cart_item_total_price_calculation(self):
        """
        Testing cart item total price calculation
        """
        raise NotImplementedError

    def test_cart_total_price_calculation(self):
        """
        Testing cart total price calculation
        """
        raise NotImplementedError

    def test_cart_total_quantity_calculation(self):
        """
        Testing cart total quantity calculation
        """
        raise NotImplementedError

    def test_cart_distinct_quantity_calculation(self):
        """
        Testing cart distinct quantity calculation
        """
        raise NotImplementedError