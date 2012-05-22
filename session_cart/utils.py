from session_cart import settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

_carts = {}

CARTS = getattr(settings, 'CARTS', {'default': 'session_cart.cart.CartItem'})

def import_cart(import_path):
    """
    Imports the cart class described by import_path, where import_path is the
    full Python path to the class.
    """
    try:
        dot = import_path.rindex('.')
    except ValueError:
        raise ImproperlyConfigured("%s isn't a Python path." % import_path)
    module, classname = import_path[:dot], import_path[dot + 1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                   (module, e))
    try:
        return getattr(mod, classname)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" '
                                   'class.' % (module, classname))

def get_carts():
    """
    Return a dictionary of carts, where each key is the request attribute name
    and each value is a Cart object.
    """
    if not _carts:
        for key, value in settings.CARTS.items():
            _carts[key] = import_cart(value)
    return _carts