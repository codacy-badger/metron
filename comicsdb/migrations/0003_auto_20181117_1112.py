# Generated by Django 2.1.3 on 2018-11-17 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comicsdb', '0002_change_team_image_field'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='issue',
            options={'ordering': ['series__sort_name', 'cover_date', 'number']},
        ),
    ]
