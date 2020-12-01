# Generated by Django 3.1.3 on 2020-11-29 03:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tugas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=100)),
                ('isi', models.CharField(max_length=255)),
                ('dibuat_pada', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Stuck', 'Stuck'), ('On Progress', 'On Progress'), ('Selesai', 'Selesai')], max_length=100)),
                ('jenis', models.CharField(choices=[('Rutin', 'Rutin'), ('Proyek', 'Proyek')], max_length=100, null=True)),
                ('pemilik_tugas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]