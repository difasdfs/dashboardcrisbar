# Generated by Django 3.1.3 on 2020-12-21 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_datakaryawan_umur'),
    ]

    operations = [
        migrations.AddField(
            model_name='datakaryawan',
            name='lama_bekerja',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
