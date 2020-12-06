from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
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
    dibuat_pada = models.DateTimeField('Dibuat pada')
    status = models.CharField(max_length=100, choices=STATUS)
    jenis = models.CharField(max_length=100, choices=JENIS, null=True)
    deadline = models.DateTimeField('Deadline', null=True)
    kuantitas = models.IntegerField(null=True)
    selesai = models.IntegerField(null=True)
    acc = models.IntegerField(null=True)

    def __str__(self):
        return self.judul

    def deadline_tugas(self):
        saat_ini = timezone.now()
        deadline = self.deadline

        selisih_deadline = deadline - saat_ini

        deadline_hari = selisih_deadline.days
        detik = selisih_deadline.seconds
        konversi = datetime.timedelta(seconds=detik)

        waktu = str(konversi).split(':')
        jam = waktu[0]
        menit = waktu[1]

        return str(deadline_hari) + " hari, " + jam + " jam, " + menit + " menit."

    def progressnya(self):
        return str(self.selesai) + "/" + str(self.kuantitas)

    def formatwaktu(self, propertinya):
        nama_bulan = {
            1: "Januari",
            2: "Februari",
            3: "Maret",
            4: "April",
            5: "Mei",
            6: "Juni",
            7: "Juli",
            8: "Agustus",
            9: "September",
            10: "Oktober",
            11: "November",
            12: "Desember"
        }

        hari = str(propertinya.day)
        bulan = nama_bulan[propertinya.month]
        tahun = str(propertinya.year)
        jam = str(propertinya.hour+7)
        if len(jam) < 2:
            jam = "0" + jam
        menit = str(propertinya.minute)
        if len(menit) < 2:
            menit = "0" + menit

        return jam + ":" + menit + ", " + hari + " " + bulan + " " + tahun
