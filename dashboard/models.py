from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import pytz
# Create your models here.


class Tugas(models.Model):
    STATUS = (
        ('Tuntas', 'Tuntas'),
        ('Hold', 'Hold'),
        ('Stuck', 'Stuck'),
        ('On Progress', 'On Progress'),
        ('Selesai', 'Selesai'),
        ('Deadline', 'Deadline'),
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
    selesai_pada = models.DateTimeField('Selesai pada', null=True)
    acc = models.IntegerField(null=True)

    def __str__(self):
        return self.judul

    def deadline_tugas(self):

        if self.status == 'Deadline':
            return 'Deadline'

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
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "Mei",
            6: "Jun",
            7: "Jul",
            8: "Agus",
            9: "Sep",
            10: "Okt",
            11: "Nov",
            12: "Des"
        }

        utc_datetime = propertinya
        local_timezone = pytz.timezone("Asia/Jakarta")
        local_datetime = utc_datetime.replace(tzinfo=pytz.utc)
        propertinya = local_datetime.astimezone(local_timezone)

        hari = str(propertinya.day)
        bulan = nama_bulan[propertinya.month]
        tahun = str(propertinya.year)
        jam = str(propertinya.hour)

        if len(jam) < 2:
            jam = "0" + jam
        menit = str(propertinya.minute)
        if len(menit) < 2:
            menit = "0" + menit

        return jam + ":" + menit + ", " + hari + " " + bulan + " " + tahun
