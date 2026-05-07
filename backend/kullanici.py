"""
Sistemdeki müşterileri (kullanıcıları) temsil eden modül.
"""
import re


class Kullanici:
    """
    Araç paylaşım sistemindeki bir kullanıcıyı temsil eder.

    Attributes:
        kullanici_id (int)
        ad (str)
        ehliyet_no (str): 6 haneli
    """

    EHLIYET_REGEX = re.compile(r"^\d{6}$")  # Sadece 6 rakamdan oluşan ehliyet formatı

    def __init__(self, kullanici_id: int, ad: str, ehliyet_no: str):
        # Ad ve Ehliyet No için temel doğrulamalar
        if not ad or not ad.strip():
            raise ValueError("Kullanıcı adı boş olamaz.")
        if not self._ehliyet_gecerli_mi(ehliyet_no):
            raise ValueError(f"Ehliyet numarası 6 haneli olmalıdır: {ehliyet_no}")

        self.kullanici_id = kullanici_id
        self.ad = ad.strip()
        self.ehliyet_no = ehliyet_no.strip()

    @staticmethod
    def _ehliyet_gecerli_mi(ehliyet_no: str) -> bool:
        """Ehliyet numarasının regex formatına uygunluğunu denetler."""
        if not ehliyet_no or not isinstance(ehliyet_no, str):
            return False
        return bool(Kullanici.EHLIYET_REGEX.match(ehliyet_no.strip()))

    def kiralama_gecmisi(self, tum_kiralamalar: list) -> list:
        """Verilen kiralama listesi içinden sadece bu kullanıcıya ait olanları döndürür."""
        return [k for k in tum_kiralamalar if k.kullanici_id == self.kullanici_id]

    def to_dict(self) -> dict:
        """Kullanıcı verilerini JSON uyumlu bir sözlüğe çevirir."""
        return {
            "kullanici_id": self.kullanici_id,
            "ad": self.ad,
            "ehliyet_no": self.ehliyet_no,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Kullanici":
        """Sözlükten Kullanici nesnesi türetir."""
        return cls(
            kullanici_id=d["kullanici_id"],
            ad=d["ad"],
            ehliyet_no=d["ehliyet_no"],
        )

    def __repr__(self) -> str:
        return f"Kullanici(id={self.kullanici_id}, ad='{self.ad}')"
