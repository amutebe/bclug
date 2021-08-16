# Generated by Django 3.2.3 on 2021-08-14 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0201_auto_20210814_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='car_number',
            field=models.CharField(default='BCL14082021416', max_length=200, primary_key=True, serialize=False, verbose_name='Corrective action no.:'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='employeeID',
            field=models.CharField(default='BCL716', max_length=20, primary_key=True, serialize=False, verbose_name='Employee ID'),
        ),
    ]
