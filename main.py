"""
DriveShare - Arac Paylasim Sistemi
====================================

Calistirma:
    python main.py

Gereksinimler:
    pip install PyQt5

Varsayilan Giris:
    Kullanici adi: admin
    Sifre:        admin123

Gelistirici: Beko
"""
import sys
import os

from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from backend import (
    VeriYoneticisi,
    AuthYoneticisi,
    seed_gerekli_mi,
    seed_uygula,
)
from frontend.ana_pencere import AnaPencere
from frontend.login import LoginPenceresi


def main():
    # Yüksek DPI ekranlar için ölçeklendirme desteği
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("DriveShare - Arac Paylasim")
    app.setStyle("Fusion") # İşletim sisteminden bağımsız modern görünüm

    # Global tema ayarları
    from frontend.tema import ANA_STIL
    app.setStyleSheet(ANA_STIL)

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Veri klasörü kontrolü (Proje dizininde 'data' klasörü)
    veri_klasoru = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data"
    )
    os.makedirs(veri_klasoru, exist_ok=True)

    # Kimlik Doğrulama Yönetimi
    # İlk çalıştırmada sistemde hiç kullanıcı yoksa varsayılan admini oluşturur.
    auth = AuthYoneticisi(os.path.join(veri_klasoru, "sistem_kullanicilari.json"))
    if not auth.kullanici_var_mi():
        auth.varsayilan_kullanici_olustur()
        print("[Auth] Varsayilan kullanici olusturuldu (admin / admin123)")

    # Login
    login = LoginPenceresi(auth)
    if login.exec_() != QDialog.Accepted:
        sys.exit(0)

    aktif_kullanici = login.dogrulanan_kullanici
    print(f"[Auth] Giris basarili: {aktif_kullanici.ad}")

    # Veri yoneticisi
    # JSON dosyalarını yöneten ana sınıfın başlatılması
    vy = VeriYoneticisi(veri_klasoru=veri_klasoru)

    # Eğer veritabanı boşsa test verilerini (Seed) yükle
    if seed_gerekli_mi(vy):
        print("[Seed] Veritabani bos, ornek veriler yukleniyor...")
        seed_uygula(vy)
        print(f"[Seed] {len(vy.tum_araclar())} arac, "
              f"{len(vy.tum_kullanicilar())} kullanici, "
              f"{len(vy.tum_kiralamalar())} kiralama kaydi eklendi.")

    # Ana pencereyi başlat
    pencere = AnaPencere(vy, aktif_kullanici=aktif_kullanici)
    pencere.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
