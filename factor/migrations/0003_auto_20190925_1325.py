# Generated by Django 2.2.5 on 2019-09-25 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factor', '0002_auto_20190925_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='OrderDate',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
