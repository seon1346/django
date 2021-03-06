# Generated by Django 3.1.3 on 2020-11-20 07:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0009_item_item_store'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='assigned_store',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='num_item_1',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='num_item_2',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='num_item_3',
        ),
        migrations.AddField(
            model_name='delivery',
            name='Item_Store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.item_store'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='del_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='assigned_customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='assigned_del_man',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.del_man'),
        ),
    ]
