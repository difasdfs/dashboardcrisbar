from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.staff, name='staff'),
    path('manager/', views.manager, name='manager'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('regisstaff/', views.regisstaff, name='regisstaff'),
    path('daftarstaff/', views.daftarstaff, name='daftarstaff'),
    path('delete/<int:user_id>/', views.deleteuser, name='deleteuser'),
    path('masuktugas/<int:user_id>/', views.masukkantugas, name='masukkantugas'),
    path('lihat_tugas/', views.lihat_tugas, name='lihattugas'),
    path('lihat_tugas/<int:tugas_id>/', views.detail_tugas, name='detail_tugas'),
    path('profile/', views.profile, name='profile'),
    path('tugas_staff/', views.tugas_staff, name='tugas_staff'),
    path('tugas_staff/<int:tugas_id>/', views.detail_tugas_manager, name='detail_tugas_manager'),
    path('edit_tugas/<int:tugas_id>', views.edit_tugas, name='edit_tugas'),
    path('data_karyawan/', views.data_karyawan, name='data_karyawan'),
    path('detail/<int:id_karyawan>', views.detail_data, name='detail'),
    path('tambah_data_karyawan/', views.tambah_data_karyawan, name='tambah_data_karyawan'),
    path('karyawan_tidak_aktif/', views.karyawan_tidak_aktif, name='karyawan_tidak_aktif'),
    path('halaman_edit/<int:id_karyawan>', views.halaman_edit, name='halaman_edit'),
    path('karyawan_keluar/<int:id_karyawan>', views.karyawan_keluar, name='karyawan_keluar'),
]
