"""
Araç Paylaşım Veri Yöneticisi - Tüm modellerin merkezi yönetimi ve JSON kalıcılık.

Bu sınıf, veritabanı gibi davranarak verilerin RAM'de tutulmasını ve dosyalara yazılmasını sağlar.
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

from .arac import Arac
from .kullanici import Kullanici
from .kiralama import Kiralama


class VeriYoneticisi:
    """Araç paylaşım verilerini JSON dosyalarında yönetir."""

    def __init__(self, veri_klasoru: str = "data"):
        # Veri saklama klasörü ve dosya yolları tanımlanır
        self.veri_klasoru = veri_klasoru
        os.makedirs(veri_klasoru, exist_ok=True)

        self.araclar_dosya = os.path.join(veri_klasoru, "araclar.json")
        self.kullanicilar_dosya = os.path.join(veri_klasoru, "kullanicilar.json")
        self.kiralamalar_dosya = os.path.join(veri_klasoru, "kiralamalar.json")

        # Bellek üzerindeki veri yapıları (Hızlı erişim için Dict kullanılır)
        self._araclar: Dict[int, Arac] = {}
        self._kullanicilar: Dict[int, Kullanici] = {}
        self._kiralamalar: Dict[int, Kiralama] = {}

        # Auto-increment (Otomatik artan) ID yönetimi
        self._sonraki_arac_id = 1
        self._sonraki_kullanici_id = 1
        self._sonraki_kiralama_id = 1

        self._yukle()

    # ---------------- KALICILIK ----------------

    def _yukle(self) -> None:
        """JSON dosyalarından verileri okur ve nesneye dönüştürerek belleğe alır."""
        if os.path.exists(self.araclar_dosya):
            try:
                with open(self.araclar_dosya, "r", encoding="utf-8") as f:
                    for d in json.load(f):
                        a = Arac.from_dict(d)
                        self._araclar[a.arac_id] = a
                        self._sonraki_arac_id = max(self._sonraki_arac_id, a.arac_id + 1)
            except (json.JSONDecodeError, KeyError):
                pass

        if os.path.exists(self.kullanicilar_dosya):
            try:
                with open(self.kullanicilar_dosya, "r", encoding="utf-8") as f:
                    for d in json.load(f):
                        k = Kullanici.from_dict(d)
                        self._kullanicilar[k.kullanici_id] = k
                        self._sonraki_kullanici_id = max(self._sonraki_kullanici_id, k.kullanici_id + 1)
            except (json.JSONDecodeError, KeyError):
                pass

        if os.path.exists(self.kiralamalar_dosya):
            try:
                with open(self.kiralamalar_dosya, "r", encoding="utf-8") as f:
                    for d in json.load(f):
                        ki = Kiralama.from_dict(d)
                        self._kiralamalar[ki.kiralama_id] = ki
                        self._sonraki_kiralama_id = max(self._sonraki_kiralama_id, ki.kiralama_id + 1)
            except (json.JSONDecodeError, KeyError):
                pass

    def kaydet(self) -> None:
        """Bellekteki tüm nesneleri ilgili JSON dosyalarına seri hale getirip kaydeder."""
        with open(self.araclar_dosya, "w", encoding="utf-8") as f:
            json.dump([a.to_dict() for a in self._araclar.values()], f,
                      ensure_ascii=False, indent=2)
        with open(self.kullanicilar_dosya, "w", encoding="utf-8") as f:
            json.dump([k.to_dict() for k in self._kullanicilar.values()], f,
                      ensure_ascii=False, indent=2)
        with open(self.kiralamalar_dosya, "w", encoding="utf-8") as f:
            json.dump([ki.to_dict() for ki in self._kiralamalar.values()], f,
                      ensure_ascii=False, indent=2)

    # ---------------- ARAÇ CRUD ----------------

    def arac_ekle(self, marka: str, model: str, kilometre: int = 0,
                  saatlik_ucret: float = 100.0) -> Arac:
        """Yeni bir araç oluşturur, listeye ekler ve kaydeder."""
        arac = Arac(
            arac_id=self._sonraki_arac_id,
            marka=marka, model=model,
            kilometre=kilometre,
            saatlik_ucret=saatlik_ucret,
        )
        self._araclar[arac.arac_id] = arac
        self._sonraki_arac_id += 1
        self.kaydet()
        return arac

    def arac_guncelle(self, arac_id: int, marka: str, model: str,
                      kilometre: int, saatlik_ucret: float) -> Arac:
        """Mevcut bir aracın bilgilerini günceller."""
        arac = self._araclar.get(arac_id)
        if not arac:
            raise ValueError(f"Araç bulunamadı (ID: {arac_id}).")
        if not marka.strip():
            raise ValueError("Marka boş olamaz.")
        if not model.strip():
            raise ValueError("Model boş olamaz.")
        arac.marka = marka.strip()
        arac.model = model.strip()
        arac.kilometre = kilometre
        arac.saatlik_ucret = saatlik_ucret
        self.kaydet()
        return arac

    def arac_sil(self, arac_id: int) -> bool:
        """Bir aracı siler. Eğer araç şu an kiradaysa silinmesine izin vermez."""
        arac = self._araclar.get(arac_id)
        if not arac:
            return False
        for ki in self._kiralamalar.values():
            if ki.arac_id == arac_id and ki.aktif_mi():
                raise ValueError("Aktif kiralaması olan araç silinemez. Önce kiralama bitirilmeli.")
        del self._araclar[arac_id]
        self.kaydet()
        return True

    def arac_getir(self, arac_id: int) -> Optional[Arac]:
        """ID'ye göre araç döndürür."""
        return self._araclar.get(arac_id)

    def tum_araclar(self) -> List[Arac]:
        """Tüm araçları alfabetik (Marka Model) olarak sıralı döndürür."""
        return sorted(self._araclar.values(), key=lambda a: f"{a.marka} {a.model}".lower())

    def musait_araclar(self) -> List[Arac]:
        """Sadece kiralanabilir durumda olan araçları filtreler."""
        return [a for a in self._araclar.values() if a.musait_mi]

    # ---------------- KULLANICI CRUD ----------------

    def kullanici_ekle(self, ad: str, ehliyet_no: str) -> Kullanici:
        ehliyet = ehliyet_no.strip()
        for k in self._kullanicilar.values():
            if k.ehliyet_no == ehliyet:
                raise ValueError(f"Bu ehliyet numarası zaten kayıtlı: {ehliyet}")

        kullanici = Kullanici(
            kullanici_id=self._sonraki_kullanici_id,
            ad=ad, ehliyet_no=ehliyet,
        )
        self._kullanicilar[kullanici.kullanici_id] = kullanici
        self._sonraki_kullanici_id += 1
        self.kaydet()
        return kullanici

    def kullanici_guncelle(self, kullanici_id: int, ad: str, ehliyet_no: str) -> Kullanici:
        """Kullanıcı bilgilerini günceller, ehliyet numarasının benzersizliğini kontrol eder."""
        kullanici = self._kullanicilar.get(kullanici_id)
        if not kullanici:
            raise ValueError(f"Kullanıcı bulunamadı (ID: {kullanici_id}).")

        ehliyet = ehliyet_no.strip()
        for k in self._kullanicilar.values():
            if k.kullanici_id != kullanici_id and k.ehliyet_no == ehliyet:
                raise ValueError(f"Bu ehliyet numarası başka kullanıcıya ait: {ehliyet}")
        if not Kullanici._ehliyet_gecerli_mi(ehliyet_no):
            raise ValueError(f"Ehliyet numarası 6 haneli olmalıdır: {ehliyet_no}")

        kullanici.ad = ad.strip()
        kullanici.ehliyet_no = ehliyet
        self.kaydet()
        return kullanici

    def kullanici_sil(self, kullanici_id: int) -> bool:
        """Kullanıcıyı siler. Aktif kiralaması varsa engel olur."""
        kullanici = self._kullanicilar.get(kullanici_id)
        if not kullanici:
            return False
        for ki in self._kiralamalar.values():
            if ki.kullanici_id == kullanici_id and ki.aktif_mi():
                raise ValueError("Aktif kiralaması olan kullanıcı silinemez. Önce kiralama bitirilmeli.")
        del self._kullanicilar[kullanici_id]
        self.kaydet()
        return True

    def kullanici_getir(self, kullanici_id: int) -> Optional[Kullanici]:
        return self._kullanicilar.get(kullanici_id)

    def tum_kullanicilar(self) -> List[Kullanici]:
        return sorted(self._kullanicilar.values(), key=lambda k: k.ad.lower())

    # ---------------- KİRALAMA İŞLEMLERİ ----------------

    def kiralama_baslat(self, arac_id: int, kullanici_id: int) -> Kiralama:
        """Bir kiralama süreci başlatır. İş mantığı (Business Logic) kontrollerini yapar."""
        arac = self._araclar.get(arac_id)
        kullanici = self._kullanicilar.get(kullanici_id)

        if not arac:
            raise ValueError("Araç bulunamadı.")
        if not kullanici:
            raise ValueError("Kullanıcı bulunamadı.")
        if not arac.musait_mi:
            raise ValueError(f"'{arac.marka} {arac.model}' şu an müsait değil.")

        # Bir kullanıcının aynı anda max 1 aktif kiralaması
        for ki in self._kiralamalar.values():
            if ki.kullanici_id == kullanici_id and ki.aktif_mi():
                raise ValueError(f"'{kullanici.ad}' adlı kullanıcının zaten aktif bir kiralaması var.")

        # Atomik işlem
        arac.arac_durumu_guncelle(False)
        try:
            kiralama = Kiralama(
                kiralama_id=self._sonraki_kiralama_id,
                arac_id=arac_id,
                kullanici_id=kullanici_id,
            )
            self._kiralamalar[kiralama.kiralama_id] = kiralama
            self._sonraki_kiralama_id += 1
            self.kaydet()
        except Exception:
            arac.arac_durumu_guncelle(True)
            raise

        return kiralama

    def kiralama_bitir(self, kiralama_id: int) -> Kiralama:
        """Kiralamayı sonlandırır ve aracı tekrar müsait hale getirir."""
        kiralama = self._kiralamalar.get(kiralama_id)
        if not kiralama:
            raise ValueError("Kiralama kaydı bulunamadı.")
        if not kiralama.aktif_mi():
            raise ValueError("Bu kiralama zaten bitirilmiş.")

        arac = self._araclar.get(kiralama.arac_id)
        kiralama.kiralama_bitir()
        if arac:
            arac.arac_durumu_guncelle(True)
        self.kaydet()
        return kiralama

    def kiralama_getir(self, kiralama_id: int) -> Optional[Kiralama]:
        return self._kiralamalar.get(kiralama_id)

    def tum_kiralamalar(self) -> List[Kiralama]:
        return sorted(self._kiralamalar.values(),
                      key=lambda ki: ki.baslangic_saati, reverse=True)

    def aktif_kiralamalar(self) -> List[Kiralama]:
        return [ki for ki in self._kiralamalar.values() if ki.aktif_mi()]

    def kullanici_kiralama_gecmisi(self, kullanici_id: int) -> List[Kiralama]:
        """Belirli bir kullanıcının geçmiş ve aktif tüm kiralamalarını getirir."""
        return sorted(
            [ki for ki in self._kiralamalar.values() if ki.kullanici_id == kullanici_id],
            key=lambda ki: ki.baslangic_saati, reverse=True,
        )

    # ---------------- İSTATİSTİK ----------------
    # Dashboard ekranında kullanılacak veriler burada hesaplanır.

    def genel_istatistikler(self) -> dict:
        toplam_arac = len(self._araclar)
        musait_arac = sum(1 for a in self._araclar.values() if a.musait_mi)
        kirada_arac = toplam_arac - musait_arac

        aktif_kiralamalar = self.aktif_kiralamalar()
        tamamlanan = [ki for ki in self._kiralamalar.values() if not ki.aktif_mi()]

        toplam_gelir = 0.0
        for ki in tamamlanan:
            arac = self._araclar.get(ki.arac_id)
            if arac:
                toplam_gelir += ki.tutar(arac.saatlik_ucret)

        return {
            "toplam_arac": toplam_arac,
            "musait_arac": musait_arac,
            "kirada_arac": kirada_arac,
            "toplam_kullanici": len(self._kullanicilar),
            "aktif_kiralama": len(aktif_kiralamalar),
            "toplam_islem": len(self._kiralamalar),
            "toplam_gelir": round(toplam_gelir, 2),
        }

    def marka_dagilim(self) -> dict:
        """Araçların markalara göre dağılımı."""
        dagilim = {}
        for a in self._araclar.values():
            dagilim[a.marka] = dagilim.get(a.marka, 0) + 1
        return dagilim
