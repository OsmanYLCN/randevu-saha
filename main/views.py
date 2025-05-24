from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.shortcuts import get_object_or_404
from .models import Halisaha
from .forms import HalisahaForm



@login_required
def saha_listesi(request):
    if request.user.user_type == 'owner':
        sahalar = Halisaha.objects.filter(owner=request.user)
    else:
        sahalar = Halisaha.objects.all()
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
    saha_sil()
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
