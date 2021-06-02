# Generated by Django 3.2.3 on 2021-05-28 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0132_auto_20210528_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='car_number',
            field=models.CharField(default='TEGA28052021822', max_length=200, primary_key=True, serialize=False, verbose_name='Corrective action no.:'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='employeeID',
            field=models.CharField(default='TEGA743', max_length=10, primary_key=True, serialize=False, verbose_name='Employee ID'),
        ),
    ]
