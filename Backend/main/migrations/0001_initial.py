# Generated by Django 2.0.2 on 2018-04-05 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=300)),
                ('location', models.CharField(max_length=300)),
                ('address', models.CharField(max_length=500)),
                ('_zip', models.CharField(max_length=10)),
            ],
        ),
    ]
