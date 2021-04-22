# Generated by Django 3.2 on 2021-04-22 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxypay', '0006_reference_key'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reference',
            options={'verbose_name': 'Reference', 'verbose_name_plural': 'Referencecs'},
        ),
        migrations.RemoveField(
            model_name='reference',
            name='is_paid',
        ),
        migrations.AddField(
            model_name='reference',
            name='data',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='reference',
            name='amount',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=12, verbose_name='amount'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='entity',
            field=models.CharField(default=None, editable=False, max_length=100, null=True, verbose_name='entity'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='expires_in',
            field=models.DateTimeField(default=None, null=True, verbose_name='expires in'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='key',
            field=models.CharField(default=None, editable=False, max_length=125, null=True, unique=True, verbose_name='unique key'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='paid_at',
            field=models.DateTimeField(default=None, null=True, verbose_name='paid at'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='reference',
            field=models.CharField(editable=False, max_length=100, verbose_name='reference'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='status',
            field=models.IntegerField(choices=[(0, 'Waitng'), (1, 'Paid')], default=0, editable=False, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='update at'),
        ),
    ]
