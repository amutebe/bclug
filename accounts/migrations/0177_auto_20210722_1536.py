# Generated by Django 3.2.3 on 2021-07-22 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0176_auto_20210722_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='car_number',
            field=models.CharField(default='BCL22072021169', max_length=200, primary_key=True, serialize=False, verbose_name='Corrective action no.:'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='employeeID',
            field=models.CharField(default='BCL732', max_length=10, primary_key=True, serialize=False, verbose_name='Employee ID'),
        ),
    ]
