# Generated by Django 2.0.2 on 2018-04-06 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_vehicle'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='vehicle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Vehicle'),
        ),
    ]
