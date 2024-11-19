# Generated by Django 5.1.3 on 2024-11-19 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_customuser_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='child_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='current_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='relationship_with_child',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
