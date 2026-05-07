"""
Modern Dark Automotive widget'lari.
Koyu lacivert + elektrik mavisi accent + yumusak koseler.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QRectF, QSize
from PyQt5.QtGui import (
    QPainter,
    QColor,
    QPen,
    QBrush,
    QFont,
    QPainterPath,
    QFontMetrics,
    QLinearGradient,
)


# Renkler
BG = QColor("#0f172a")
BG_CARD = QColor("#1e293b")
BG_HOVER = QColor("#334155")
TEXT = QColor("#f1f5f9")
TEXT_SEC = QColor("#94a3b8")
TEXT_MUTED = QColor("#64748b")
TEXT_FAINT = QColor("#475569")
BORDER = QColor("#334155")
ACCENT = QColor("#3b82f6")
ACCENT_HOVER = QColor("#2563eb")
ACCENT_PALE = QColor("#1e3a5f")
SUCCESS = QColor("#22c55e")
WARNING = QColor("#f59e0b")
DANGER = QColor("#ef4444")


# ============================================================
# METRİK KART
# ============================================================
class MetrikKart(QFrame):
    def __init__(self, etiket: str, deger: str = "0", altyazi: str = "",
                 accent: bool = False, parent=None):
        super().__init__(parent)
        renk = "#3b82f6" if accent else "#334155"
        self.setStyleSheet(
            "QFrame { background-color: #1e293b; "
            "border: 1px solid #334155; "
            f"border-top: 3px solid {renk}; "
            "border-radius: 10px; }"
        )
        self.setFixedHeight(140)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)

        et = QLabel(etiket.upper())
        et.setStyleSheet(
            "color: #64748b; font-size: 10px; font-weight: 700; "
            "letter-spacing: 1.5px; background: transparent; border: none;"
        )
        layout.addWidget(et)
        layout.addStretch()

        self.deger_lbl = QLabel(str(deger))
        font = QFont("Segoe UI", 34, QFont.Bold)
        self.deger_lbl.setFont(font)
        self.deger_lbl.setStyleSheet(
            "color: #f1f5f9; background: transparent; border: none;"
        )
        layout.addWidget(self.deger_lbl)

        self.alt_lbl = QLabel(altyazi)
        self.alt_lbl.setStyleSheet(
            "color: #94a3b8; font-size: 11px; "
            "background: transparent; border: none;"
        )
        layout.addWidget(self.alt_lbl)

    def deger_ayarla(self, deger):
        deger_str = str(deger)
        n = len(deger_str)
        if n <= 3:
            size = 34
        elif n == 4:
            size = 28
        else:
            size = 22
        font = QFont("Segoe UI", size, QFont.Bold)
        self.deger_lbl.setFont(font)
        self.deger_lbl.setText(deger_str)

    def altyazi_ayarla(self, altyazi):
        self.alt_lbl.setText(altyazi)


# ============================================================
# MASTHEAD
# ============================================================
class Masthead(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(86)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Accent ince cizgi ust
        p.setPen(Qt.NoPen)
        p.setBrush(ACCENT)
        p.drawRect(QRectF(22, 16, 32, 3))

        # Ana isim
        p.setPen(TEXT)
        font = QFont("Segoe UI", 20, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 0.5)
        p.setFont(font)
        p.drawText(QRectF(22, 28, w - 44, 28),
                   Qt.AlignLeft | Qt.AlignVCenter, "DriveShare")

        # Alt etiket
        p.setPen(TEXT_MUTED)
        font = QFont("Segoe UI", 8, QFont.DemiBold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2)
        p.setFont(font)
        p.drawText(QRectF(22, 58, w - 44, 14),
                   Qt.AlignLeft | Qt.AlignVCenter, "ARAC PAYLASIM SISTEMI")

        # Alt ayrac
        p.setPen(QPen(BORDER, 1))
        p.drawLine(22, h - 6, w - 22, h - 6)


# ============================================================
# EDITORIAL HEADER (simdi modern header)
# ============================================================
class EditorialHeader(QWidget):
    def __init__(self, kategori: str, baslik: str, altyazi: str,
                 sag_etiket: str = "", sag_meta: str = "",
                 parent=None):
        super().__init__(parent)
        self.kategori = kategori
        self.baslik = baslik
        self.altyazi = altyazi
        self.sag_etiket = sag_etiket
        self.sag_meta = sag_meta
        self.setMinimumHeight(140)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Kategori tag (accent mavi)
        p.setPen(ACCENT)
        font = QFont("Segoe UI", 9, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2)
        p.setFont(font)
        p.drawText(0, 24, self.kategori)

        # Sag etiket
        if self.sag_etiket:
            p.setPen(TEXT_MUTED)
            fm = QFontMetrics(font)
            sag_x = w - fm.horizontalAdvance(self.sag_etiket)
            p.drawText(sag_x, 24, self.sag_etiket)

        # Buyuk baslik
        p.setPen(TEXT)
        font = QFont("Segoe UI", 36, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -0.8)
        p.setFont(font)
        p.drawText(QRectF(0, 36, w, 50),
                   Qt.AlignLeft | Qt.AlignTop, self.baslik)

        # Altyazi
        p.setPen(TEXT_SEC)
        font = QFont("Segoe UI", 13)
        p.setFont(font)
        p.drawText(QRectF(0, 90, w, 24),
                   Qt.AlignLeft | Qt.AlignTop, self.altyazi)

        # Alt gradient cizgi (accent mavi -> seffaf)
        grad = QLinearGradient(0, h - 2, w * 0.6, h - 2)
        grad.setColorAt(0, ACCENT)
        grad.setColorAt(1, QColor(ACCENT.red(), ACCENT.green(), ACCENT.blue(), 0))
        p.setPen(QPen(QBrush(grad), 2))
        p.drawLine(0, h - 1, int(w * 0.6), h - 1)


# ============================================================
# ARAÇ GÖRSELİ
# ============================================================
class AracGorseli(QWidget):
    PALETLER = [
        (QColor("#1e40af"), QColor("#1e3a8a")),   # mavi
        (QColor("#047857"), QColor("#065f46")),   # yesil
        (QColor("#7c3aed"), QColor("#6d28d9")),   # mor
        (QColor("#dc2626"), QColor("#b91c1c")),   # kirmizi
        (QColor("#d97706"), QColor("#b45309")),   # turuncu
        (QColor("#0891b2"), QColor("#0e7490")),   # teal
        (QColor("#4f46e5"), QColor("#4338ca")),   # indigo
        (QColor("#be185d"), QColor("#9d174d")),   # pembe
    ]

    def __init__(self, marka: str, model: str, musait: bool = True, parent=None):
        super().__init__(parent)
        self.marka = marka
        self.model = model
        self.musait = musait
        self.setFixedSize(150, 110)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        idx = hash(f"{self.marka}{self.model}") % len(self.PALETLER)
        ana_renk, koyu_renk = self.PALETLER[idx]

        # Golge
        p.setBrush(QColor(0, 0, 0, 50))
        p.setPen(Qt.NoPen)
        path = QPainterPath()
        path.addRoundedRect(QRectF(6, h - 10, w - 12, 8), 4, 4)
        p.drawPath(path)

        # Ana kutu (rounded)
        path = QPainterPath()
        path.addRoundedRect(QRectF(4, 4, w - 8, h - 14), 10, 10)
        grad = QLinearGradient(4, 4, 4, h - 14)
        grad.setColorAt(0, ana_renk)
        grad.setColorAt(1, koyu_renk)
        p.setBrush(QBrush(grad))
        p.setPen(QPen(QColor(255, 255, 255, 20), 1))
        p.drawPath(path)

        # Ic parlama cizgisi
        p.setPen(QPen(QColor(255, 255, 255, 40), 1))
        p.drawLine(20, 20, w - 24, 20)

        # Marka
        p.setPen(QColor(255, 255, 255, 240))
        font = QFont("Segoe UI", 14, QFont.Bold)
        p.setFont(font)
        p.drawText(QRectF(10, 26, w - 20, 22),
                   Qt.AlignHCenter | Qt.AlignTop, self.marka)

        # Model
        p.setPen(QColor(255, 255, 255, 180))
        font = QFont("Segoe UI", 10)
        p.setFont(font)
        p.drawText(QRectF(10, 50, w - 20, 18),
                   Qt.AlignHCenter | Qt.AlignTop, self.model)

        # Alt cizgi
        p.setPen(QPen(QColor(255, 255, 255, 40), 1))
        p.drawLine(24, h - 26, w - 28, h - 26)

        # Musait degilse "KIRADA" muhru
        if not self.musait:
            p.save()
            p.translate(w / 2, h / 2 - 4)
            p.rotate(-12)

            # Yuvarlak koseli muhur
            muh_w, muh_h = 96, 26
            path = QPainterPath()
            path.addRoundedRect(QRectF(-muh_w / 2, -muh_h / 2, muh_w, muh_h), 4, 4)
            p.setBrush(QColor(239, 68, 68, 220))
            p.setPen(Qt.NoPen)
            p.drawPath(path)

            p.setPen(QColor(255, 255, 255))
            font = QFont("Segoe UI", 9, QFont.Bold)
            font.setLetterSpacing(QFont.AbsoluteSpacing, 2)
            p.setFont(font)
            p.drawText(QRectF(-muh_w / 2, -muh_h / 2, muh_w, muh_h),
                       Qt.AlignCenter, "KIRADA")
            p.restore()


# ============================================================
# MÜHÜR AVATAR
# ============================================================
class MuhurAvatar(QWidget):
    def __init__(self, ad: str, boyut: int = 40, parent=None):
        super().__init__(parent)
        self.ad = ad.strip()
        self.bas_harf = self.ad[0].upper() if self.ad else "?"
        self.setFixedSize(boyut, boyut)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Isime gore renk
        renkler = [ACCENT, SUCCESS, WARNING, QColor("#8b5cf6"), QColor("#ec4899")]
        secim = hash(self.ad) % len(renkler)
        renk = renkler[secim]

        # Dolu daire (gradient)
        grad = QLinearGradient(0, 0, w, h)
        grad.setColorAt(0, renk)
        grad.setColorAt(1, renk.darker(130))
        p.setBrush(QBrush(grad))
        p.setPen(Qt.NoPen)
        p.drawEllipse(1, 1, w - 2, h - 2)

        # Harf
        p.setPen(QColor(255, 255, 255))
        font = QFont("Segoe UI", int(w * 0.4), QFont.Bold)
        p.setFont(font)
        p.drawText(self.rect(), Qt.AlignCenter, self.bas_harf)


# ============================================================
# KART
# ============================================================
class Kart(QFrame):
    def __init__(self, baslik: str = None, alt_baslik: str = None,
                 accent: bool = False, parent=None):
        super().__init__(parent)
        self.setObjectName("Kart")
        self.accent = accent

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 20, 24, 20)
        self.layout.setSpacing(12)

        if baslik:
            ust = QHBoxLayout()
            ust.setContentsMargins(0, 0, 0, 0)
            ust.setSpacing(0)

            if accent:
                marker = QFrame()
                marker.setFixedSize(3, 24)
                marker.setStyleSheet(
                    "background-color: #3b82f6; border: none; border-radius: 2px;"
                )
                ust.addWidget(marker, 0, Qt.AlignVCenter)
                ust.addSpacing(10)

            baslik_l = QVBoxLayout()
            baslik_l.setSpacing(2)
            baslik_l.setContentsMargins(0, 0, 0, 0)

            self.baslik_lbl = QLabel(baslik)
            self.baslik_lbl.setObjectName("KartBaslik")
            baslik_l.addWidget(self.baslik_lbl)

            if alt_baslik:
                self.alt_baslik_lbl = QLabel(alt_baslik)
                self.alt_baslik_lbl.setObjectName("KartAltBaslik")
                baslik_l.addWidget(self.alt_baslik_lbl)

            ust.addLayout(baslik_l)
            ust.addStretch()
            self.layout.addLayout(ust)

            ayrac = QFrame()
            ayrac.setFixedHeight(1)
            ayrac.setStyleSheet("background-color: #334155;")
            self.layout.addWidget(ayrac)


# ============================================================
# KATEGORİ BAR (marka dagilimi icin)
# ============================================================
class KategoriBarYatay(QWidget):
    def __init__(self, dagilim: dict, parent=None):
        super().__init__(parent)
        self.dagilim = dagilim
        n = len(dagilim) if dagilim else 1
        self.setMinimumHeight(n * 40 + 10)

    def paintEvent(self, e):
        if not self.dagilim:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()

        sirali = sorted(self.dagilim.items(), key=lambda x: -x[1])
        max_v = max(v for _, v in sirali) if sirali else 1

        no_w = 36
        kat_w = 130
        sag_w = 50
        bar_x = no_w + kat_w + 6
        bar_w = w - bar_x - sag_w - 6

        satir_y = 4

        for i, (kategori, sayi) in enumerate(sirali):
            # Sira no
            p.setPen(TEXT_FAINT)
            font = QFont("Segoe UI", 16, QFont.Bold)
            p.setFont(font)
            p.drawText(QRectF(0, satir_y, no_w, 32),
                       Qt.AlignLeft | Qt.AlignVCenter, f"{i + 1:02d}")

            # Kategori adi
            p.setPen(TEXT)
            font = QFont("Segoe UI", 12, QFont.DemiBold)
            p.setFont(font)
            p.drawText(QRectF(no_w, satir_y, kat_w, 32),
                       Qt.AlignLeft | Qt.AlignVCenter, kategori)

            # Bar arkaplan
            p.setPen(Qt.NoPen)
            p.setBrush(QColor("#1e293b"))
            path = QPainterPath()
            path.addRoundedRect(QRectF(bar_x, satir_y + 16, bar_w, 10), 4, 4)
            p.drawPath(path)

            # Bar dolu
            dolu_w = max((sayi / max_v) * bar_w, 8)
            renk = ACCENT if i == 0 else TEXT_MUTED
            grad = QLinearGradient(bar_x, 0, bar_x + dolu_w, 0)
            grad.setColorAt(0, renk)
            grad.setColorAt(1, renk.lighter(120) if i == 0 else renk)
            p.setBrush(QBrush(grad))
            path = QPainterPath()
            path.addRoundedRect(QRectF(bar_x, satir_y + 16, dolu_w, 10), 4, 4)
            p.drawPath(path)

            # Sayi
            p.setPen(TEXT)
            font = QFont("Segoe UI", 14, QFont.Bold)
            p.setFont(font)
            p.drawText(QRectF(bar_x + bar_w + 6, satir_y, sag_w, 32),
                       Qt.AlignRight | Qt.AlignVCenter, str(sayi))

            satir_y += 40


# ============================================================
# Yardimci Sarmalayicilar
# ============================================================
class Rozet(QLabel):
    STILLER = {
        "basari": (
            "background-color: #14532d; color: #22c55e; "
            "border: 1px solid #166534;"
        ),
        "uyari": (
            "background-color: #713f12; color: #f59e0b; "
            "border: 1px solid #854d0e;"
        ),
        "tehlike": (
            "background-color: #7f1d1d; color: #ef4444; "
            "border: 1px solid #991b1b;"
        ),
        "notr": (
            "background-color: #1e293b; color: #94a3b8; "
            "border: 1px solid #334155;"
        ),
    }

    def __init__(self, metin: str, tip: str = "basari", parent=None):
        super().__init__(metin, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(28)
        self.setMinimumWidth(96)

        renk_stil = self.STILLER.get(tip, self.STILLER["notr"])
        self.setStyleSheet(
            f"QLabel {{ {renk_stil} "
            f"border-radius: 5px; "
            f"padding: 4px 12px; "
            f"font-size: 9px; font-weight: 700; "
            f"letter-spacing: 1px; }}"
        )


class HucreSarmalayici(QWidget):
    def __init__(self, icerik: QWidget, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(0)
        layout.addWidget(icerik, 0, Qt.AlignVCenter)


class ButonGrubu(QWidget):
    def __init__(self, butonlar: list, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)
        for b in butonlar:
            layout.addWidget(b)
        layout.addStretch()


class Ayirici(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Ayirici")
        self.setFixedHeight(1)


class AyiriciInce(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AyiriciInce")
        self.setFixedHeight(1)
