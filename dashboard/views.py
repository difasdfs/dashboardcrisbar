from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.utils import timezone

from .decorators import unauthenticated_user
from .logic import *
from .forms import CreateUserForm
from .models import *
# Create your views here.

""" HALAMAN LOGIN """


@unauthenticated_user
def loginpage(request):
    ngecekdeadline()
    context = {}
    # jika metode request adalah post
    if request.method == 'POST':
        # ambil username dan passwordnya
        username = request.POST.get('username')
        password = request.POST.get('password')

        # autentifikasi usernya
        user = authenticate(request, username=username, password=password)

        # kalau user berhasil diautentifikasi, login
        if user is not None:
            login(request, user)
            if apamanager(request.user):
                return redirect('manager')
            else:
                return redirect('staff')
        else:
            messages.info(request, 'username atau password salah')
            return render(request, 'dashboard/login.html', context)

    return render(request, 'dashboard/login.html', context)


"""HALAMAN PROFILE"""


@login_required(login_url='login')
def profile(request):
    nama = request.user.first_name
    context = {'nama': nama}
    manager = apamanager(request.user)

    if manager:
        return render(request, 'dashboard/profile.html', context)
    else:
        return render(request, 'dashboard/profile_staff.html', context)


""" LOGOUT """


def logoutuser(request):
    logout(request)
    return redirect('login')


""" MANAGER """


@login_required(login_url='login')
def manager(request):
    nama = request.user.first_name
    context = {'nama': nama}
    if not apamanager(request.user):
        return redirect('staff')
    return render(request, 'dashboard/manager.html', context)


@login_required(login_url='login')
def regisstaff(request):

    if not apamanager(request.user):
        return redirect('staff')

    nama = request.user.first_name
    bagian = bagianapa(request.user)

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username, '', password)
        user.first_name = request.POST['nama_lengkap']
        user.last_name = request.POST['bagian']
        user.save()
        grup_staff = Group.objects.get(name='Staff')
        grup_staff.user_set.add(user)
        return redirect('daftarstaff')

    else:
        context = {'bagian': bagian, 'nama': nama}

    return render(request, 'dashboard/regisstaff.html', context)


@login_required(login_url='login')
def daftarstaff(request):
    if not apamanager(request.user):
        return redirect('staff')

    nama = request.user.first_name
    bagian = bagianapa(request.user)
    anggota = anggotabagian(nama, bagian)

    context = {'nama': nama, 'anggota': anggota}
    return render(request, 'dashboard/daftarstaff.html', context)


@login_required(login_url='login')
def deleteuser(request, user_id):

    if not apamanager(request.user):
        return redirect('staff')

    delete_user(user_id)

    return redirect('manager')


@login_required(login_url='login')
def masukkantugas(request, user_id):

    if not apamanager(request.user):
        return redirect('staff')

    if request.method == 'POST':

        # ambil judul, isi, dan jenisnya
        staff = User.objects.get(pk=user_id)
        juduls = request.POST.get('judul')
        isis = request.POST.get('isi')
        jeniss = request.POST.get('jenis')
        deadlinetugas = request.POST.get('deadline')
        kuantitasnya = request.POST.get('kuantitas')

        # tulis data ke dalam database
        staff.tugas_set.create(
            judul=juduls,
            isi=isis,
            status="On Progress",
            jenis=jeniss,
            dibuat_pada=timezone.now(),
            deadline=deadlinetugas,
            kuantitas=kuantitasnya,
            selesai=0,
            acc=0
        )
        return redirect('tugas_staff')

    KelasStaff = get_user_model()
    objek_staff = KelasStaff.objects.get(pk=user_id)
    nama_staff = objek_staff.first_name

    nama = request.user.first_name
    context = {'nama': nama, 'nama_staff': nama_staff}
    return render(request, 'dashboard/inputtugas.html', context)


@ login_required(login_url='login')
def tugas_staff(request):

    context = {}
    if not apamanager(request.user):
        return redirect('staff')

    nama = request.user.first_name
    bagian = bagianapa(request.user)
    anggota = anggotabagian(nama, bagian)
    context['nama'] = nama

    tugas_pengguna = []

    for user in anggota:
        nama_user = user.first_name
        nama_tugas = user.tugas_set.all()

        for tugasnya in nama_tugas:
            judul = tugasnya.judul
            progress = tugasnya.progressnya()
            deadline = tugasnya.deadline_tugas()
            id_tugas = tugasnya.id
            tugas_pengguna.append(
                [nama_user, judul, progress, deadline, id_tugas])

    context['tugas_pengguna'] = tugas_pengguna

    return render(request, 'dashboard/tugas_staff.html', context)


""" STAFF """


@ login_required(login_url='login')
def staff(request):
    nama = request.user.first_name
    context = {'nama': nama}
    if apamanager(request.user):
        return redirect('manager')
    return render(request, 'dashboard/staff.html', context)


@ login_required(login_url='login')
def lihat_tugas(request):

    if apamanager(request.user):
        return redirect('manager')

    tugas_rutin, tugas_proyek = dapatkantugas(request.user.id)
    tugas_selesai = tugasselesai(request.user.id)
    tugas_deadline = tugasdeadline(request.user.id)

    nama = request.user.first_name
    context = {'nama': nama, 'tugas_rutin': tugas_rutin,
               'tugas_proyek': tugas_proyek, 'tugas_selesai': tugas_selesai, 'tugas_deadline': tugas_deadline}
    return render(request, 'dashboard/lihat_tugas.html', context)


@login_required(login_url='login')
def detail_tugas(request, tugas_id):

    if apamanager(request.user):
        return redirect('manager')

    if request.method == 'POST':
        a = Tugas.objects.get(pk=tugas_id)
        if (a.kuantitas > a.selesai) and a.status != 'Deadline':
            a.selesai += 1
            if (a.kuantitas == a.selesai) and (a.selesai > a.acc):
                a.status = 'Selesai'
                a.selesai_pada = timezone.now()
                a.save()
            a.save()

    nama = request.user.first_name
    context = detailtugas(tugas_id)
    context['nama'] = nama

    return render(request, 'dashboard/detail_tugas.html', context)
