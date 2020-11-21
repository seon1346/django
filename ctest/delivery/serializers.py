from rest_framework import serializers
from .models import *
import django.http.response


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "username", "password","new_address", "old_address")



class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ("id", "assigned_del_man", "assigned_customer","Item_Store","del_num","complete",)
