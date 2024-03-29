from django.contrib import admin
from .models import *
admin.site.register(Brand)
admin.site.register(Size)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('alt_text','image_tag')
admin.site.register(Banner,BannerAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','image_tag')
admin.site.register(Category,CategoryAdmin)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('title','color_bg')
admin.site.register(Color,ColorAdmin)



class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','title','brand','color','size','status','is_featured','category')
    list_editable = ('status','is_featured')
admin.site.register(Product,ProductAdmin)


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id','product','price','color','size')
admin.site.register(ProductAttribute,ProductAttributeAdmin)

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ('paid_status','order_status')
    list_display = ('user','total_amt','paid_status','order_dt','order_status')
admin.site.register(CartOrder,CartOrderAdmin)


class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = ('invoice_no','item','image_tag','qty','price','total')
admin.site.register(CartOrderItems,CartOrderItemAdmin)

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user','product','review_text','get_review_rating')
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(Wishlist)

class UserAddressBookAdmin(admin.ModelAdmin):
    list_editable = ('status',)
    list_display = ('user','address','status','mobile')
admin.site.register(UserAddressBook,UserAddressBookAdmin)