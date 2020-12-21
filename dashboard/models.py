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

class DataKaryawan(models.Model):
    AREA = (
        ('Office', 'Office'),
        ('Jatinangor', 'Jatinangor'),
        ('Cisitu', 'Cisitu'),
        ('Unjani', 'Unjani'),
        ('Metro', 'Metro'),
        ('Sukajadi', 'Sukajadi'),
        ('Telkom Sukabirus', 'Telkom Sukabirus'),
        ('Telkom Sukapura', 'Telkom Sukapura'),
    )

    JENIS_KELAMIN = (
        ('L', 'L'),
        ('P', 'P'),
    )

    PENDIDIKAN = (
        ('SD', 'SD'),
        ('SMP', 'SMP'),
        ('SMA/SMK', 'SMA/SMK'),
        ('D3', 'D3'),
        ('S1', 'S1'),
        ('S2', 'S2'),
        ('S3', 'S3'),
    )

    MARITAL = (
        ('BELUM MENIKAH', 'BELUM MENIKAH'),
        ('MENIKAH', 'MENIKAH'),
        ('CERAI', 'CERAI')
    )

    STATUS = (
        ('AKTIF','AKTIF'),
        ('KELUAR', 'KELUAR'),
    )

    nik = models.CharField(max_length=4, null=True)
    no_id_fingerprint = models.IntegerField()
    nama = models.CharField(max_length=100)
    area = models.CharField(max_length=30, choices=AREA)
    level_manajemen = models.CharField(max_length=40)
    nama_posisi = models.CharField(max_length=30)
    kode_posisi = models.CharField(max_length=5)
    status_jabatan = models.CharField(max_length=40, null=True)
    jabatan_baru = models.CharField(max_length=40, null=True)
    status_pegawai = models.CharField(max_length=50, null=True)
    tanggal_masuk = models.DateField('Tanggal Masuk', null=True)
    lama_bekerja = models.CharField(max_length=100, null=True)
    no_ktp = models.CharField(max_length=30, null=True)
    tempat_lahir = models.CharField(max_length=40, null=True)
    umur = models.IntegerField(null=True)
    tanggal_lahir = models.DateField('Tanggal Lahir', null=True)
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN)
    agama = models.CharField(max_length=20, null=True)
    pendidikan = models.CharField(max_length=10, choices=PENDIDIKAN)
    jurusan = models.CharField(max_length=40, null=True)
    alamat = models.CharField(max_length=100, null=True)
    no_hp = models.CharField(max_length=20)
    marital_status = models.CharField(max_length=20, choices=MARITAL)
    anak = models.IntegerField()
    no_rekening = models.CharField(max_length=100, null=True)
    bpjs_ketenagakerjaan = models.CharField(max_length=100, null=True)
    nama_darurat = models.CharField(max_length=100, null=True)
    alamat_darurat = models.CharField(max_length=100, null=True)
    hubungan_darurat = models.CharField(max_length=100, null=True)
    no_hp_darurat = models.CharField(max_length=100, null=True)

    status = models.CharField(max_length=100, null=True, choices=STATUS)

    tanggal_keluar = models.DateField('Tanggal Keluar', null=True)
    alasan_keluar = models.CharField(max_length=200, null=True)
    # metod lama bekerja
    # umur
    def __str__(self):
        return self.nama

    def pasang_nik(self):
        nike = str(self.id)
        tampilan = '000' + nike
        self.nik = tampilan[-4:]

    def inisialisasi(self):
        self.nama = self.nama.upper()
        self.alamat = self.alamat.upper()
        self.tempat_lahir = self.tempat_lahir.upper()
        self.kode_posisi = self.kode_posisi.upper()
        self.agama = self.agama.upper()

    def update_data(self):
        # umur
        if self.status != 'KELUAR':
            lahir = self.tanggal_lahir
            hariini = datetime.date.today()
            selisih = hariini - lahir
            self.umur = selisih.days // 365

            # lama bekerja
            masuk = self.tanggal_masuk
            selisih = hariini - masuk
            selisih = selisih.days
            bulan = selisih // 30
            selisih = selisih - (bulan*30)

            self.lama_bekerja = str(bulan) + " bulan, " + str(selisih) + " hari"