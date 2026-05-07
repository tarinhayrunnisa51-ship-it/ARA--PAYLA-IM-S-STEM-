"""
Kiralamalar Sayfasi - Editorial.
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
    QComboBox,
    QFrame,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader,
    Rozet,
    HucreSarmalayici,
    ButonGrubu,
)
from frontend.widgets.diyaloglar import KiralamaBaslatDiyalog


class KiralamalarSayfasi(QWidget):
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
            kategori="KIRALAMALAR",
            baslik="Kiralamalar",
            altyazi="Tum kiralama ve iade hareketleri.",
            sag_etiket="KAYIT",
        )
        header_satir.addWidget(self.header, 1)

        olustur_btn = QPushButton("+  YENI KIRALAMA")
        olustur_btn.setStyleSheet(
            "QPushButton { background-color: #3b82f6; color: #f1f5f9; "
            "border: 1px solid #3b82f6; border-radius: 6px; "
            "padding: 0 28px; font-family: 'Segoe UI', sans-serif; "
            "font-size: 12px; font-weight: 700; letter-spacing: 1px; } "
            "QPushButton:hover { background-color: #2563eb; "
            "border: 1px solid #2563eb; }"
        )
        olustur_btn.setFixedHeight(46)
        olustur_btn.setMinimumWidth(190)
        olustur_btn.setCursor(Qt.PointingHandCursor)
        olustur_btn.clicked.connect(self._kiralama_baslat)

        btn_sarici = QVBoxLayout()
        btn_sarici.addStretch()
        btn_sarici.addWidget(olustur_btn)
        btn_sarici.addSpacing(20)
        header_satir.addLayout(btn_sarici)

        ana.addLayout(header_satir)

        # Filtre
        filtre = QHBoxLayout()
        filtre.setSpacing(12)

        self.arama = QLineEdit()
        self.arama.setObjectName("AramaInput")
        self.arama.setPlaceholderText("ARA  ·  Arac, kullanici ya da islem no...")
        self.arama.setFixedHeight(44)
        self.arama.textChanged.connect(self.yenile)
        filtre.addWidget(self.arama, 1)

        self.durum_filtre = QComboBox()
        self.durum_filtre.addItem("TUMU", "tumu")
        self.durum_filtre.addItem("AKTIF", "aktif")
        self.durum_filtre.addItem("TAMAMLANDI", "tamamlandi")
        self.durum_filtre.setFixedHeight(44)
        self.durum_filtre.setMinimumWidth(180)
        self.durum_filtre.currentIndexChanged.connect(self.yenile)
        filtre.addWidget(self.durum_filtre)

        ana.addLayout(filtre)

        # Tablo
        self.tablo = QTableWidget(0, 6)
        self.tablo.setHorizontalHeaderLabels(
            ["NO.", "ARAC", "KULLANICI", "BASLANGIC", "DURUM", "ISLEM"]
        )
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablo.setShowGrid(False)
        self.tablo.setFocusPolicy(Qt.NoFocus)
        self.tablo.setAlternatingRowColors(True)

        h = self.tablo.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.Fixed)
        h.setSectionResizeMode(1, QHeaderView.Stretch)
        h.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(3, QHeaderView.Fixed)
        h.setSectionResizeMode(4, QHeaderView.Fixed)
        h.setSectionResizeMode(5, QHeaderView.Fixed)
        self.tablo.setColumnWidth(0, 80)
        self.tablo.setColumnWidth(3, 160)
        self.tablo.setColumnWidth(4, 170)
        self.tablo.setColumnWidth(5, 130)

        ana.addWidget(self.tablo, 1)

    def yenile(self):
        filtre = self.arama.text().strip().lower()
        durum_filtre = self.durum_filtre.currentData()

        kiralamalar = self.vy.tum_kiralamalar()

        if durum_filtre == "aktif":
            kiralamalar = [ki for ki in kiralamalar if ki.aktif_mi()]
        elif durum_filtre == "tamamlandi":
            kiralamalar = [ki for ki in kiralamalar if not ki.aktif_mi()]

        if filtre:
            filtrelenen = []
            for ki in kiralamalar:
                a = self.vy.arac_getir(ki.arac_id)
                k = self.vy.kullanici_getir(ki.kullanici_id)
                metin = (
                    f"{ki.kiralama_id} "
                    f"{a.marka if a else ''} {a.model if a else ''} "
                    f"{k.ad if k else ''} {k.ehliyet_no if k else ''}"
                ).lower()
                if filtre in metin:
                    filtrelenen.append(ki)
            kiralamalar = filtrelenen

        self.tablo.setRowCount(len(kiralamalar))

        for satir, ki in enumerate(kiralamalar):
            arac = self.vy.arac_getir(ki.arac_id)
            kullanici = self.vy.kullanici_getir(ki.kullanici_id)

            # Numara
            no_lbl = QLabel(f"{ki.kiralama_id:03d}")
            no_lbl.setStyleSheet(
                "color: #475569; "
                "font-family: 'Segoe UI', sans-serif; "
                "font-size: 18px; font-weight: 900; letter-spacing: -0.5px; "
                "padding-left: 14px; "
                "background: transparent; border: none;"
            )
            no_lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.tablo.setCellWidget(satir, 0, no_lbl)

            # Araç
            arac_lbl = QLabel(
                f"{arac.marka} {arac.model}" if arac else "?"
            )
            arac_lbl.setStyleSheet(
                "color: #f1f5f9; "
                "font-family: 'Segoe UI', sans-serif; "
                "font-size: 14px; font-weight: 700; "
                "padding-left: 14px; padding-right: 14px; "
                "background: transparent; border: none;"
            )
            self.tablo.setCellWidget(satir, 1, arac_lbl)

            # Kullanıcı
            kul_item = QTableWidgetItem(kullanici.ad if kullanici else "?")
            kul_item.setForeground(QColor("#94a3b8"))
            f = QFont("Inter", 11)
            kul_item.setFont(f)
            self.tablo.setItem(satir, 2, kul_item)

            # Başlangıç
            tarih_item = QTableWidgetItem(
                ki.baslangic_saati.strftime("%d.%m.%Y %H:%M")
            )
            tarih_item.setForeground(QColor("#64748b"))
            f = QFont("Inter", 11)
            tarih_item.setFont(f)
            self.tablo.setItem(satir, 3, tarih_item)

            # Durum
            if not ki.aktif_mi():
                sure = ki.sure_saat()
                tutar = ki.tutar(arac.saatlik_ucret) if arac else 0
                rozet = Rozet(f"BITTI {tutar:.0f}TL", "notr")
            else:
                sure = ki.sure_saat()
                if sure < 1:
                    rozet = Rozet(f"AKTIF {int(sure * 60)}DK", "basari")
                else:
                    rozet = Rozet(f"AKTIF {sure:.1f}SA", "uyari")
            self.tablo.setCellWidget(satir, 4, HucreSarmalayici(rozet))

            # İşlem
            if ki.aktif_mi():
                bitir_btn = QPushButton("BITIR")
                bitir_btn.setStyleSheet(
                    "QPushButton { background-color: transparent; "
                    "color: #f1f5f9; "
                    "border: 1px solid #3b82f6; "
                    "border-radius: 6px; "
                    "padding-left: 12px; padding-right: 12px; "
                    "font-family: 'Segoe UI', sans-serif; "
                    "font-size: 11px; font-weight: 700; letter-spacing: 0.5px; } "
                    "QPushButton:hover { background-color: #3b82f6; color: #f1f5f9; }"
                )
                bitir_btn.setFixedHeight(30)
                bitir_btn.setFixedWidth(96)
                bitir_btn.setCursor(Qt.PointingHandCursor)
                bitir_btn.clicked.connect(
                    lambda _, kid=ki.kiralama_id: self._kiralama_bitir(kid)
                )
                self.tablo.setCellWidget(satir, 5, ButonGrubu([bitir_btn]))
            else:
                bos = QLabel("—")
                bos.setStyleSheet(
                    "color: #334155; font-size: 16px; "
                    "background: transparent; border: none;"
                )
                bos.setAlignment(Qt.AlignCenter)
                self.tablo.setCellWidget(satir, 5, HucreSarmalayici(bos))

            self.tablo.setRowHeight(satir, 56)

    def _kiralama_baslat(self):
        if not self.vy.musait_araclar():
            QMessageBox.warning(self, "Musait Arac Yok",
                                "Su anda kiralanabilecek musait arac yok.")
            return
        if not self.vy.tum_kullanicilar():
            QMessageBox.warning(self, "Kullanici Yok",
                                "Once en az bir kullanici eklemelisiniz.")
            return

        d = KiralamaBaslatDiyalog(self.vy, parent=self)
        if d.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _kiralama_bitir(self, kiralama_id: int):
        ki = self.vy.kiralama_getir(kiralama_id)
        if not ki:
            return
        arac = self.vy.arac_getir(ki.arac_id)
        kullanici = self.vy.kullanici_getir(ki.kullanici_id)

        cevap = QMessageBox.question(
            self, "Kiralama Bitir",
            f"'{arac.marka} {arac.model if arac else ''}' aracinin "
            f"{kullanici.ad if kullanici else ''} kiralamasini bitirmek istiyor musunuz?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes,
        )
        if cevap == QMessageBox.Yes:
            try:
                self.vy.kiralama_bitir(kiralama_id)
                self.yenile()
                self.veri_degisti.emit()

                ki = self.vy.kiralama_getir(kiralama_id)
                tutar = ki.tutar(arac.saatlik_ucret) if arac else 0
                QMessageBox.information(
                    self, "Kiralama Bitti",
                    f"Kiralama basariyla bitirildi.\n\n"
                    f"Sure: {ki.sure_saat():.1f} saat\n"
                    f"Tutar: {tutar:.2f} TL",
                )
            except ValueError as e:
                QMessageBox.warning(self, "Hata", str(e))
