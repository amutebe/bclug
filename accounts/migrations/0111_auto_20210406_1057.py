# Generated by Django 3.0.2 on 2021-04-06 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0110_auto_20210406_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='car_number',
            field=models.CharField(default='TEGA06042021260', max_length=200, primary_key=True, serialize=False, verbose_name='Corrective action no.:'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='employeeID',
            field=models.CharField(default='TEGA875', max_length=10, primary_key=True, serialize=False, verbose_name='Employee ID'),
        ),
    ]
