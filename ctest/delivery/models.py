from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class Customer(AbstractUser):
    new_address=models.TextField(default="")
    old_address =models.TextField(default="")
    detailed_address=models.TextField(default="")
    x= models.FloatField(default=0)
    y= models.FloatField(default=0)

    class Meta:
        db_table = "Customer"
        verbose_name = "고객"
        verbose_name_plural = "고객"



class Del_man(models.Model):
    name=models.CharField(default="",max_length=30)
    new_address=models.TextField(default="")
    old_address =models.TextField(default="")
    detailed_address = models.TextField(default="")
    x= models.FloatField(default=0)
    y= models.FloatField(default=0)
    class Meta:
        db_table = "DeliveryMan"
        verbose_name = "배달원"
        verbose_name_plural = "배달원"


class Store(models.Model):
    name=models.TextField(default="")
    class Meta:
        db_table = "Store"
        verbose_name = "고객사"
        verbose_name_plural = "고객사"


class Item(models.Model):
    name=models.TextField(default="")
    total=models.IntegerField(default=0)

    class Meta:
        db_table = "Item"
        verbose_name = "상품"
        verbose_name_plural = "상품"


class Item_Store(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    num=models.IntegerField(default=0)

    class Meta:
        db_table = "Item_Store"
        verbose_name = "고객사별 상품수"
        verbose_name_plural = "고객사별 상품수"


class Delivery(models.Model):
    assigned_del_man=models.ForeignKey('Del_man',null=True, on_delete=models.CASCADE)
    assigned_customer=models.ForeignKey('Customer',null=True, on_delete=models.CASCADE)
    Item_Store = models.ForeignKey('Item_Store', null=True,on_delete=models.CASCADE)
    del_num=models.IntegerField(default=0)
    complete=models.BooleanField(default=False)
    class Meta:
        db_table = "Delivery"
        verbose_name = "배달정보"
        verbose_name_plural = "배달정보"

