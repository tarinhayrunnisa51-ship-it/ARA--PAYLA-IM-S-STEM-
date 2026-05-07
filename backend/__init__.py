"""
Backend paketi - Araç Paylaşım Sistemi

Bu paket, sistemin temel iş mantığını, veri yönetimini, 
kimlik doğrulama süreçlerini ve veri modellerini içerir.
"""
from .arac import Arac
from .kullanici import Kullanici
from .kiralama import Kiralama
from .veri_yoneticisi import VeriYoneticisi
from .seed import seed_gerekli_mi, seed_uygula
from .auth import AuthYoneticisi, SistemKullanici

# Diğer modüllerden kolay erişim için dışa aktarılan sınıflar ve fonksiyonlar
__all__ = [
    "Arac", "Kullanici", "Kiralama", "VeriYoneticisi",
    "seed_gerekli_mi", "seed_uygula",
    "AuthYoneticisi", "SistemKullanici",
]
