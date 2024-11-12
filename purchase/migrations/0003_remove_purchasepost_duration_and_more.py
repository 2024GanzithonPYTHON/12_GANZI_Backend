# Generated by Django 5.1.3 on 2024-11-10 12:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0002_rename_account_info_purchasepost_account_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasepost',
            name='duration',
        ),
        migrations.AddField(
            model_name='purchasepost',
            name='duration_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='purchasepost',
            name='duration_time',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AlterField(
            model_name='purchasepost',
            name='bank_name',
            field=models.CharField(default='Default Bank Name', max_length=100),
        ),
        migrations.AlterField(
            model_name='purchasepost',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchasepost',
            name='tags',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
    ]