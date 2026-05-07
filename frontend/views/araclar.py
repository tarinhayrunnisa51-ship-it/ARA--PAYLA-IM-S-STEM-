"""
Araclar Sayfasi - Editorial dergi grid.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFrame,
    QMessageBox,
    QLineEdit,
    QComboBox,
    QScrollArea,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader,
    AracGorseli,
    Rozet,
)
from frontend.widgets.diyaloglar import AracDiyalog


class AraclarSayfasi(QWidget):
    veri_degisti = pyqtSignal()

    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        # Üst bar
        ust_bar = QWidget()
        ust_bar.setStyleSheet("background-color: #0f172a;")
        ust_layout = QVBoxLayout(ust_bar)
        ust_layout.setContentsMargins(48, 36, 48, 24)
        ust_layout.setSpacing(20)

        header_satir = QHBoxLayout()
        header_satir.setSpacing(20)

        self.header = EditorialHeader(
            kategori="ARACLAR",
            baslik="Araclar",
            altyazi="Tum araclar — marka sirasina gore.",
            sag_etiket="FILO",
        )
        header_satir.addWidget(self.header, 1)

        ekle_btn = QPushButton("+  YENI ARAC")
        ekle_btn.setObjectName("PrimaryButon")
        ekle_btn.setStyleSheet(
            "QPushButton { background-color: #3b82f6; color: #f1f5f9; "
            "border: 1px solid #3b82f6; border-radius: 6px; "
            "padding: 0 28px; font-family: 'Segoe UI', sans-serif; "
            "font-size: 12px; font-weight: 700; letter-spacing: 1px; } "
            "QPushButton:hover { background-color: #2563eb; "
            "border: 1px solid #2563eb; }"
        )
        ekle_btn.setFixedHeight(46)
        ekle_btn.setMinimumWidth(170)
        ekle_btn.setCursor(Qt.PointingHandCursor)
        ekle_btn.clicked.connect(self._ekle)

        btn_sarici = QVBoxLayout()
        btn_sarici.addStretch()
        btn_sarici.addWidget(ekle_btn)
        btn_sarici.addSpacing(20)
        header_satir.addLayout(btn_sarici)

        ust_layout.addLayout(header_satir)

        # Filtre satırı
        filtre = QHBoxLayout()
        filtre.setSpacing(12)

        self.arama = QLineEdit()
        self.arama.setObjectName("AramaInput")
        self.arama.setPlaceholderText("ARA  ·  Marka veya model...")
        self.arama.setFixedHeight(44)
        self.arama.textChanged.connect(self.yenile)
        filtre.addWidget(self.arama, 1)

        self.durum_filtre = QComboBox()
        self.durum_filtre.addItem("TUM DURUMLAR", "tumu")
        self.durum_filtre.addItem("MUSAIT", "musait")
        self.durum_filtre.addItem("KIRADA", "kirada")
        self.durum_filtre.setFixedHeight(44)
        self.durum_filtre.setMinimumWidth(180)
        self.durum_filtre.currentIndexChanged.connect(self.yenile)
        filtre.addWidget(self.durum_filtre)

        ust_layout.addLayout(filtre)

        self.sayim_lbl = QLabel("")
        self.sayim_lbl.setStyleSheet(
            "color: #64748b; font-family: 'Inter', sans-serif; "
            "font-size: 10px; font-weight: 700; letter-spacing: 2px; "
            "background: transparent; border: none;"
        )
        ust_layout.addWidget(self.sayim_lbl)

        ana.addWidget(ust_bar)

        # Scroll içeriği
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setStyleSheet("background-color: #1e293b; border: none;")

        self.icerik = QWidget()
        self.scroll.setWidget(self.icerik)
        self.grid = QGridLayout(self.icerik)
        self.grid.setContentsMargins(48, 24, 48, 36)
        self.grid.setSpacing(16)
        self.grid.setAlignment(Qt.AlignTop)

        ana.addWidget(self.scroll, 1)

    def yenile(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()

        filtre = self.arama.text().strip().lower()
        durum_filtre = self.durum_filtre.currentData()

        araclar = self.vy.tum_araclar()

        if filtre:
            araclar = [
                a for a in araclar
                if filtre in a.marka.lower()
                or filtre in a.model.lower()
            ]

        if durum_filtre == "musait":
            araclar = [a for a in araclar if a.musait_mi]
        elif durum_filtre == "kirada":
            araclar = [a for a in araclar if not a.musait_mi]

        toplam = len(araclar)
        musait = sum(1 for a in araclar if a.musait_mi)
        self.sayim_lbl.setText(
            f"{toplam} ARAC  ·  {musait} MUSAIT  ·  {toplam - musait} KIRADA"
        )

        if not araclar:
            bos = QLabel("— Aranan olcutlerde arac bulunamadi. —")
            bos.setStyleSheet(
                "color: #64748b; font-family: 'Segoe UI', sans-serif; "
                "font-size: 16px; font-style: italic; padding: 60px; "
                "background: transparent; border: none;"
            )
            bos.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(bos, 0, 0, 1, 4)
            return

        cols = 4
        for i, a in enumerate(araclar):
            row = i // cols
            col = i % cols
            kart = self._arac_karti(a)
            self.grid.addWidget(kart, row, col)

        for c in range(cols):
            self.grid.setColumnStretch(c, 1)

        n_satir = (len(araclar) + cols - 1) // cols
        for r in range(n_satir):
            self.grid.setRowMinimumHeight(r, 340)

    def _arac_karti(self, arac) -> QFrame:
        kart = QFrame()
        kart.setStyleSheet(
            "QFrame { background-color: #1e293b; "
            "border: 1px solid #334155; border-radius: 6px; }"
        )
        kart.setMinimumHeight(320)
        kart.setMaximumHeight(320)

        ana = QVBoxLayout(kart)
        ana.setContentsMargins(18, 18, 18, 18)
        ana.setSpacing(10)

        # Görsel ortalanmış
        gorsel_sarici_w = QWidget()
        gorsel_sarici_w.setFixedHeight(125)
        gorsel_sarici = QHBoxLayout(gorsel_sarici_w)
        gorsel_sarici.setContentsMargins(0, 0, 0, 0)
        gorsel_sarici.addStretch()
        gorsel = AracGorseli(arac.marka, arac.model, arac.musait_mi)
        gorsel_sarici.addWidget(gorsel)
        gorsel_sarici.addStretch()
        ana.addWidget(gorsel_sarici_w)

        # Hairline
        hr = QFrame()
        hr.setFixedHeight(1)
        hr.setStyleSheet("background-color: #334155;")
        ana.addWidget(hr)

        # Marka tag
        kat = QLabel(arac.marka.upper())
        kat.setStyleSheet(
            "color: #3b82f6; font-family: 'Inter', sans-serif; "
            "font-size: 9px; font-weight: 800; letter-spacing: 2px; "
            "background: transparent; border: none;"
        )
        ana.addWidget(kat)

        # Model
        model_lbl = QLabel(f"{arac.marka} {arac.model}")
        model_lbl.setWordWrap(True)
        model_lbl.setMaximumHeight(40)
        model_lbl.setStyleSheet(
            "color: #f1f5f9; "
            "font-family: 'Segoe UI', sans-serif; "
            "font-size: 15px; font-weight: 800; letter-spacing: -0.2px; "
            "background: transparent; border: none;"
        )
        ana.addWidget(model_lbl)

        # Km + Ücret
        detay = QLabel(f"{arac.kilometre:,} km  ·  {arac.saatlik_ucret:.0f} TL/saat")
        detay.setStyleSheet(
            "color: #64748b; "
            "font-family: 'Inter', sans-serif; "
            "font-size: 11px; "
            "background: transparent; border: none;"
        )
        ana.addWidget(detay)

        ana.addStretch()

        # Alt buton satırı
        alt = QHBoxLayout()
        alt.setSpacing(6)

        duzen_btn = QPushButton("DUZENLE")
        duzen_btn.setObjectName("KucukIkincilButon")
        duzen_btn.setFixedHeight(30)
        duzen_btn.setCursor(Qt.PointingHandCursor)
        duzen_btn.clicked.connect(
            lambda _, aid=arac.arac_id: self._duzenle(aid)
        )

        sil_btn = QPushButton("SIL")
        sil_btn.setObjectName("KucukTehlikeButon")
        sil_btn.setFixedHeight(30)
        sil_btn.setFixedWidth(60)
        sil_btn.setCursor(Qt.PointingHandCursor)
        sil_btn.clicked.connect(lambda _, aid=arac.arac_id: self._sil(aid))

        alt.addWidget(duzen_btn, 1)
        alt.addWidget(sil_btn)
        ana.addLayout(alt)

        return kart

    def _ekle(self):
        d = AracDiyalog(self.vy, parent=self)
        if d.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _duzenle(self, arac_id: int):
        a = self.vy.arac_getir(arac_id)
        if not a:
            return
        d = AracDiyalog(self.vy, arac=a, parent=self)
        if d.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _sil(self, arac_id: int):
        a = self.vy.arac_getir(arac_id)
        if not a:
            return
        cevap = QMessageBox.question(
            self, "Araci Sil",
            f"'{a.marka} {a.model}' kaydini silmek istediginizden emin misiniz?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            try:
                self.vy.arac_sil(arac_id)
                self.yenile()
                self.veri_degisti.emit()
            except ValueError as e:
                QMessageBox.warning(self, "Silinemedi", str(e))
