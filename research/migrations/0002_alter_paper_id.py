# Generated by Django 4.2.5 on 2023-10-01 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
