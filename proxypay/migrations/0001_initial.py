# Generated by Django 3.0.5 on 2020-05-07 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.IntegerField(unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('custom_fields_text', models.TextField(default='')),
                ('paid', models.BooleanField(default=False)),
                ('payment_status', models.CharField(default='wait', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
