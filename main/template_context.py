from .models import *;
from django.db.models import Max , Min;

def get_filters(request):
    cats = Product.objects.distinct().values('category__title','category__id')
    brand = Product.objects.distinct().values('brand__title','brand__id')
    color = ProductAttribute.objects.distinct().values('color__title','color__id','color__color_code')
    size = ProductAttribute.objects.distinct().values('size__title','size__id'),
    minMaxPrice = ProductAttribute.objects.aggregate(Min('price'),Max('price'))
    data = {
        'cats':cats,
        'brands':brand,
        'colors':color,
        'sizes':size,
        'minMaxPrice':minMaxPrice
    }
    return data