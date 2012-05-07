"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Model managers
"""
from mptt.managers import TreeManager

class EnabledTreeManager(TreeManager):
    """
    Tree manager with enabled=True filter predefined.
    """
    def get_query_set(self):
        """
        Returns a ``QuerySet`` which contains all tree items, ordered in
        such a way that that root nodes appear in tree id order and
        their subtrees appear in depth-first order, filtered by enabled=True.
        """
        return super(EnabledTreeManager, self).get_query_set().filter(enabled=True)

class EnabledRootManager(EnabledTreeManager):
    """
    Tree manager with enabled=True and parent=None filters predefined
    """
    def get_query_set(self):
        """
        Returns a ``QuerySet`` which contains all tree items, ordered in
        such a way that that root nodes appear in tree id order and
        their subtrees appear in depth-first order, filtered by enabled=True and parent=None.
        """
        return super(EnabledRootManager, self).get_query_set().filter(parent=None)