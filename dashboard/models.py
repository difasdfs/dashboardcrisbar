from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tugas(models.Model):
    STATUS = (
        ('Stuck', 'Stuck'),
        ('On Progress', 'On Progress'),
        ('Selesai', 'Selesai'),
    )

    JENIS = (
        ('Rutin', 'Rutin'),
        ('Proyek', 'Proyek')
    )

    pemilik_tugas = models.ForeignKey(User, on_delete=models.CASCADE)
    judul = models.CharField(max_length=100)
    isi = models.CharField(max_length=255)
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS)
    jenis = models.CharField(max_length=100, choices=JENIS, null=True)

    def __str__(self):
        return self.judul
