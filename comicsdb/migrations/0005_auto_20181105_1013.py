# Generated by Django 2.1.3 on 2018-11-05 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comicsdb', '0004_auto_20181105_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='desc',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='short_desc',
            field=models.CharField(blank=True, max_length=350, verbose_name='Short Description'),
        ),
    ]
