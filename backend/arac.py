"""
Araç modelini temsil eden modül.
"""


class Arac:
    """
    Araç paylaşım sistemindeki bir aracı temsil eder.

    Attributes:
        arac_id (int)
        marka (str)
        model (str)
        kilometre (int)
        musait_mi (bool)
        saatlik_ucret (float)
    """

    def __init__(self, arac_id: int, marka: str, model: str,
                 kilometre: int = 0, musait_mi: bool = True,
                 saatlik_ucret: float = 100.0):
        # Veri bütünlüğü için girdi kontrolleri (Validation)
        if not marka or not marka.strip():
            raise ValueError("Marka boş olamaz.")
        if not model or not model.strip():
            raise ValueError("Model boş olamaz.")
        if kilometre < 0:
            raise ValueError("Kilometre negatif olamaz.")
        if saatlik_ucret < 0:
            raise ValueError("Saatlik ücret negatif olamaz.")

        self.arac_id = arac_id
        self.marka = marka.strip()  # Gereksiz boşlukları temizle
        self.model = model.strip()  # Gereksiz boşlukları temizle
        self.kilometre = kilometre
        self.musait_mi = musait_mi  # Aracın kiralanabilir olup olmadığını belirtir
        self.saatlik_ucret = saatlik_ucret

    def arac_durumu_guncelle(self, yeni_durum: bool) -> None:
        """Aracın müsaitlik durumunu değiştirir (Örn: kiralandığında False yapılır)."""
        self.musait_mi = yeni_durum

    def kilometre_guncelle(self, yeni_km: int) -> None:
        """Aracın katettiği toplam yolu günceller."""
        if yeni_km < 0:
            raise ValueError("Kilometre negatif olamaz.")
        self.kilometre = yeni_km

    def to_dict(self) -> dict:
        """Nesneyi JSON formatında saklanabilmesi için sözlük yapısına dönüştürür."""
        return {
            "arac_id": self.arac_id,
            "marka": self.marka,
            "model": self.model,
            "kilometre": self.kilometre,
            "musait_mi": self.musait_mi,
            "saatlik_ucret": self.saatlik_ucret,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Arac":
        """Sözlük yapısından yeni bir Arac nesnesi oluşturur (Deserialization)."""
        return cls(
            arac_id=d["arac_id"],
            marka=d["marka"],
            model=d["model"],
            kilometre=d.get("kilometre", 0),
            musait_mi=d.get("musait_mi", True),
            saatlik_ucret=d.get("saatlik_ucret", 100.0),
        )

    def __repr__(self) -> str:
        """Nesnenin debug/konsol çıktısını daha anlamlı hale getirir."""
        durum = "müsait" if self.musait_mi else "kirada"
        return f"Arac(id={self.arac_id}, {self.marka} {self.model}, {durum})"
