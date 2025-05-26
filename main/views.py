from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import Halisaha, Reservation, CustomUser
from .forms import HalisahaForm, ReservationForm, CustomUserCreationForm
from .serializers import (
    HaliSahaSerializer, 
    UserSerializer, 
    UserRegistrationSerializer,
    ReservationSerializer
)

from django.db.models import Q  # Arama için Q nesnesi

@login_required
def saha_listesi(request):
    if request.user.user_type == 'owner':
        sahalar = Halisaha.objects.filter(owner=request.user)
    else:
        sahalar = Halisaha.objects.all()

    # Arama filtreleri
    name = request.GET.get('name')
    address = request.GET.get('address')
    phone = request.GET.get('phone')

    if name:
        sahalar = sahalar.filter(name__icontains=name)
    if address:
        sahalar = sahalar.filter(address__icontains=address)
    if phone:
        sahalar = sahalar.filter(phone__icontains=phone)

    return render(request, 'main/saha_listesi.html', {'sahalar': sahalar})


@login_required
def saha_ekle(request):
    if request.user.user_type != 'owner':
        return redirect('home')
    if request.method == 'POST':
        form = HalisahaForm(request.POST)
        if form.is_valid():
            saha = form.save(commit=False)
            saha.owner = request.user
            saha.save()
            return redirect('saha_listesi')
    else:
        form = HalisahaForm()

    return render(request, 'main/saha_form.html', {'form': form})

@login_required
def saha_duzenle(request, saha_id):
    saha = get_object_or_404(Halisaha, id=saha_id, owner=request.user)

    if request.method == 'POST':
        form = HalisahaForm(request.POST, instance=saha)
        if form.is_valid():
            form.save()
            return redirect('saha_listesi')
        else:
            form = HalisahaForm(instance=saha)

        return render(request, 'main/saha_form.html', {'form': form})
    

@login_required
def saha_sil(request, saha_id):
    saha = get_object_or_404(Halisaha, id=saha_id, owner=request.user)
    saha.delete()
    return redirect('saha_listesi')


def home(request):
    return render(request, 'main/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = request.POST.get('user_type', 'standard')
            user.save()
            login(request, user)
            messages.success(request, 'Kayıt başarılı! Hoş geldiniz.')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Giriş başarılı!')
            if user.user_type == 'owner':
                return redirect('saha_listesi')
            else:
                return redirect('rezervasyonlarim')
        else:
            messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
    
    return render(request, 'main/login.html')

@login_required
def saha_detay(request, saha_id):
    saha = get_object_or_404(Halisaha, id=saha_id)
    form = ReservationForm()

    # Aşama 1: Form gönderildiğinde veriyi session'a kaydet
    if request.method == 'POST' and 'form_submit' in request.POST:
        form = ReservationForm(request.POST)
        if form.is_valid():
            request.session['rez_saha_id'] = saha.id
            request.session['rez_date'] = form.cleaned_data['date'].isoformat()
            request.session['rez_hour_range'] = form.cleaned_data['hour_range']
            return render(request, 'main/saha_detail.html', {
                'saha': saha,
                'form': form,
                'show_payment': True  # Ödeme ekranı gözüksün
            })

    # Aşama 2: Ödeme onaylandıysa rezervasyon kaydı oluştur
    elif request.method == 'POST' and 'odeme_onayla' in request.POST:
        Reservation.objects.create(
            saha=saha,
            user=request.user,
            date=request.session.get('rez_date'),
            hour_range=request.session.get('rez_hour_range'),
        )
        return render(request, 'main/saha_detail.html', {
            'saha': saha,
            'form': ReservationForm(),
            'mesaj': "Rezervasyon oluşturuldu. Güzel maçlar dileriz! ⚽"
        })

    # Aşama 3: İptal edildiyse hiçbir şey kaydetme
    elif request.method == 'POST' and 'iptal_et' in request.POST:
        return render(request, 'main/saha_detail.html', {
            'saha': saha,
            'form': ReservationForm(),
            'mesaj': "Rezervasyon iptal edildi. Paran 2–5 gün içinde hesabında! 💸"
        })

    return render(request, 'main/saha_detail.html', {'saha': saha, 'form': form})


@login_required
def rezervasyonlarim(request):
    rezervasyonlar = Reservation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/rezervasyonlarim.html', {'rezervasyonlar': rezervasyonlar})

@login_required
def rezervasyon_iptal(request, rezervasyon_id):
    rezervasyon = get_object_or_404(Reservation, id=rezervasyon_id, user=request.user)
    rezervasyon.delete()
    return redirect('rezervasyonlarim')


# API Views
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Geçersiz kullanıcı adı veya şifre'}, status=status.HTTP_401_UNAUTHORIZED)

class HalisahaViewSet(viewsets.ModelViewSet):
    queryset = Halisaha.objects.all()
    serializer_class = HaliSahaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.user_type == 'owner':
            return Halisaha.objects.filter(owner=self.request.user)
        return Halisaha.objects.all()

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@login_required
def profil(request):
    if request.method == 'POST':
        # Kullanıcı bilgilerini güncelle
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        
        # Şifre değişikliği kontrolü
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if current_password and new_password and confirm_password:
            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    messages.success(request, 'Şifreniz başarıyla güncellendi.')
                else:
                    messages.error(request, 'Yeni şifreler eşleşmiyor.')
            else:
                messages.error(request, 'Mevcut şifre yanlış.')
        
        try:
            user.save()
            messages.success(request, 'Profil bilgileriniz güncellendi.')
        except Exception as e:
            messages.error(request, 'Profil güncellenirken bir hata oluştu.')
        
        return redirect('profil')
    
    return render(request, 'main/profil.html')
