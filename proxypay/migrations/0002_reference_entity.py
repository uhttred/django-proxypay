# Generated by Django 3.0.5 on 2020-05-09 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxypay', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='entity',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]