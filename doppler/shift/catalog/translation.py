from modeltranslation.translator import translator, TranslationOptions
from .models import Product, Category, MULTIPLE_PRICES

class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

translator.register(Product, ProductTranslationOptions)
translator.register(Category, CategoryTranslationOptions)

if MULTIPLE_PRICES:
    from .models import Color
    class ColorTranslationOptions(TranslationOptions):
        fields = ('title',)
    translator.register(Color, ColorTranslationOptions)