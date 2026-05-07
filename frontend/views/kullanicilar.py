"""
Kullanicilar Sayfasi - Editorial liste.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QMessageBox,
    QLineEdit,
    QFrame,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader,
    MuhurAvatar,
    Rozet,
    HucreSarmalayici,
    ButonGrubu,
)
from frontend.widgets.diyaloglar import KullaniciDiyalog


class _KullaniciHucresi(QWidget):
    """Avatar muhur + ad + ehliyet birlesik hucre."""

    def __init__(self, ad: str, ehliyet_no: str, kid: int, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(14)

        layout.addWidget(MuhurAvatar(ad, boyut=40))

        bilgi = QVBoxLayout()
        bilgi.setSpacing(2)
        bilgi.setContentsMargins(0, 0, 0, 0)

        ad_lbl = QLabel(ad)
        ad_lbl.setStyleSheet(
            "color: #f1f5f9; "
            "font-family: 'Segoe UI', sans-serif; "
            "font-weight: 800; font-size: 14px; "
            "background: transparent; border: none;"
        )

        meta_lbl = QLabel(
            f"<span style=\"color:#475569; font-family:'Inter',sans-serif; "
            f"font-size:10px; font-weight:700; letter-spacing:1.5px;\">"
            f"#{kid:03d}  ·  </span>"
            f"<span style=\"color:#64748b; font-family:'Inter',sans-serif; "
            f"font-size:11px;\">Ehliyet: {ehliyet_no}</span>"
        )
        meta_lbl.setStyleSheet("background: transparent; border: none;")

        bilgi.addWidget(ad_lbl)
        bilgi.addWidget(meta_lbl)

        layout.addLayout(bilgi)
        layout.addStretch()


class KullanicilarSayfasi(QWidget):
    veri_degisti = pyqtSignal()

    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(48, 36, 48, 32)
        ana.setSpacing(20)

        header_satir = QHBoxLayout()
        header_satir.setSpacing(20)

        self.header = EditorialHeader(
            kategori="KULLANICILAR",
            baslik="Kullanicilar",
            altyazi="Sisteme kayitli tum kullanicilar.",
            sag_etiket="LISTE",
        )
        header_satir.addWidget(self.header, 1)

        ekle_btn = QPushButton("+  YENI KULLANICI")
        ekle_btn.setStyleSheet(
            "QPushButton { background-color: #3b82f6; color: #f1f5f9; "
            "border: 1px solid #3b82f6; border-radius: 6px; "
            "padding: 0 28px; font-family: 'Segoe UI', sans-serif; "
            "font-size: 12px; font-weight: 700; letter-spacing: 1px; } "
            "QPushButton:hover { background-color: #2563eb; "
            "border: 1px solid #2563eb; }"
        )
        ekle_btn.setFixedHeight(46)
        ekle_btn.setMinimumWidth(190)
        ekle_btn.setCursor(Qt.PointingHandCursor)
        ekle_btn.clicked.connect(self._ekle)

        btn_sarici = QVBoxLayout()
        btn_sarici.addStretch()
        btn_sarici.addWidget(ekle_btn)
        btn_sarici.addSpacing(20)
        header_satir.addLayout(btn_sarici)

        ana.addLayout(header_satir)

        # Arama
        self.arama = QLineEdit()
        self.arama.setObjectName("AramaInput")
        self.arama.setPlaceholderText("ARA  ·  Isim veya ehliyet no...")
        self.arama.setFixedHeight(44)
        self.arama.textChanged.connect(self.yenile)
        ana.addWidget(self.arama)

        # Tablo
        self.tablo = QTableWidget(0, 3)
        self.tablo.setHorizontalHeaderLabels(["KULLANICI", "AKTIF KIRALAMA", "ISLEMLER"])
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablo.setShowGrid(False)
        self.tablo.setFocusPolicy(Qt.NoFocus)
        self.tablo.setAlternatingRowColors(True)

        h = self.tablo.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.Stretch)
        h.setSectionResizeMode(1, QHeaderView.Fixed)
        h.setSectionResizeMode(2, QHeaderView.Fixed)
        self.tablo.setColumnWidth(1, 170)
        self.tablo.setColumnWidth(2, 220)

        ana.addWidget(self.tablo, 1)

    def yenile(self):
        filtre = self.arama.text().strip().lower()
        kullanicilar = [
            k for k in self.vy.tum_kullanicilar()
            if filtre in k.ad.lower() or filtre in k.ehliyet_no
        ]

        aktif_sayilari = {}
        for ki in self.vy.aktif_kiralamalar():
            aktif_sayilari[ki.kullanici_id] = aktif_sayilari.get(ki.kullanici_id, 0) + 1

        self.tablo.setRowCount(len(kullanicilar))

        for satir, k in enumerate(kullanicilar):
            self.tablo.setCellWidget(
                satir, 0,
                _KullaniciHucresi(k.ad, k.ehliyet_no, k.kullanici_id)
            )

            aktif_n = aktif_sayilari.get(k.kullanici_id, 0)
            if aktif_n > 0:
                rozet = Rozet(f"{aktif_n} KIRALAMA", "basari")
            else:
                rozet = Rozet("YOK", "notr")
            self.tablo.setCellWidget(satir, 1, HucreSarmalayici(rozet))

            duzen_btn = QPushButton("DUZENLE")
            duzen_btn.setObjectName("KucukIkincilButon")
            duzen_btn.setFixedHeight(30)
            duzen_btn.setFixedWidth(94)
            duzen_btn.setCursor(Qt.PointingHandCursor)
            duzen_btn.clicked.connect(
                lambda _, kid=k.kullanici_id: self._duzenle(kid)
            )

            sil_btn = QPushButton("SIL")
            sil_btn.setObjectName("KucukTehlikeButon")
            sil_btn.setFixedHeight(30)
            sil_btn.setFixedWidth(56)
            sil_btn.setCursor(Qt.PointingHandCursor)
            sil_btn.clicked.connect(lambda _, kid=k.kullanici_id: self._sil(kid))

            self.tablo.setCellWidget(satir, 2, ButonGrubu([duzen_btn, sil_btn]))
            self.tablo.setRowHeight(satir, 64)

    def _ekle(self):
        d = KullaniciDiyalog(self.vy, parent=self)
        if d.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _duzenle(self, kullanici_id: int):
        k = self.vy.kullanici_getir(kullanici_id)
        if not k:
            return
        d = KullaniciDiyalog(self.vy, kullanici=k, parent=self)
        if d.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _sil(self, kullanici_id: int):
        k = self.vy.kullanici_getir(kullanici_id)
        if not k:
            return
        cevap = QMessageBox.question(
            self, "Kullaniciyi Sil",
            f"'{k.ad}' adli kullaniciyi silmek istediginizden emin misiniz?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            try:
                self.vy.kullanici_sil(kullanici_id)
                self.yenile()
                self.veri_degisti.emit()
            except ValueError as e:
                QMessageBox.warning(self, "Silinemedi", str(e))
