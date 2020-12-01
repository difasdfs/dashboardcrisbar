from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import *


def apamanager(user):
    return user.groups.filter(name='Manager').exists()


def bagianapa(user):
    return user.last_name


def anggotabagian(nama_manager, bagian):
    User = get_user_model()
    users = User.objects.filter(
        last_name=bagian).exclude(first_name=nama_manager)
    return users


def delete_user(user_id):
    User = get_user_model()
    users = User.objects.filter(pk=user_id)
    users.delete()


def inputtugasstaff(nama_staff, judul, isi, status, jenis):
    t = Tugas(
        nama_staff,
        judul,
        isi,
        status,
        jenis
    )
    t.save()


def dapatkantugas(user_id):
    pengguna = User.objects.get(pk=user_id)
    tugasnya = pengguna.tugas_set.all()

    tugas_rutin = []
    tugas_proyek = []

    for tugas in tugasnya:
        if tugas.jenis == "Rutin":
            tugas_rutin.append(tugas)
        elif tugas.jenis == "Proyek":
            tugas_proyek.append(tugas)

    return (tugas_rutin, tugas_proyek)