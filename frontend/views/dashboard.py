"""
Dashboard / Kontrol Paneli - Sade editorial.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader,
    Kart,
    Rozet,
    HucreSarmalayici,
    MetrikKart,
)


class DashboardSayfasi(QWidget):
    def __init__(self, vy: VeriYoneticisi, aktif_kullanici=None, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.aktif_kullanici = aktif_kullanici
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(48, 36, 48, 32)
        ana.setSpacing(24)

        self.header = EditorialHeader(
            kategori="DASHBOARD",
            baslik="Kontrol Paneli",
            altyazi="Arac paylasim sisteminin anlik durumu.",
            sag_etiket="GENEL BAKIS",
        )
        ana.addWidget(self.header)

        # 4 metric kart
        grid = QGridLayout()
        grid.setSpacing(16)

        self.kart_arac = MetrikKart("Toplam Arac", "0", "Filodaki arac sayisi.")
        self.kart_musait = MetrikKart("Musait Arac", "0", "Kiralanabilir durumdakiler.")
        self.kart_aktif = MetrikKart("Aktif Kiralama", "0", "Su an kirada.", accent=True)
        self.kart_gelir = MetrikKart("Toplam Gelir", "0", "Tamamlanan kiralamalardan.")

        grid.addWidget(self.kart_arac, 0, 0)
        grid.addWidget(self.kart_musait, 0, 1)
        grid.addWidget(self.kart_aktif, 0, 2)
        grid.addWidget(self.kart_gelir, 0, 3)
        ana.addLayout(grid)

        # Aktif kiralama tablosu
        tablo_kart = Kart(
            "Aktif Kiralamalar",
            "Su anda kirada olan araclar — baslangic saatine gore.",
        )

        self.tablo = QTableWidget(0, 4)
        self.tablo.setHorizontalHeaderLabels(["ARAC", "KULLANICI", "BASLANGIC", "DURUM"])
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablo.setShowGrid(False)
        self.tablo.setFocusPolicy(Qt.NoFocus)
        self.tablo.setAlternatingRowColors(True)

        h = self.tablo.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.Stretch)
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.Fixed)
        h.setSectionResizeMode(3, QHeaderView.Fixed)
        self.tablo.setColumnWidth(2, 160)
        self.tablo.setColumnWidth(3, 170)

        self.tablo.setMinimumHeight(340)
        tablo_kart.layout.addWidget(self.tablo)

        ana.addWidget(tablo_kart, 1)

    def yenile(self):
        stats = self.vy.genel_istatistikler()

        self.kart_arac.deger_ayarla(stats["toplam_arac"])
        self.kart_arac.altyazi_ayarla(
            f"{stats['musait_arac']} musait, {stats['kirada_arac']} kirada."
        )

        self.kart_musait.deger_ayarla(stats["musait_arac"])
        self.kart_musait.altyazi_ayarla("Kiralanabilir arac sayisi.")

        self.kart_aktif.deger_ayarla(stats["aktif_kiralama"])
        self.kart_aktif.altyazi_ayarla(f"Toplam {stats['toplam_islem']} islem.")

        gelir = stats["toplam_gelir"]
        if gelir >= 1000:
            gelir_str = f"{gelir:,.0f}"
        else:
            gelir_str = f"{gelir:.0f}"
        self.kart_gelir.deger_ayarla(f"{gelir_str}")
        self.kart_gelir.altyazi_ayarla("TL toplam gelir.")

        # Aktif kiralama tablosu
        kiralamalar = sorted(
            self.vy.aktif_kiralamalar(),
            key=lambda ki: ki.baslangic_saati, reverse=True,
        )[:8]

        self.tablo.setRowCount(len(kiralamalar) if kiralamalar else 1)

        if not kiralamalar:
            bos = QTableWidgetItem("  Aktif kiralama bulunmuyor.")
            bos.setForeground(QColor("#64748b"))
            f = QFont("Segoe UI", 11)
            f.setItalic(True)
            bos.setFont(f)
            self.tablo.setSpan(0, 0, 1, 4)
            self.tablo.setItem(0, 0, bos)
            self.tablo.setRowHeight(0, 80)
            return

        for satir, ki in enumerate(kiralamalar):
            arac = self.vy.arac_getir(ki.arac_id)
            kullanici = self.vy.kullanici_getir(ki.kullanici_id)

            # Araç
            arac_item = QTableWidgetItem(
                "  " + (f"{arac.marka} {arac.model}" if arac else "?")
            )
            f = QFont("Segoe UI", 12)
            if not f.exactMatch():
                f = QFont("Segoe UI", 12)
            f.setBold(True)
            arac_item.setFont(f)
            arac_item.setForeground(QColor("#f1f5f9"))
            self.tablo.setItem(satir, 0, arac_item)

            # Kullanıcı
            kul_item = QTableWidgetItem(kullanici.ad if kullanici else "?")
            kul_item.setForeground(QColor("#94a3b8"))
            self.tablo.setItem(satir, 1, kul_item)

            # Başlangıç
            tarih_item = QTableWidgetItem(
                ki.baslangic_saati.strftime("%d.%m.%Y %H:%M")
            )
            tarih_item.setForeground(QColor("#64748b"))
            self.tablo.setItem(satir, 2, tarih_item)

            # Durum rozeti
            sure = ki.sure_saat()
            if sure < 1:
                rozet = Rozet(f"{int(sure * 60)} DK", "basari")
            else:
                rozet = Rozet(f"{sure:.1f} SAAT", "uyari")
            self.tablo.setCellWidget(satir, 3, HucreSarmalayici(rozet))

            self.tablo.setRowHeight(satir, 56)
