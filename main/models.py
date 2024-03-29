from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
#Banner
class Banner(models.Model):
    img = models.ImageField(upload_to ="banner_imgs/")
    alt_text = models.CharField(max_length = 200)
    class Meta:
        verbose_name_plural = '1. Banners'
    def image_tag(self):
        return mark_safe(f'<img src = "{self.img.url}" width="100"/>')
    def __str__(self):
        return self.alt_text

# Category models
class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cat_imgs/")
    class Meta:
        verbose_name_plural = '2.Categories'
    def image_tag(self):
        return mark_safe(f'<img src = "{self.image.url}" width="50" height="50"/>')
    def __str__(self):
        return self.title
    

# Brand models
class Brand(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="brand_imgs/")
    class Meta:
        verbose_name_plural = '3. Brands'
    def __str__(self):
        return self.title
#Color
class Color(models.Model):
    title = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = '4. Colors'
    def color_bg(self):
        return mark_safe(f'<div style="width:50px; height:50px;background-color:{self.color_code}"></div>')
    def __str__(self):
        return self.title
#size 
class Size(models.Model):
    title = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = '5. Sizes'
    def __str__(self):
        return self.title
#Product models
class Product(models.Model):
    title = models.CharField(max_length=100)
   
    slug = models.CharField(max_length=100)
    detail = models.TextField()
    specs = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = '6. Products'
    def __str__(self):
        return self.title
    


#product Attribute
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    color = models.ForeignKey(Color , on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    price =models.PositiveBigIntegerField()
    image = models.ImageField(upload_to="product_imgs/",null=True)
    class Meta:
        verbose_name_plural = '7. ProductAttributes'
    def __str__ (self):
        return self.product.title
    

status_choice = (
    ('process','In Process'),
    ('shipped','Shipped'),
    ('delivered','Delivered'),
)

class CartOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total_amt = models.FloatField()
    paid_status = models.BooleanField(default=False)
    order_dt = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices = status_choice,default='process',max_length=150)
    class Meta:
        verbose_name_plural = '8.Order'
    
  




class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=150)
    item = models.CharField(max_length=150)
    image = models.CharField(max_length=200)
    qty = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
    class Meta:
        verbose_name_plural = '9.Order Items'
    def image_tag(self):
        return mark_safe(f'<img src = "/media/{self.image}" width="50" height="50"/>')


#Product Review
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProductReview(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    review_text = models.TextField()
    review_rating = models.CharField(choices=RATING,max_length=150)

    def get_review_rating(self):
        return self.review_rating


class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)



class UserAddressBook(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=False)
    mobile = models.CharField(max_length=50,null=True)
    address = models.TextField()
    status = models.BooleanField(default = False)
    class Meta:
        verbose_name_plural = 'AddressBook'
