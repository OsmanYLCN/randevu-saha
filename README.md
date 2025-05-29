# Randevu Saha

**Randevu Saha**, halı saha sahipleriyle oyuncuları bir araya getiren, modern rezervasyon sistemi sunan bir Django web uygulamasıdır. Kullanıcılar kolayca saha arayabilir, uygun saatleri seçip rezervasyon yapabilir; işletmeler ise sahalarını yönetebilir.

---

## 🎯 Proje Özeti

Gerçek dünyadaki halı saha rezervasyon sorunlarına çözüm üretmeyi amaçlayan bu proje, kullanıcıların çevrimiçi ortamda hızlı ve pratik bir şekilde saha bulup rezervasyon yapmasını sağlar. Aynı zamanda saha sahiplerine kullanıcı dostu bir yönetim paneli sunar.

---

## 🗂️ Klasör Yapısı

```
randevu-saha/
├── .git/                  # Git versiyon kontrol klasörü
├── config/                # Django ayarlarını içeren config uygulaması
├── main/                  # Uygulamanın ana fonksiyonlarını barındıran klasör
│   ├── migrations/        # Veritabanı migration dosyaları
│   ├── static/            # Statik dosyalar (CSS, JS, resimler)
│   ├── templates/         # HTML şablonları
│   ├── admin.py           # Admin arayüz tanımları
│   ├── apps.py            # Uygulama konfigürasyonu
│   ├── forms.py           # Form tanımlamaları
│   ├── models.py          # Veritabanı modelleri
│   ├── serializers.py     # API serializer'ları
│   ├── tests.py           # Test dosyası
│   ├── urls.py            # Uygulama URL yönlendirmeleri
│   └── views.py           # View fonksiyonları
├── manage.py              # Django yönetim komut dosyası
├── requirements.txt       # Proje bağımlılıkları
└── README.md              # Proje tanıtım dosyası
```

---

## 🛠️ Kullanılan Teknolojiler

- Python 3.x
- Django 5.x
- Django REST Framework
- SQLite 
- HTML5 / CSS3 / JavaScript

---

## 🔐 Temel Özellikler

- ✅ Halı saha ekleme, listeleme, düzenleme, silme (CRUD işlemleri)
- 👥 Kullanıcı kayıt, giriş ve çıkış işlemleri
- 🔐 Farklı kullanıcı rolleri (normal kullanıcı ve saha sahibi)
- 🕒 Rezervasyon oluşturma ve zaman aralığına göre kontrol
- 🔍 Saha filtreleme ve arama özelliği
- 📂 Veri dışa aktarma (CSV formatı)
- 🌐 REST API üzerinden saha ve rezervasyon yönetimi
- 📱 Mobil uyumlu ve basit arayüz tasarımı
- 🎨 HTML5, CSS3 ile şık ve modern tasarım

---

## 🌐 API Desteği

Uygulama, RESTful mimari ile API desteği sunar. JSON formatında veri alıp gönderebilir. API endpoint’leri aşağıdaki gibidir:

- `/api/sahalar/` → Saha listeleme ve oluşturma
- `/api/rezervasyonlar/` → Rezervasyon işlemleri
- `/api/register/` → Kullanıcı kaydı
- `/api/login/` → Giriş işlemi (token ile)

---

## 📦 Kurulum

```bash
# 1. Depoyu klonlayın
git clone https://github.com/kullaniciadi/randevu-saha.git
cd randevu-saha

# 2. Sanal ortam oluşturun
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. Veritabanını migrate edin
python manage.py makemigrations
python manage.py migrate

# 5. Admin hesabı oluşturun
python manage.py createsuperuser

# 6. Sunucuyu başlatın
python manage.py runserver
```

---

## 🌐 API Uç Noktaları

- `/api/sahalar/` – Saha listeleme/oluşturma
- `/api/rezervasyonlar/` – Rezervasyon işlemleri
- `/api/register/` – Yeni kullanıcı oluşturma
- `/api/login/` – Kullanıcı girişi

---

## 📜 Lisans

Bu proje, bireysel öğrenim ve geliştirme amaçlıdır. Ticari kullanım için uygun değildir.

---

Randevu Saha projesi, temel web geliştirme becerilerini gerçek bir probleme entegre ederek sunmak amacıyla geliştirilmiştir. Hem teknik hem görsel açıdan öğretici ve geliştirici bir örnek teşkil eder.