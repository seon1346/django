from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','username','old_address', 'new_address','detailed_address','x','y')

class Del_manAdmin(admin.ModelAdmin):
    list_display = ('id','name','old_address', 'new_address','detailed_address','x','y')

class StoreAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','total')


class Item_StoreResource(Item_Store.ModelResource):
    def before_save_instance(self, instance, using_transactions, dry_run):
        instance.num = str(instance.username)

    class Meta:
        model = Item_Store

class Item_StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'item','store','num')
    resource_class = Item_StoreResource

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'assigned_del_man','assigned_customer','Item_Store','del_num','complete')





# Register your models here.
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Del_man, Del_manAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Item_Store, Item_StoreAdmin)
admin.site.register(Item, ItemAdmin)
