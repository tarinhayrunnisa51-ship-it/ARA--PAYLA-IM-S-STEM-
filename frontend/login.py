"""
Login Penceresi - Modern dark automotive tema.
"""
from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QCheckBox,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import (
    QPainter,
    QColor,
    QPen,
    QFont,
    QLinearGradient,
    QBrush,
    QPainterPath,
)

from backend import AuthYoneticisi, SistemKullanici


# Renkler
BG = QColor("#0f172a")
BG_CARD = QColor("#1e293b")
TEXT = QColor("#f1f5f9")
TEXT_SEC = QColor("#94a3b8")
TEXT_MUTED = QColor("#64748b")
BORDER = QColor("#334155")
ACCENT = QColor("#3b82f6")
ACCENT_HOVER = QColor("#2563eb")


class _SolPanel(QWidget):
    """Login penceresinin sol tarafi - modern dark branding."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(520)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        w = rect.width()
        h = rect.height()

        # Gradient arkaplan
        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0, QColor("#0f172a"))
        grad.setColorAt(0.5, QColor("#1e293b"))
        grad.setColorAt(1, QColor("#0f172a"))
        p.fillRect(rect, QBrush(grad))

        # Sag kenarlik
        p.setPen(QPen(BORDER, 1))
        p.drawLine(w - 1, 0, w - 1, h)

        margin = 48

        # Ust accent cizgi
        p.setPen(Qt.NoPen)
        grad2 = QLinearGradient(margin, 0, margin + 80, 0)
        grad2.setColorAt(0, ACCENT)
        grad2.setColorAt(1, QColor(ACCENT.red(), ACCENT.green(), ACCENT.blue(), 0))
        p.setBrush(QBrush(grad2))
        p.drawRect(QRectF(margin, 56, 80, 3))

        # Ust etiket
        p.setPen(TEXT_MUTED)
        font = QFont("Segoe UI", 9, QFont.DemiBold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2)
        p.setFont(font)
        p.drawText(QRectF(margin, 72, w - margin * 2, 18),
                   Qt.AlignLeft | Qt.AlignVCenter, "ARAC PAYLASIM SISTEMI")

        # Buyuk baslik
        p.setPen(TEXT)
        font = QFont("Segoe UI", 46, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -1)
        p.setFont(font)
        p.drawText(QRectF(margin, 98, w - margin * 2, 60),
                   Qt.AlignLeft | Qt.AlignVCenter, "DriveShare")

        # Alt cizgi
        p.setPen(QPen(BORDER, 1))
        p.drawLine(margin, 170, w - margin, 170)

        # Slogan
        p.setPen(TEXT_SEC)
        font = QFont("Segoe UI", 16)
        p.setFont(font)
        p.drawText(QRectF(margin, 200, w - margin * 2, 28),
                   Qt.AlignLeft, "Aracini paylas,")
        p.drawText(QRectF(margin, 230, w - margin * 2, 28),
                   Qt.AlignLeft, "mesafeni kisalt.")

        # Ozellikler
        ozellik_y = 300
        ozellikler = [
            "Saatlik arac kiralama",
            "Kullanici ve ehliyet yonetimi",
            "Kiralama takibi ve gecmis",
            "Detayli raporlar ve analiz",
        ]

        for i, oz in enumerate(ozellikler):
            y = ozellik_y + i * 40

            # Accent daire bullet
            p.setBrush(ACCENT)
            p.setPen(Qt.NoPen)
            p.drawEllipse(QRectF(margin, y - 4, 8, 8))

            # Metin
            p.setPen(TEXT_SEC)
            font = QFont("Segoe UI", 12)
            p.setFont(font)
            p.drawText(margin + 22, y + 4, oz)

        # Alt footer
        p.setPen(QPen(BORDER, 1))
        p.drawLine(margin, h - 48, w - margin, h - 48)

        p.setPen(TEXT_MUTED)
        font = QFont("Segoe UI", 9)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1)
        p.setFont(font)
        p.drawText(QRectF(margin, h - 36, w - margin * 2, 16),
                   Qt.AlignLeft | Qt.AlignVCenter, "© 2026 DriveShare")
        p.drawText(QRectF(margin, h - 36, w - margin * 2, 16),
                   Qt.AlignRight | Qt.AlignVCenter, "v1.0")


class LoginPenceresi(QDialog):
    def __init__(self, auth: AuthYoneticisi, parent=None):
        super().__init__(parent)
        self.auth = auth
        self.dogrulanan_kullanici: SistemKullanici | None = None

        self.setWindowTitle("DriveShare — Giris")
        self.setFixedSize(1080, 680)
        self.setModal(True)

        self._arayuz_olustur()

    def _arayuz_olustur(self):
        ana = QHBoxLayout(self)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        ana.addWidget(_SolPanel())

        # Sag form alani
        sag = QFrame()
        sag.setStyleSheet("background-color: #0f172a;")
        sag_layout = QVBoxLayout(sag)
        sag_layout.setContentsMargins(56, 64, 56, 48)
        sag_layout.setSpacing(0)

        kat = QLabel("GIRIS")
        kat.setStyleSheet(
            "color: #3b82f6; font-size: 10px; font-weight: 700; "
            "letter-spacing: 2.5px; background: transparent; border: none;"
        )
        sag_layout.addWidget(kat)
        sag_layout.addSpacing(14)

        baslik = QLabel("Hos Geldin")
        baslik.setStyleSheet(
            "color: #f1f5f9; font-size: 38px; font-weight: 800; "
            "letter-spacing: -0.5px; background: transparent; border: none;"
        )
        sag_layout.addWidget(baslik)

        alt = QLabel("Devam etmek icin hesabina giris yap.")
        alt.setStyleSheet(
            "color: #94a3b8; font-size: 13px; "
            "background: transparent; border: none;"
        )
        sag_layout.addWidget(alt)

        sag_layout.addSpacing(12)

        # Accent gradient cizgi
        ayrac = QFrame()
        ayrac.setFixedHeight(2)
        ayrac.setStyleSheet("background-color: #3b82f6;")
        sag_layout.addWidget(ayrac)

        sag_layout.addSpacing(28)

        # Form
        sag_layout.addWidget(self._etiket("KULLANICI ADI"))
        sag_layout.addSpacing(8)

        self.kul_input = QLineEdit()
        self.kul_input.setPlaceholderText("kullanici adinizi girin")
        self.kul_input.setFixedHeight(46)
        self.kul_input.setStyleSheet(self._input_stil())
        self.kul_input.returnPressed.connect(lambda: self.sifre_input.setFocus())
        sag_layout.addWidget(self.kul_input)
        sag_layout.addSpacing(20)

        sag_layout.addWidget(self._etiket("SIFRE"))
        sag_layout.addSpacing(8)

        self.sifre_input = QLineEdit()
        self.sifre_input.setPlaceholderText("••••••••")
        self.sifre_input.setEchoMode(QLineEdit.Password)
        self.sifre_input.setFixedHeight(46)
        self.sifre_input.setStyleSheet(self._input_stil())
        self.sifre_input.returnPressed.connect(self._giris_yap)
        sag_layout.addWidget(self.sifre_input)

        sag_layout.addSpacing(14)

        self.goster_chk = QCheckBox("Sifreyi goster")
        self.goster_chk.setStyleSheet(
            "QCheckBox { color: #94a3b8; font-size: 11px; font-weight: 600; "
            "background: transparent; border: none; spacing: 8px; }"
            "QCheckBox::indicator { width: 14px; height: 14px; "
            "border: 1px solid #334155; border-radius: 3px; "
            "background-color: #0f172a; }"
            "QCheckBox::indicator:checked { background-color: #3b82f6; "
            "border: 1px solid #3b82f6; }"
        )
        self.goster_chk.toggled.connect(self._sifre_goster)
        sag_layout.addWidget(self.goster_chk)

        sag_layout.addSpacing(24)

        self.hata_lbl = QLabel("")
        self.hata_lbl.setStyleSheet(
            "background-color: #7f1d1d; color: #ef4444; "
            "border: 1px solid #991b1b; border-radius: 6px; "
            "padding: 12px 16px; font-size: 12px; font-weight: 600;"
        )
        self.hata_lbl.setVisible(False)
        sag_layout.addWidget(self.hata_lbl)

        self.giris_btn = QPushButton("OTURUM AC")
        self.giris_btn.setFixedHeight(50)
        self.giris_btn.setCursor(Qt.PointingHandCursor)
        self.giris_btn.setStyleSheet(
            "QPushButton { background-color: #3b82f6; color: #ffffff; "
            "border: 1px solid #3b82f6; border-radius: 8px; "
            "font-size: 13px; font-weight: 700; letter-spacing: 2px; } "
            "QPushButton:hover { background-color: #2563eb; "
            "border: 1px solid #2563eb; }"
        )
        self.giris_btn.clicked.connect(self._giris_yap)
        sag_layout.addWidget(self.giris_btn)

        sag_layout.addSpacing(20)

        hr = QFrame()
        hr.setFixedHeight(1)
        hr.setStyleSheet("background-color: #334155;")
        sag_layout.addWidget(hr)
        sag_layout.addSpacing(16)

        ipucu = QLabel(
            "<span style=\"color:#64748b; font-size:11px; font-weight:700; "
            "letter-spacing:1.5px;\">VARSAYILAN ERISIM</span><br><br>"
            "<span style=\"color:#f1f5f9; font-size:13px; font-weight:600;\">"
            "admin <span style='color:#3b82f6;'>·</span> admin123</span>"
        )
        ipucu.setStyleSheet(
            "background-color: #1e293b; "
            "border-left: 3px solid #3b82f6; "
            "padding: 14px 18px; border-radius: 6px;"
        )
        sag_layout.addWidget(ipucu)

        sag_layout.addStretch()

        footer = QLabel("© 2026 DriveShare")
        footer.setStyleSheet(
            "color: #475569; font-size: 10px; letter-spacing: 1px; "
            "background: transparent; border: none;"
        )
        footer.setAlignment(Qt.AlignCenter)
        sag_layout.addWidget(footer)

        ana.addWidget(sag, 1)

    def _etiket(self, metin: str) -> QLabel:
        lbl = QLabel(metin)
        lbl.setStyleSheet(
            "color: #94a3b8; font-size: 10px; font-weight: 700; "
            "letter-spacing: 1.8px; background: transparent; border: none;"
        )
        return lbl

    def _input_stil(self) -> str:
        return (
            "QLineEdit { background-color: #1e293b; "
            "border: 1px solid #334155; border-radius: 8px; "
            "padding: 0 14px; "
            "color: #f1f5f9; font-size: 14px; "
            "selection-background-color: #3b82f6; selection-color: #ffffff; } "
            "QLineEdit:focus { border: 1px solid #3b82f6; "
            "background-color: #1e293b; } "
            "QLineEdit:hover { border: 1px solid #64748b; }"
        )

    def _sifre_goster(self, checked: bool):
        self.sifre_input.setEchoMode(
            QLineEdit.Normal if checked else QLineEdit.Password
        )

    def _hata_goster(self, mesaj: str):
        self.hata_lbl.setText(mesaj.upper())
        self.hata_lbl.setVisible(True)

    def _hata_gizle(self):
        self.hata_lbl.setVisible(False)

    def _giris_yap(self):
        kul = self.kul_input.text().strip()
        sifre = self.sifre_input.text()

        if not kul:
            self._hata_goster("Kullanici adi bos olamaz.")
            self.kul_input.setFocus()
            return
        if not sifre:
            self._hata_goster("Sifre bos olamaz.")
            self.sifre_input.setFocus()
            return

        kullanici = self.auth.dogrula(kul, sifre)
        if kullanici is None:
            self._hata_goster("Kullanici adi veya sifre hatali.")
            self.sifre_input.clear()
            self.sifre_input.setFocus()
            return

        self.dogrulanan_kullanici = kullanici
        self.accept()
