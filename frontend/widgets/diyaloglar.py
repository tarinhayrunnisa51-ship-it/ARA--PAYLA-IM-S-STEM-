"""
Diyalog pencereleri - Editorial.
"""
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QPushButton,
    QMessageBox,
    QFrame,
    QDoubleSpinBox,
)
from PyQt5.QtCore import Qt

from backend import VeriYoneticisi, Arac, Kullanici


def _form_satiri(etiket_metni: str, alan_widget) -> QVBoxLayout:
    layout = QVBoxLayout()
    layout.setSpacing(8)
    layout.setContentsMargins(0, 0, 0, 0)

    etiket = QLabel(etiket_metni.upper())
    etiket.setObjectName("FormEtiket")

    alan_widget.setMinimumHeight(42)

    layout.addWidget(etiket)
    layout.addWidget(alan_widget)
    return layout


def _diyalog_butonlari(iptal_metin="IPTAL", kaydet_metin="KAYDET"):
    iptal_btn = QPushButton(iptal_metin)
    iptal_btn.setObjectName("HayaletButon")
    iptal_btn.setFixedHeight(42)
    iptal_btn.setMinimumWidth(110)
    iptal_btn.setCursor(Qt.PointingHandCursor)

    kaydet_btn = QPushButton(kaydet_metin)
    kaydet_btn.setObjectName("PrimaryButon")
    kaydet_btn.setStyleSheet(
        "QPushButton { background-color: #3b82f6; color: #f1f5f9; "
        "border: 1px solid #3b82f6; border-radius: 6px; "
        "padding: 0 28px; font-family: 'Segoe UI', sans-serif; "
        "font-size: 12px; font-weight: 700; letter-spacing: 1px; } "
        "QPushButton:hover { background-color: #2563eb; "
        "border: 1px solid #2563eb; }"
    )
    kaydet_btn.setFixedHeight(42)
    kaydet_btn.setMinimumWidth(140)
    kaydet_btn.setCursor(Qt.PointingHandCursor)

    return iptal_btn, kaydet_btn


def _editorial_baslik(metin: str, kategori: str = "EDITORYAL") -> QVBoxLayout:
    l = QVBoxLayout()
    l.setSpacing(8)
    l.setContentsMargins(0, 0, 0, 0)

    kat = QLabel(kategori)
    kat.setStyleSheet(
        "color: #3b82f6; font-family: 'Inter', sans-serif; "
        "font-size: 9px; font-weight: 800; letter-spacing: 2.5px; "
        "background: transparent; border: none;"
    )
    l.addWidget(kat)

    bl = QLabel(metin)
    bl.setStyleSheet(
        "color: #f1f5f9; font-family: 'Segoe UI', sans-serif; "
        "font-size: 28px; font-weight: 900; letter-spacing: -0.5px; "
        "background: transparent; border: none;"
    )
    l.addWidget(bl)

    cizgi = QFrame()
    cizgi.setFixedHeight(2)
    cizgi.setStyleSheet("background-color: #3b82f6;")
    l.addWidget(cizgi)

    return l


class AracDiyalog(QDialog):
    def __init__(self, vy: VeriYoneticisi, arac: Arac = None, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.arac = arac
        self.duzenleme_modu = arac is not None

        self.setWindowTitle("Yeni Arac")
        self.setMinimumWidth(520)
        self.setModal(True)

        self._arayuz_olustur()
        if self.duzenleme_modu:
            self._mevcut_verileri_yukle()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(36, 32, 36, 28)
        ana.setSpacing(24)

        baslik = "Araci Duzenle" if self.duzenleme_modu else "Yeni Arac"
        kategori = "DUZENLE" if self.duzenleme_modu else "YENI ARAC"
        ana.addLayout(_editorial_baslik(baslik, kategori))

        aciklama = QLabel(
            "Tum alanlar zorunludur. Saatlik ucret TL cinsindendir."
        )
        aciklama.setStyleSheet(
            "color: #64748b; font-family: 'Segoe UI', sans-serif; "
            "font-size: 13px; font-style: italic; "
            "background: transparent; border: none;"
        )
        aciklama.setWordWrap(True)
        ana.addWidget(aciklama)

        self.marka_input = QLineEdit()
        self.marka_input.setPlaceholderText("Orn: Volkswagen")
        self.marka_input.returnPressed.connect(lambda: self.model_input.setFocus())

        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("Orn: Polo")
        self.model_input.returnPressed.connect(self._kaydet)

        self.km_input = QSpinBox()
        self.km_input.setRange(0, 999999)
        self.km_input.setSuffix(" km")
        self.km_input.setValue(0)

        self.ucret_input = QDoubleSpinBox()
        self.ucret_input.setRange(0, 9999)
        self.ucret_input.setSuffix(" TL/saat")
        self.ucret_input.setValue(100.0)
        self.ucret_input.setDecimals(0)

        ana.addLayout(_form_satiri("Marka", self.marka_input))
        ana.addLayout(_form_satiri("Model", self.model_input))
        ana.addLayout(_form_satiri("Kilometre", self.km_input))
        ana.addLayout(_form_satiri("Saatlik Ucret", self.ucret_input))

        ana.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        iptal_btn, kaydet_btn = _diyalog_butonlari(
            kaydet_metin="GUNCELLE" if self.duzenleme_modu else "ARACI EKLE"
        )
        iptal_btn.clicked.connect(self.reject)
        kaydet_btn.clicked.connect(self._kaydet)

        btn_layout.addStretch()
        btn_layout.addWidget(iptal_btn)
        btn_layout.addWidget(kaydet_btn)
        ana.addLayout(btn_layout)

    def _mevcut_verileri_yukle(self):
        self.marka_input.setText(self.arac.marka)
        self.model_input.setText(self.arac.model)
        self.km_input.setValue(self.arac.kilometre)
        self.ucret_input.setValue(self.arac.saatlik_ucret)

    def _kaydet(self):
        marka = self.marka_input.text().strip()
        model = self.model_input.text().strip()
        km = self.km_input.value()
        ucret = self.ucret_input.value()

        if not marka:
            QMessageBox.warning(self, "Eksik Bilgi", "Marka bos olamaz.")
            self.marka_input.setFocus()
            return
        if not model:
            QMessageBox.warning(self, "Eksik Bilgi", "Model bos olamaz.")
            self.model_input.setFocus()
            return

        try:
            if self.duzenleme_modu:
                self.vy.arac_guncelle(self.arac.arac_id, marka, model, km, ucret)
            else:
                self.vy.arac_ekle(marka, model, km, ucret)
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))


class KullaniciDiyalog(QDialog):
    def __init__(self, vy: VeriYoneticisi, kullanici: Kullanici = None, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.kullanici = kullanici
        self.duzenleme_modu = kullanici is not None

        self.setWindowTitle("Yeni Kullanici")
        self.setMinimumWidth(520)
        self.setModal(True)

        self._arayuz_olustur()
        if self.duzenleme_modu:
            self._mevcut_verileri_yukle()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(36, 32, 36, 28)
        ana.setSpacing(24)

        baslik = "Kullaniciyi Duzenle" if self.duzenleme_modu else "Yeni Kullanici"
        kategori = "DUZENLE" if self.duzenleme_modu else "YENI KULLANICI"
        ana.addLayout(_editorial_baslik(baslik, kategori))

        aciklama = QLabel(
            "Ehliyet numarasi 6 haneli olmali ve sistem genelinde benzersiz olmalidir."
        )
        aciklama.setStyleSheet(
            "color: #64748b; font-family: 'Segoe UI', sans-serif; "
            "font-size: 13px; font-style: italic; "
            "background: transparent; border: none;"
        )
        ana.addWidget(aciklama)

        self.ad_input = QLineEdit()
        self.ad_input.setPlaceholderText("Orn: Beko Yilmaz")
        self.ad_input.returnPressed.connect(lambda: self.ehliyet_input.setFocus())

        self.ehliyet_input = QLineEdit()
        self.ehliyet_input.setPlaceholderText("6 haneli ehliyet numarasi")
        self.ehliyet_input.setMaxLength(6)
        self.ehliyet_input.returnPressed.connect(self._kaydet)

        ana.addLayout(_form_satiri("Ad Soyad", self.ad_input))
        ana.addLayout(_form_satiri("Ehliyet No", self.ehliyet_input))

        ana.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        iptal_btn, kaydet_btn = _diyalog_butonlari(
            kaydet_metin="GUNCELLE" if self.duzenleme_modu else "KAYIT OLUSTUR"
        )
        iptal_btn.clicked.connect(self.reject)
        kaydet_btn.clicked.connect(self._kaydet)

        btn_layout.addStretch()
        btn_layout.addWidget(iptal_btn)
        btn_layout.addWidget(kaydet_btn)
        ana.addLayout(btn_layout)

    def _mevcut_verileri_yukle(self):
        self.ad_input.setText(self.kullanici.ad)
        self.ehliyet_input.setText(self.kullanici.ehliyet_no)

    def _kaydet(self):
        ad = self.ad_input.text().strip()
        ehliyet = self.ehliyet_input.text().strip()

        if not ad:
            QMessageBox.warning(self, "Eksik Bilgi", "Ad soyad bos olamaz.")
            self.ad_input.setFocus()
            return
        if not ehliyet or len(ehliyet) != 6 or not ehliyet.isdigit():
            QMessageBox.warning(
                self, "Gecersiz Ehliyet",
                "Ehliyet numarasi 6 haneli rakamlardan olusmalidir."
            )
            self.ehliyet_input.setFocus()
            return

        try:
            if self.duzenleme_modu:
                self.vy.kullanici_guncelle(self.kullanici.kullanici_id, ad, ehliyet)
            else:
                self.vy.kullanici_ekle(ad, ehliyet)
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))
            self.ehliyet_input.setFocus()


class KiralamaBaslatDiyalog(QDialog):
    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy

        self.setWindowTitle("Yeni Kiralama")
        self.setMinimumWidth(560)
        self.setModal(True)

        self._arayuz_olustur()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(36, 32, 36, 28)
        ana.setSpacing(24)

        ana.addLayout(_editorial_baslik("Kiralama Baslat", "KIRALAMA"))

        aciklama = QLabel(
            "Musait araclar arasindan secim yapin. "
            "Her kullanicinin ayni anda en fazla 1 aktif kiralamasi olabilir."
        )
        aciklama.setStyleSheet(
            "color: #64748b; font-family: 'Segoe UI', sans-serif; "
            "font-size: 13px; font-style: italic; "
            "background: transparent; border: none;"
        )
        ana.addWidget(aciklama)

        self.arac_combo = QComboBox()
        self._araclari_yukle()

        self.kullanici_combo = QComboBox()
        self._kullanicilari_yukle()

        ana.addLayout(_form_satiri("Arac", self.arac_combo))
        ana.addLayout(_form_satiri("Kullanici", self.kullanici_combo))

        # Bilgi kutu
        bilgi_kutu = QFrame()
        bilgi_kutu.setStyleSheet(
            "background-color: #1e293b; "
            "border-left: 3px solid #3b82f6; "
            "border-radius: 6px;"
        )
        bilgi_layout = QHBoxLayout(bilgi_kutu)
        bilgi_layout.setContentsMargins(16, 14, 16, 14)

        bilgi = QLabel(
            "Kiralama baslatildiginda arac durumu <b>kirada</b> olarak guncellenir. "
            "Ucretlendirme saatlik bazda yapilir."
        )
        bilgi.setStyleSheet(
            "color: #f1f5f9; font-family: 'Segoe UI', sans-serif; "
            "font-size: 13px; font-style: italic; "
            "background: transparent; border: none;"
        )
        bilgi.setWordWrap(True)
        bilgi_layout.addWidget(bilgi)

        ana.addWidget(bilgi_kutu)

        ana.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        iptal_btn = QPushButton("IPTAL")
        iptal_btn.setObjectName("HayaletButon")
        iptal_btn.setFixedHeight(42)
        iptal_btn.setMinimumWidth(110)
        iptal_btn.setCursor(Qt.PointingHandCursor)
        iptal_btn.clicked.connect(self.reject)

        olustur_btn = QPushButton("KIRALAMAYA BASLA")
        olustur_btn.setStyleSheet(
            "QPushButton { background-color: #3b82f6; color: #f1f5f9; "
            "border: 1px solid #3b82f6; border-radius: 6px; "
            "padding: 0 28px; font-family: 'Inter', sans-serif; "
            "font-size: 12px; font-weight: 700; letter-spacing: 1px; } "
            "QPushButton:hover { background-color: #2563eb; "
            "border: 1px solid #2563eb; }"
        )
        olustur_btn.setFixedHeight(42)
        olustur_btn.setMinimumWidth(200)
        olustur_btn.setCursor(Qt.PointingHandCursor)
        olustur_btn.clicked.connect(self._kaydet)

        btn_layout.addStretch()
        btn_layout.addWidget(iptal_btn)
        btn_layout.addWidget(olustur_btn)
        ana.addLayout(btn_layout)

    def _araclari_yukle(self):
        self.arac_combo.clear()
        for a in self.vy.musait_araclar():
            etiket = f"{a.marka} {a.model}   ·   {a.saatlik_ucret:.0f} TL/saat"
            self.arac_combo.addItem(etiket, a.arac_id)

    def _kullanicilari_yukle(self):
        self.kullanici_combo.clear()
        for k in self.vy.tum_kullanicilar():
            self.kullanici_combo.addItem(f"{k.ad}   ·   {k.ehliyet_no}", k.kullanici_id)

    def _kaydet(self):
        aid = self.arac_combo.currentData()
        kid = self.kullanici_combo.currentData()

        if aid is None or kid is None:
            QMessageBox.warning(self, "Eksik Veri", "Lutfen arac ve kullanici secin.")
            return

        try:
            kiralama = self.vy.kiralama_baslat(aid, kid)
            arac = self.vy.arac_getir(aid)
            kullanici = self.vy.kullanici_getir(kid)
            QMessageBox.information(
                self, "Kiralama Baslatildi",
                f"'{arac.marka} {arac.model}' araci {kullanici.ad} kullanicisina kiralanmistir.\n\n"
                f"Saatlik ucret: {arac.saatlik_ucret:.0f} TL",
            )
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))
