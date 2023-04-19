# Generated by Django 4.1.7 on 2023-04-15 10:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('budgetApp', '0005_remove_expense_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='description',
            field=models.TextField(default=django.utils.timezone.now, max_length=60),
            preserve_default=False,
        ),
    ]
