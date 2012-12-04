def import_from_csv(filename):
    f = open(filename)
    parsed = []
    for s in f:
        parsed.append(s.split(','))
    objects = [{'category': p[0], 'name': p[1], 'slug': p[2], 'sizes': p[4:-2], 'price': int("0"+p[3])} for p in parsed[3:]]

    i = 0
    sizes = []
    for p in parsed[0][3:-1]:
        sizes.append((p, parsed[1][3+i], parsed[2][3+i]))
        i += 1

    return sizes, objects

def import_sizes(sizes):
    from doppler.shift.catalog.models import Size
    for s in sizes:
        Size(title=s[-1]).save()


def import_products(products, mens_category, womens_category, childrens_category, quantity=100):
    from doppler.shift.catalog.models import Product, Shipment
    for p in products:
        if p['category'] == '\xd0\xbc\xd1\x83\xd0\xb6':
            c = mens_category
        elif p['category'] == '\xd0\xb6\xd0\xb5\xd0\xbd' :
            c = womens_category
        c = childrens_category
        pd = Product(category=c, name=p['name'], name_en=p['name'], name_ru=p['name'], base_price=p['price'], slug=p['slug'])
        pd.save()
        for s in range(len(p['sizes'])): #bug here
            Shipment(product=pd, size_id=s+1, remainder=quantity, enabled=True).save()

"""
from import_from_csv import *
from doppler.shift.catalog.models import *
Product.objects.all().delete()
sizes, products = import_from_csv('catalog.csv')
#import_sizes(sizes)
m,f,c = Category.objects.all()
import_products(products, m, f, c)

for p in products:
    if p['category'] == 'муж':
        pd = Product.objects.get(slug=p['slug'])
        pd.category_id = 1
        pd.save()
for p in products:
    if p['category'] == 'жен':
        pd = Product.objects.get(slug=p['slug'])
        pd.category_id = 2
        pd.save()

"""
