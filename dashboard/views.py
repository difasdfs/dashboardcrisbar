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
    usr = User.objects.get(pk=request.user.id)
    username = usr.username
    nama = request.user.first_name
    context = {'nama': nama, 'username': username}
    manager = apamanager(request.user)

    if request.method == 'POST':
        name = request.POST.get('nama_lengkap')
        username = request.POST.get('username')
        password = request.POST.get('password')
        usr.username = username
        usr.first_name = name        
        usr.set_password(password)
        usr.save()

        return redirect('login')

    if manager:
        return render(request, 'dashboard/profile.html', context)
    else:
        return render(request, 'dashboard/profile_staff.html', context)


""" LOGOUT """


def logoutuser(request):
    # ini halaman logout
    logout(request)
    return redirect('login')


""" MANAGER """

# test
@login_required(login_url='login')
def manager(request):
    nama = request.user.first_name
    context = {'nama': nama, 'data_kar' : True}
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
        context = {'bagian': bagian, 'nama': nama, 'data_kar' : True}

    return render(request, 'dashboard/regisstaff.html', context)


@login_required(login_url='login')
def daftarstaff(request):
    if not apamanager(request.user):
        return redirect('staff')

    nama = request.user.first_name
    bagian = bagianapa(request.user)
    anggota = anggotabagian(nama, bagian)

    context = {'nama': nama, 'anggota': anggota, 'data_kar' : True}
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
    context = {'nama': nama, 'nama_staff': nama_staff, 'data_kar' : True}
    return render(request, 'dashboard/inputtugas.html', context)


@ login_required(login_url='login')
def tugas_staff(request):
    
    ngecekdeadline()
    context = {'data_kar' : True}
    if not apamanager(request.user):
        return redirect('staff')

    nama = request.user.first_name
    bagian = bagianapa(request.user)
    anggota = anggotabagian(nama, bagian)
    context['nama'] = nama

    tugas_pengguna = []
    tugas_selesai = []
    tugas_deadline = []

    for user in anggota:
        nama_user = user.first_name
        nama_tugas = user.tugas_set.all()

        for tugasnya in nama_tugas:
            judul = tugasnya.judul
            progress = tugasnya.progressnya()
            deadline = tugasnya.deadline_tugas()
            id_tugas = tugasnya.id
            jenis = tugasnya.jenis
            status = tugasnya.status
            if status == 'Selesai':
                selesai_pada = tugasnya.formatwaktu(tugasnya.selesai_pada)
                tugas_selesai.append([nama_user, judul, progress, selesai_pada, id_tugas, status])
            elif status == 'Deadline':
                deadlinenya = tugasnya.formatwaktu(tugasnya.deadline)
                tugas_deadline.append([nama_user, judul, progress, deadlinenya, id_tugas, status])
            else:
                tugas_pengguna.append([nama_user, judul, progress, deadline, id_tugas, status, jenis])

    context['tugas_pengguna'] = tugas_pengguna
    context['tugas_selesai'] = tugas_selesai
    context['tugas_deadline'] = tugas_deadline

    return render(request, 'dashboard/tugas_staff.html', context)

@ login_required(login_url='login')
def detail_tugas_manager(request, tugas_id):
    if not apamanager(request.user):
        return redirect('staff')
    
    nama = request.user.first_name
    context = detailtugas(tugas_id)
    context['nama'] = nama
    context['idnya'] = tugas_id

    if request.method == 'POST':
        tugas = Tugas.objects.get(pk=tugas_id)
        tugas.delete()
        return redirect('tugas_staff')

    return render(request, 'dashboard/detail_tugas_manager.html', context)


@ login_required(login_url='login')
def edit_tugas(request, tugas_id):

    if not apamanager(request.user):
        return redirect('staff')

    nama = request.user.first_name
    context = detailtugas(tugas_id)
    status = context['status']
    context['nama'] = nama

    if request.method == 'POST':
        judul = request.POST.get('judul')
        isi = request.POST.get('isi')
        deadline = request.POST.get('deadline')
        kuantitas = request.POST.get('kuantitas')
        selesai = request.POST.get('selesai')
        t = Tugas.objects.get(pk=tugas_id)
        t.judul = judul
        t.isi = isi
        t.deadline = deadline
        t.kuantitas = kuantitas
        t.selesai = selesai

        if (t.kuantitas > t.selesai) and (status == 'Selesai'):
            t.status = 'On Progress'
        elif (t.selesai >= t.kuantitas ):
            t.status = 'Selesai'
        elif request.POST.get('status') == 'Selesai':
            t.selesai_pada = timezone.now()
            t.selesai = t.kuantitas
            t.status = 'Selesai'
        else:
            t.status = request.POST.get('status')

        t.save()
        return redirect('tugas_staff')

    return render(request, 'dashboard/edit_tugas.html', context)


""" STAFF """
@ login_required(login_url='login')
def staff(request):
    nama = request.user.first_name
    context = {'nama': nama}

    if request.user.last_name == 'Human Resource':
        context['data_kar'] = True

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
    
    if request.user.last_name == 'Human Resource':
        context['data_kar'] = True

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

    if request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'dashboard/detail_tugas.html', context)


""" HALAMAN DATA KARYAWAN """
@login_required(login_url='login')
def data_karyawan(request):
    
    d = DataKaryawan.objects.filter(status='AKTIF')
    
    context = {'nama' : request.user.first_name, 'data_kar':True, 'data' : d}
    
    return render(request, 'data_karyawan/index.html', context)


@login_required(login_url='login')
def detail_data(request, id_karyawan):
    data = DataKaryawan.objects.get(pk=id_karyawan)
    data.update_data()

    context = {'nama' : request.user.first_name, 'data_kar':True, 'data':data}
    return render(request, 'data_karyawan/detail.html', context)


@login_required(login_url='login')
def karyawan_tidak_aktif(request):

    d = DataKaryawan.objects.filter(status='KELUAR')
    
    context = {'nama' : request.user.first_name, 'data_kar':True, 'data' : d}
    return render(request, 'data_karyawan/karyawan_tidak_aktif.html', context)


@login_required(login_url='login')
def tambah_data_karyawan(request):

    if request.method == 'POST':
        dno_id_fingerprint = request.POST.get('no_id_fingerprint')
        dnama = request.POST.get('nama')
        darea = request.POST.get('area')
        dlevel_manajemen = request.POST.get('level_manajemen')
        dnama_posisi = request.POST.get('nama_posisi')
        dkode_posisi = request.POST.get('kode_posisi')
        dstatus_jabatan = request.POST.get('status_jabatan')
        djabatan_baru = request.POST.get('jabatan_baru')
        dstatus_pegawai = request.POST.get('status_pegawai')
        dtanggal_masuk = request.POST.get('tanggal_masuk')
        dno_ktp = request.POST.get('no_ktp')
        dtempat_lahir = request.POST.get('tempat_lahir')
        dtanggal_lahir = request.POST.get('tanggal_lahir')
        djenis_kelamin = request.POST.get('jenis_kelamin')
        dagama = request.POST.get('agama')
        dpendidikan = request.POST.get('pendidikan')
        djurusan = request.POST.get('jurusan')
        dalamat = request.POST.get('alamat')
        dno_hp = request.POST.get('no_hp')
        dmarital_status = request.POST.get('marital_status')
        danak = request.POST.get('anak')
        dno_rekening = request.POST.get('no_rekening')
        dbpjs_ketenagakerjaan = request.POST.get('bpjs_ketenagakerjaan')
        dstatus = request.POST.get('status')
        
        # -------------------------------------------------------------
        # darurat
        dnama_darurat = request.POST.get('nama_darurat')
        dalamat_darurat = request.POST.get('alamat_darurat')
        dhubungan_darurat = request.POST.get('hubungan_darurat')
        dno_hp_darurat = request.POST.get('no_hp_darurat')

        d = DataKaryawan(
            no_id_fingerprint = dno_id_fingerprint,
            nama = dnama,
            area = darea,
            level_manajemen = dlevel_manajemen,
            nama_posisi = dnama_posisi,
            kode_posisi = dkode_posisi,
            status_jabatan = dstatus_jabatan,
            jabatan_baru = djabatan_baru,
            status_pegawai = dstatus_pegawai,
            tanggal_masuk = dtanggal_masuk,
            no_ktp = dno_ktp,
            tempat_lahir = dtempat_lahir,
            tanggal_lahir = dtanggal_lahir,
            jenis_kelamin = djenis_kelamin,
            agama = dagama,
            pendidikan = dpendidikan,
            jurusan = djurusan,
            alamat = dalamat,
            no_hp = dno_hp,
            marital_status = dmarital_status,
            anak = danak,
            no_rekening = dno_rekening,
            bpjs_ketenagakerjaan = dbpjs_ketenagakerjaan,
            status = dstatus,
            nama_darurat = dnama_darurat,
            alamat_darurat = dalamat_darurat,
            hubungan_darurat = dhubungan_darurat,
            no_hp_darurat = dno_hp_darurat,
        )
        d.save()
        d.pasang_nik()
        d.inisialisasi()
        d.save()
        return redirect('data_karyawan')

    context = {'nama' : request.user.first_name, 'data_kar':True}
    return render(request, 'data_karyawan/tambah_data_karyawan.html', context)


@login_required(login_url='login')
def halaman_edit(request, id_karyawan):

    d = DataKaryawan.objects.get(pk=id_karyawan)

    context = {'nama' : request.user.first_name, 'data_kar':True, 'data' : d}

    if d.area == 'Office':
        context['area_office'] = True
    elif d.area == 'Cisitu':
        context['area_cisitu'] = True
    elif d.area == 'Jatinangor':
        context['area_jatinangor'] = True
    elif d.area == 'Metro':
        context['area_metro'] = True
    elif d.area == 'Sukajadi':
        context['area_sukajadi'] = True
    elif d.area == 'Telkom Sukabirus':
        context['area_telkom_sukabirus'] = True
    elif d.area == 'Telkom Sukapura':
        context['area_telkom_sukapura'] = True
    elif d.area == 'Unjani':
        context['area_unjadi'] = True

    if d.jenis_kelamin == 'L':
        context['lakilaki'] = True

    if d.pendidikan == 'SD':
        context['pendidikan_sd'] = True
    elif d.pendidikan == 'SMP':
        context['pendidikan_smp'] = True
    elif d.pendidikan == 'SMA/SMK':
        context['pendidikan_sma'] = True
    elif d.pendidikan == 'D3':
        context['pendidikan_d3'] = True
    elif d.pendidikan == 'S1':
        context['pendidikan_s1'] = True
    elif d.pendidikan == 'S2':
        context['pendidikan_s2'] = True
    elif d.pendidikan == 'S3':
        context['pendidikan_s3'] = True

    if d.marital_status == 'BELUM MENIKAH':
        context['status_belum'] = True
    elif d.marital_status == 'MENIKAH':
        context['status_menikah'] = True
    elif d.marital_status == 'CERAI':
        context['status_cerai'] = True

    if d.status == 'AKTIF':
        context['status_aktif'] = True

    if request.method == 'POST':
        dno_id_fingerprint = request.POST.get('no_id_fingerprint')
        dnama = request.POST.get('nama')
        darea = request.POST.get('area')
        dlevel_manajemen = request.POST.get('level_manajemen')
        dnama_posisi = request.POST.get('nama_posisi')
        dkode_posisi = request.POST.get('kode_posisi')
        dstatus_jabatan = request.POST.get('status_jabatan')
        djabatan_baru = request.POST.get('jabatan_baru')
        dstatus_pegawai = request.POST.get('status_pegawai')
        dtanggal_masuk = request.POST.get('tanggal_masuk')
        dno_ktp = request.POST.get('no_ktp')
        dtempat_lahir = request.POST.get('tempat_lahir')
        dtanggal_lahir = request.POST.get('tanggal_lahir')
        djenis_kelamin = request.POST.get('jenis_kelamin')
        dagama = request.POST.get('agama')
        dpendidikan = request.POST.get('pendidikan')
        djurusan = request.POST.get('jurusan')
        dalamat = request.POST.get('alamat')
        dno_hp = request.POST.get('no_hp')
        dmarital_status = request.POST.get('marital_status')
        danak = request.POST.get('anak')
        dno_rekening = request.POST.get('no_rekening')
        dbpjs_ketenagakerjaan = request.POST.get('bpjs_ketenagakerjaan')
        dstatus = request.POST.get('status')
        
        # -------------------------------------------------------------
        # darurat
        dnama_darurat = request.POST.get('nama_darurat')
        dalamat_darurat = request.POST.get('alamat_darurat')
        dhubungan_darurat = request.POST.get('hubungan_darurat')
        dno_hp_darurat = request.POST.get('no_hp_darurat')

        d.no_id_fingerprint = int(dno_id_fingerprint)
        d.nama = dnama
        d.area = darea
        d.level_manajemen = dlevel_manajemen
        d.nama_posisi = dnama_posisi
        d.kode_posisi = dkode_posisi
        d.status_jabatan = dstatus_jabatan
        d.jabatan_baru = djabatan_baru
        d.status_pegawai = dstatus_pegawai
        d.tanggal_masuk = dtanggal_masuk
        d.no_ktp = dno_ktp
        d.tempat_lahir = dtempat_lahir
        d.tanggal_lahir = dtanggal_lahir
        d.jenis_kelamin = djenis_kelamin
        d.agama = dagama
        d.pendidikan = dpendidikan
        d.jurusan = djurusan
        d.alamat = dalamat
        d.no_hp = dno_hp
        d.marital_status = dmarital_status
        d.anak = danak
        d.no_rekening = dno_rekening
        d.bpjs_ketenagakerjaan = dbpjs_ketenagakerjaan
        d.status = dstatus
        d.nama_darurat = dnama_darurat
        d.alamat_darurat = dalamat_darurat
        d.hubungan_darurat = dhubungan_darurat
        d.no_hp_darurat = dno_hp_darurat
        
        d.save()
        d.inisialisasi()
        d.save()
        return redirect('data_karyawan')
        # path('detail/<int:id_karyawan>', views.detail_data, name='detail'),

    return render(request, 'data_karyawan/halaman_edit.html', context)