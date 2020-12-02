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
    path('profile/', views.profile, name='profile')
]
