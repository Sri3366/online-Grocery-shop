import json
from django import template
from groceryapp.models import *

register = template.Library()

@register.filter()
def applydiscount(pid):
    try:
        data = Product.objects.get(id=pid)
        # Safely strip text strings and % signs out of character fields before converting to integer
        discount_str = str(data.discount).replace('%', '').strip()
        discount_value = int(discount_str) if discount_str.isdigit() else 0
        
        price = float(data.price) * (100 - discount_value) / 100
        return price
    except (Product.DoesNotExist, ValueError, KeyError):
        return 0

@register.filter()
def productimage(pid):
    try:
        data = Product.objects.get(id=pid)
        return data.image.url
    except (Product.DoesNotExist, ValueError):
        return ""

@register.filter()
def productname(pid):
    try:
        data = Product.objects.get(id=pid)
        return data.name
    except (Product.DoesNotExist, ValueError):
        return "Unknown Product"

@register.filter()
def productprice(pid):
    try:
        data = Product.objects.get(id=pid)
        return data.price
    except (Product.DoesNotExist, ValueError):
        return 0

@register.simple_tag()
def producttotalprice(data, qty):
    try:
        product = Product.objects.get(id=data)
        # Safely clean the discount string exactly like we did in applydiscount
        discount_str = str(product.discount).replace('%', '').strip()
        discount_value = float(discount_str) if discount_str.replace('.', '', 1).isdigit() else 0.0
        
        price = float(product.price) * (100 - discount_value) / 100
        return int(qty) * price
    except (Product.DoesNotExist, ValueError, KeyError):
        return 0

@register.filter()
def get_product(productli):
    try:
        productli = productli.replace("'", '"')
        myli = json.loads(str(productli))['objects'][0]
        pro_li = []
        for i, j in myli.items():
            pro_li.append(int(i))
        product = Product.objects.filter(id__in=pro_li)
        return product
    except:
        return None

@register.simple_tag
def get_qty(pro, bookid):
    try:
        book = Booking.objects.get(id=bookid)
        productli = book.product.replace("'", '"')
        myli = json.loads(str(productli))['objects'][0]
        return myli[str(pro)]
    except:
        return 0