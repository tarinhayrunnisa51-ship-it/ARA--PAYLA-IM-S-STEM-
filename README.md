# DriveShare - Araç Paylaşım Sistemi

DriveShare, araç kiralama süreçlerini dijitalleştirmek ve kolayca yönetmek için geliştirilmiş profesyonel bir masaüstü yönetici panelidir. Python ve PyQt5 kullanılarak geliştirilen bu proje, modern bir arayüz ile güçlü bir backend mimarisini birleştirir.

## 🎯 Projenin Amacı
Bu projenin temel amacı, araç kiralama işletmelerinin araç envanterini, müşteri verilerini ve kiralama işlemlerini merkezi bir noktadan, güvenli ve verimli bir şekilde yönetmesini sağlamaktır.

## ✨ Temel Özellikler

*   **Güvenli Kimlik Doğrulama:** Yönetici paneli için PBKDF2-HMAC-SHA256 algoritması ile şifrelenmiş giriş sistemi.
*   **Araç Envanter Yönetimi:** Araç ekleme, silme, güncelleme, kilometre takibi ve müsaitlik durumu kontrolü.
*   **Kullanıcı (Müşteri) Kaydı:** Ehliyet doğrulamalı müşteri kayıt sistemi ve kiralama geçmişi takibi.
*   **Kiralama Operasyonları:** Otomatik ücret hesaplama, kiralama başlatma ve bitirme işlemleri.
*   **Gelişmiş İstatistik Paneli:** Toplam gelir, aktif kiralamalar ve marka dağılımı gibi verilerin anlık takibi.
*   **Veri Kalıcılığı:** SQL veritabanı kurulumu gerektirmeyen, hafif ve hızlı JSON tabanlı depolama.
*   **Örnek Veri Desteği:** İlk kurulumda sistemi test etmek için otomatik olarak yüklenen örnek veriler.

## 🛠️ Teknolojiler

*   **Dil:** Python 3.x
*   **Arayüz:** PyQt5 (Modern Fusion Teması)
*   **Veri Depolama:** JSON
*   **Güvenlik:** Hashlib & HMAC (Şifre Güvenliği)

## 🚀 Kurulum ve Çalıştırma

### 1. Gereksinimler
Sisteminizde Python 3 yüklü olmalıdır. Gerekli kütüphaneyi kurmak için terminale şu komutu yazın:

```bash
pip install PyQt5
```

### 2. Çalıştırma
Proje klasörüne gidin ve uygulamayı şu komutla başlatın:

```bash
python main.py
```

### 3. Varsayılan Giriş Bilgileri
Sistem ilk kez çalıştırıldığında otomatik olarak şu hesabı oluşturur:
*   **Kullanıcı Adı:** `admin`
*   **Şifre:** `admin123`

## 📂 Proje Yapısı

*   `main.py`: Uygulamanın giriş noktası ve başlatıcı dosyası.
*   `backend/`: İş mantığı (Business Logic), modeller ve veri yönetimi sınıfları.
    *   `auth.py`: Şifreleme ve giriş işlemleri.
    *   `veri_yoneticisi.py`: JSON CRUD ve veri bütünlüğü yönetimi.
    *   `seed.py`: Test verileri oluşturucu.
*   `frontend/`: Arayüz bileşenleri, pencereler ve görsel temalar (CSS/QSS).
*   `data/`: Verilerin saklandığı JSON dosyalarının bulunduğu klasör.

## 🛡️ Güvenlik Notu
Şifreler veritabanında asla düz metin (plaintext) olarak saklanmaz. Her kullanıcıya özel rastgele bir `salt` değeri ile hash'lenerek saklanır ve zamanlama saldırılarına (timing attacks) karşı korunur.

---
*Geliştirici: Beko*