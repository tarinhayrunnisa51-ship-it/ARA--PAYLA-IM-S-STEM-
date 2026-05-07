"""
Otomatik seed - Boş veritabanını örnek araç, kullanıcı ve kiralama ile doldurur.
"""
from datetime import datetime, timedelta

from .veri_yoneticisi import VeriYoneticisi


def seed_gerekli_mi(vy: VeriYoneticisi) -> bool:
    return (
        len(vy.tum_araclar()) == 0
        and len(vy.tum_kullanicilar()) == 0
        and len(vy.tum_kiralamalar()) == 0
    )


def seed_uygula(vy: VeriYoneticisi) -> None:
    """Boş bir VeriYoneticisi'ye örnek araç paylaşım verileri yükler."""

    # ARAÇLAR (10 tane)
    araclar = [
        ("Renault", "Clio", 45000, 90.0),
        ("Volkswagen", "Polo", 32000, 110.0),
        ("Fiat", "Egea", 58000, 85.0),
        ("Toyota", "Corolla", 27000, 150.0),
        ("Hyundai", "i20", 61000, 80.0),
        ("Ford", "Focus", 73000, 120.0),
        ("Peugeot", "301", 89000, 95.0),
        ("Honda", "Civic", 15000, 180.0),
        ("Dacia", "Duster", 42000, 100.0),
        ("Skoda", "Fabia", 110000, 85.0),
    ]
    arac_objs = [
        vy.arac_ekle(marka, model, km, ucret)
        for marka, model, km, ucret in araclar
    ]

    # KULLANICILAR (8 kişi)
    kullanicilar = [
        ("Beko Yılmaz", "482916"),
        ("Ali Demir", "317582"),
        ("Ayşe Kaya", "624871"),
        ("Mehmet Şahin", "195437"),
        ("Zeynep Arslan", "738264"),
        ("Can Öztürk", "561923"),
        ("Selin Yıldız", "843617"),
        ("Murat Koç", "279548"),
    ]
    kullanici_objs = [
        vy.kullanici_ekle(ad, ehliyet)
        for ad, ehliyet in kullanicilar
    ]

    # KİRALAMALAR (12 tane: 4 aktif, 8 tamamlanmış)
    # ÖNCELİK: Tamamlananlar önce (yoksa max 1 aktif kuralı engeller)
    kiralama_planlari = [
        # (arac_idx, kullanici_idx, kac_saat_once_basladi, bitti_mi, kac_saat_sonra_bitti)
        # TAMAMLANMIŞ (8 tane) — önce bunlar oluşturulmalı
        (8, 0, 168, True, 5),       # Dacia Duster - Beko, 7 gün önce, 5 saat
        (9, 1, 240, True, 2),       # Skoda Fabia - Ali, 10 gün önce, 2 saat
        (0, 3, 336, True, 7),       # Renault Clio - Mehmet, 14 gün önce, 7 saat
        (1, 5, 480, True, 4),       # VW Polo - Can, 20 gün önce, 4 saat
        (2, 4, 72, True, 4),        # Fiat Egea - Zeynep, 3 gün önce, 4 saat
        (4, 5, 48, True, 6),        # Hyundai i20 - Can, 2 gün önce, 6 saat
        (5, 6, 120, True, 3),       # Ford Focus - Selin, 5 gün önce, 3 saat
        (6, 7, 96, True, 8),        # Peugeot 301 - Murat, 4 gün önce, 8 saat

        # AKTİF (4 tane) — en son
        (0, 0, 3, False, None),     # Renault Clio - Beko, 3 saat önce
        (1, 1, 2, False, None),     # VW Polo - Ali, 2 saat önce
        (3, 2, 5, False, None),     # Toyota Corolla - Ayşe, 5 saat önce
        (7, 3, 1, False, None),     # Honda Civic - Mehmet, 1 saat önce
    ]

    simdi = datetime.now()

    for plan in kiralama_planlari:
        arac_idx, kullanici_idx, kac_saat_once, bitti, kac_saat_sonra = plan
        arac = arac_objs[arac_idx]
        kullanici = kullanici_objs[kullanici_idx]

        if not arac.musait_mi:
            continue

        try:
            kiralama = vy.kiralama_baslat(arac.arac_id, kullanici.kullanici_id)
        except ValueError:
            continue

        # Tarihleri geriye al
        kiralama.baslangic_saati = simdi - timedelta(hours=kac_saat_once)

        if bitti and kac_saat_sonra is not None:
            kiralama.bitis_saati = kiralama.baslangic_saati + timedelta(hours=kac_saat_sonra)
            arac.musait_mi = True

    vy.kaydet()
