from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    #Kullanıcı İşlemleri
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sahalar/', views.saha_listesi, name='saha_listesi'),
    path('saha/ekle/', views.saha_ekle, name='saha_ekle'),
    path('saha/<int:saha_id>/duzenle/', views.saha_duzenle, name='saha_duzenle'),
    path('saha/<int:saha_id>/sil/', views.saha_sil, name='saha_sil'),

]