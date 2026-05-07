"""
Araç ve kullanıcı arasındaki kiralama işlemini temsil eden modül.
"""
from datetime import datetime


class Kiralama:
    """
    Bir kiralama işlemi kaydını temsil eder.

    Attributes:
        kiralama_id (int)
        arac_id (int)
        kullanici_id (int)
        baslangic_saati (datetime)
        bitis_saati (datetime | None): None = henüz aktif
    """

    def __init__(self, kiralama_id: int, arac_id: int, kullanici_id: int,
                 baslangic_saati: datetime = None,
                 bitis_saati: datetime = None):
        self.kiralama_id = kiralama_id
        self.arac_id = arac_id
        self.kullanici_id = kullanici_id
        self.baslangic_saati = baslangic_saati or datetime.now()
        self.bitis_saati = bitis_saati

    def kiralama_baslat(self) -> None:
        """Kiralama başlangıç anını kaydeder."""
        self.baslangic_saati = datetime.now()

    def kiralama_bitir(self) -> None:
        """Kiralamayı sonlandırır ve bitiş saatini atar."""
        if self.bitis_saati is not None:
            raise ValueError("Bu kiralama zaten bitirilmiş.")
        self.bitis_saati = datetime.now()

    def aktif_mi(self) -> bool:
        """Kiralama işleminin hala devam edip etmediğini döndürür."""
        return self.bitis_saati is None

    def sure_saat(self) -> float:
        """Kiralama süresi saat cinsinden. Aktifse şu ana kadar."""
        bitis = self.bitis_saati or datetime.now()
        delta = bitis - self.baslangic_saati
        return delta.total_seconds() / 3600

    def tutar(self, saatlik_ucret: float) -> float:
        """Kiralama süresine göre ödenecek toplam tutarı hesaplar."""
        return self.sure_saat() * saatlik_ucret

    def kiralama_bilgisi(self) -> dict:
        """Frontend arayüzü için genişletilmiş kiralama bilgilerini döndürür."""
        return {
            "kiralama_id": self.kiralama_id,
            "arac_id": self.arac_id,
            "kullanici_id": self.kullanici_id,
            "baslangic": self.baslangic_saati.isoformat(),
            "bitis": self.bitis_saati.isoformat() if self.bitis_saati else None,
            "sure_saat": round(self.sure_saat(), 2),
            "aktif": self.aktif_mi(),
        }

    def to_dict(self) -> dict:
        """Verileri JSON formatına uygun sözlüğe çevirir (Tarihler ISO formatına çevrilir)."""
        return {
            "kiralama_id": self.kiralama_id,
            "arac_id": self.arac_id,
            "kullanici_id": self.kullanici_id,
            "baslangic_saati": self.baslangic_saati.isoformat(),
            "bitis_saati": self.bitis_saati.isoformat() if self.bitis_saati else None,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Kiralama":
        """Sözlükten kiralama nesnesi oluşturur (ISO tarihlerini datetime nesnesine geri çevirir)."""
        return cls(
            kiralama_id=d["kiralama_id"],
            arac_id=d["arac_id"],
            kullanici_id=d["kullanici_id"],
            baslangic_saati=datetime.fromisoformat(d["baslangic_saati"]),
            bitis_saati=(datetime.fromisoformat(d["bitis_saati"])
                         if d.get("bitis_saati") else None),
        )

    def __repr__(self) -> str:
        durum = "aktif" if self.aktif_mi() else "tamamlandı"
        return f"Kiralama(id={self.kiralama_id}, arac={self.arac_id}, kullanici={self.kullanici_id}, {durum})"
