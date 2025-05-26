from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login

from .models import Halisaha, Reservation, CustomUser
from .forms import HalisahaForm, ReservationForm, CustomUserCreationForm
from rest_framework import viewsets

from .serializers import HaliSahaSerializer
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
            user.user_type = 'standard'  # varsayılan kullanıcı tipi
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})


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


class HalisahaViewSet(viewsets.ModelViewSet):
    queryset = Halisaha.objects.all()
    serializer_class = HaliSahaSerializer
