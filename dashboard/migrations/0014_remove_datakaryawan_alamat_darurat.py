# Generated by Django 3.1.3 on 2020-12-18 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_auto_20201218_1034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datakaryawan',
            name='alamat_darurat',
        ),
    ]