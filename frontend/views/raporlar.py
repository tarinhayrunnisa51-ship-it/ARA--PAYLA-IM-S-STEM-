"""
Raporlar Sayfasi - Editorial rapor.
"""
import csv
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFrame,
    QFileDialog,
    QMessageBox,
    QScrollArea,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader,
    Kart,
    MetrikKart,
    KategoriBarYatay,
    MuhurAvatar,
    Ayirici,
    AyiriciInce,
)


class RaporlarSayfasi(QWidget):
    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background-color: #0f172a; border: none;")

        ic = QWidget()
        scroll.setWidget(ic)

        ana = QVBoxLayout(ic)
        ana.setContentsMargins(48, 36, 48, 32)
        ana.setSpacing(28)

        header_satir = QHBoxLayout()
        header_satir.setSpacing(20)

        self.header = EditorialHeader(
            kategori="RAPORLAR",
            baslik="Genel Rapor",
            altyazi="Arac paylasim istatistikleri ve analiz.",
            sag_etiket="DETAY",
        )
        header_satir.addWidget(self.header, 1)

        export_btn = QPushButton("CSV OLARAK INDIR")
        export_btn.setObjectName("IkincilButon")
        export_btn.setStyleSheet(
            "QPushButton { background-color: #3b82f6; color: #f1f5f9; "
            "border: 1px solid #3b82f6; border-radius: 6px; "
            "padding: 0 28px; font-family: 'Segoe UI', sans-serif; "
            "font-size: 12px; font-weight: 700; letter-spacing: 1px; } "
            "QPushButton:hover { background-color: #2563eb; "
            "border: 1px solid #2563eb; }"
        )
        export_btn.setFixedHeight(46)
        export_btn.setMinimumWidth(220)
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.clicked.connect(self._csv_export)

        btn_sarici = QVBoxLayout()
        btn_sarici.addStretch()
        btn_sarici.addWidget(export_btn)
        btn_sarici.addSpacing(20)
        header_satir.addLayout(btn_sarici)

        ana.addLayout(header_satir)

        # 4 metric kart
        grid = QGridLayout()
        grid.setSpacing(16)

        self.blok_arac = MetrikKart("Toplam Arac", "0", "Filo hacmi.")
        self.blok_kullanici = MetrikKart("Toplam Kullanici", "0", "Kayitli suruculer.")
        self.blok_islem = MetrikKart("Toplam Islem", "0", "Tum zamanlar.")
        self.blok_gelir = MetrikKart("Toplam Gelir", "0", "Tamamlanan kiralamalar.", accent=True)

        grid.addWidget(self.blok_arac, 0, 0)
        grid.addWidget(self.blok_kullanici, 0, 1)
        grid.addWidget(self.blok_islem, 0, 2)
        grid.addWidget(self.blok_gelir, 0, 3)
        ana.addLayout(grid)

        # Alt: marka dağılımı + en aktif kullanıcılar
        alt = QHBoxLayout()
        alt.setSpacing(16)

        marka_kart = Kart(
            "Marka Dagilimi",
            "Filodaki araclarin markalara gore dagilimi.",
        )
        self.marka_widget = QWidget()
        marka_layout = QVBoxLayout(self.marka_widget)
        marka_layout.setContentsMargins(0, 0, 0, 0)
        marka_kart.layout.addWidget(self.marka_widget)
        alt.addWidget(marka_kart, 1)

        aktif_kart = Kart(
            "En Aktif Kullanicilar",
            "Tum zamanlarda en cok kiralama yapan bes kullanici.",
            accent=True,
        )
        self.aktif_kullanicilar_widget = QWidget()
        self.aktif_kullanicilar_layout = QVBoxLayout(self.aktif_kullanicilar_widget)
        self.aktif_kullanicilar_layout.setContentsMargins(0, 0, 0, 0)
        self.aktif_kullanicilar_layout.setSpacing(8)
        aktif_kart.layout.addWidget(self.aktif_kullanicilar_widget)
        alt.addWidget(aktif_kart, 1)

        ana.addLayout(alt)

        ana.addStretch()

        dis_layout = QVBoxLayout(self)
        dis_layout.setContentsMargins(0, 0, 0, 0)
        dis_layout.addWidget(scroll)

    def _layout_temizle(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

    def yenile(self):
        stats = self.vy.genel_istatistikler()

        self.blok_arac.deger_ayarla(stats["toplam_arac"])
        self.blok_arac.altyazi_ayarla(
            f"{stats['musait_arac']} musait, {stats['kirada_arac']} kirada."
        )

        self.blok_kullanici.deger_ayarla(stats["toplam_kullanici"])

        self.blok_islem.deger_ayarla(stats["toplam_islem"])
        self.blok_islem.altyazi_ayarla(f"{stats['aktif_kiralama']} aktif kiralama.")

        gelir = stats["toplam_gelir"]
        if gelir >= 1000:
            gelir_str = f"{gelir:,.0f}"
        else:
            gelir_str = f"{gelir:.0f}"
        self.blok_gelir.deger_ayarla(f"{gelir_str}")
        self.blok_gelir.altyazi_ayarla("TL toplam gelir.")

        # Marka dağılımı
        self._layout_temizle(self.marka_widget.layout())
        dagilim = self.vy.marka_dagilim()
        if dagilim:
            self.marka_widget.layout().addWidget(KategoriBarYatay(dagilim))
            self.marka_widget.layout().addStretch()
        else:
            bos = QLabel("— Henuz kayitli arac yok. —")
            bos.setStyleSheet(
                "color: #64748b; "
                "font-family: 'Segoe UI', sans-serif; "
                "font-style: italic; padding: 30px; "
                "background: transparent; border: none;"
            )
            bos.setAlignment(Qt.AlignCenter)
            self.marka_widget.layout().addWidget(bos)

        # En aktif kullanıcılar
        self._layout_temizle(self.aktif_kullanicilar_layout)

        sayim = {}
        for ki in self.vy.tum_kiralamalar():
            sayim[ki.kullanici_id] = sayim.get(ki.kullanici_id, 0) + 1

        sirali = sorted(sayim.items(), key=lambda x: -x[1])[:5]

        if not sirali:
            bos = QLabel("— Henuz islem kaydi yok. —")
            bos.setStyleSheet(
                "color: #64748b; "
                "font-family: 'Segoe UI', sans-serif; "
                "font-style: italic; padding: 30px; "
                "background: transparent; border: none;"
            )
            bos.setAlignment(Qt.AlignCenter)
            self.aktif_kullanicilar_layout.addWidget(bos)
        else:
            for sira, (kullanici_id, sayi) in enumerate(sirali, 1):
                k = self.vy.kullanici_getir(kullanici_id)
                if not k:
                    continue
                self.aktif_kullanicilar_layout.addWidget(
                    self._kullanici_satiri(sira, k, sayi)
                )

        self.aktif_kullanicilar_layout.addStretch()

    def _kullanici_satiri(self, sira: int, kullanici, sayi: int) -> QFrame:
        f = QFrame()
        f.setStyleSheet(
            "QFrame { background-color: #0f172a; "
            "border-bottom: 1px solid #334155; }"
        )

        layout = QHBoxLayout(f)
        layout.setContentsMargins(4, 12, 4, 12)
        layout.setSpacing(14)

        no_lbl = QLabel(f"{sira:02d}")
        no_lbl.setFixedWidth(40)
        no_lbl.setStyleSheet(
            "color: #3b82f6; "
            "font-family: 'Segoe UI', sans-serif; "
            "font-size: 28px; font-weight: 900; letter-spacing: -1px; "
            "background: transparent; border: none;"
        )
        no_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(no_lbl)

        layout.addWidget(MuhurAvatar(kullanici.ad, boyut=36))

        bilgi = QVBoxLayout()
        bilgi.setSpacing(2)
        bilgi.setContentsMargins(0, 0, 0, 0)

        ad = QLabel(kullanici.ad)
        ad.setStyleSheet(
            "color: #f1f5f9; "
            "font-family: 'Segoe UI', sans-serif; "
            "font-size: 14px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        ehliyet = QLabel(f"Ehliyet: {kullanici.ehliyet_no}")
        ehliyet.setStyleSheet(
            "color: #64748b; font-family: 'Inter', sans-serif; "
            "font-size: 10px; "
            "background: transparent; border: none;"
        )
        bilgi.addWidget(ad)
        bilgi.addWidget(ehliyet)
        layout.addLayout(bilgi, 1)

        sayi_kutu = QVBoxLayout()
        sayi_kutu.setSpacing(0)
        sayi_kutu.setContentsMargins(0, 0, 0, 0)

        sayi_lbl = QLabel(str(sayi))
        sayi_lbl.setStyleSheet(
            "color: #f1f5f9; "
            "font-family: 'Segoe UI', sans-serif; "
            "font-size: 24px; font-weight: 900; letter-spacing: -0.5px; "
            "background: transparent; border: none;"
        )
        sayi_lbl.setAlignment(Qt.AlignRight)

        etiket = QLabel("KIRALAMA")
        etiket.setStyleSheet(
            "color: #64748b; font-family: 'Inter', sans-serif; "
            "font-size: 8px; font-weight: 800; letter-spacing: 1.8px; "
            "background: transparent; border: none;"
        )
        etiket.setAlignment(Qt.AlignRight)

        sayi_kutu.addWidget(sayi_lbl)
        sayi_kutu.addWidget(etiket)
        layout.addLayout(sayi_kutu)

        return f

    def _csv_export(self):
        dosya_yolu, _ = QFileDialog.getSaveFileName(
            self, "CSV Olarak Kaydet",
            "driveshare_raporu.csv", "CSV Dosyalari (*.csv)"
        )
        if not dosya_yolu:
            return

        try:
            with open(dosya_yolu, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                stats = self.vy.genel_istatistikler()

                w.writerow(["DRIVESHARE — GENEL RAPOR"])
                w.writerow([])
                w.writerow(["Toplam Arac", stats["toplam_arac"]])
                w.writerow(["Musait", stats["musait_arac"]])
                w.writerow(["Kirada", stats["kirada_arac"]])
                w.writerow(["Toplam Kullanici", stats["toplam_kullanici"]])
                w.writerow(["Aktif Kiralama", stats["aktif_kiralama"]])
                w.writerow(["Toplam Islem", stats["toplam_islem"]])
                w.writerow(["Toplam Gelir (TL)", stats["toplam_gelir"]])
                w.writerow([])

                w.writerow(["MARKA DAGILIMI"])
                for m, v in sorted(self.vy.marka_dagilim().items(),
                                   key=lambda x: -x[1]):
                    w.writerow([m, v])
                w.writerow([])

                w.writerow(["TUM KIRALAMA KAYITLARI"])
                w.writerow([
                    "Islem No", "Marka", "Model", "Kullanici", "Ehliyet No",
                    "Baslangic", "Bitis", "Sure (saat)", "Tutar (TL)", "Durum"
                ])
                for ki in self.vy.tum_kiralamalar():
                    a = self.vy.arac_getir(ki.arac_id)
                    k = self.vy.kullanici_getir(ki.kullanici_id)
                    if not a or not k:
                        continue
                    if ki.aktif_mi():
                        durum = f"Aktif ({ki.sure_saat():.1f} saat)"
                        tutar = ki.tutar(a.saatlik_ucret)
                    else:
                        durum = "Tamamlandi"
                        tutar = ki.tutar(a.saatlik_ucret)
                    w.writerow([
                        ki.kiralama_id, a.marka, a.model, k.ad, k.ehliyet_no,
                        ki.baslangic_saati.strftime("%d.%m.%Y %H:%M"),
                        ki.bitis_saati.strftime("%d.%m.%Y %H:%M") if ki.bitis_saati else "",
                        f"{ki.sure_saat():.1f}",
                        f"{tutar:.2f}",
                        durum,
                    ])

            QMessageBox.information(
                self, "Basarili", f"Rapor kaydedildi:\n{dosya_yolu}"
            )
        except Exception as ex:
            QMessageBox.critical(self, "Hata", f"Dosya kaydedilemedi:\n{ex}")
