# Generated by Django 2.0.9 on 2018-11-23 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Images', '0002_auto_20181122_1757'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-created_at']},
        ),
    ]
