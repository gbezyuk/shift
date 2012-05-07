from modeltranslation.translator import translator, TranslationOptions
from .models import Product, Category

class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

translator.register(Product, ProductTranslationOptions)
translator.register(Category, CategoryTranslationOptions)