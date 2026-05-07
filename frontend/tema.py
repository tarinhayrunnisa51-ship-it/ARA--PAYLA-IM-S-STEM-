"""
Modern Dark Automotive Tema - Araç paylaşım sistemi için koyu modern tema.
Koyu lacivert tonları, elektrik mavisi accent, yumuşak köşeler.
"""

RENKLER = {
    # Arkaplan katmanları
    "bg": "#0f172a",              # ana arkaplan (koyu lacivert)
    "bg_card": "#1e293b",         # kart / panel
    "bg_input": "#0f172a",        # input arkaplan
    "bg_hover": "#334155",        # hover durumu
    "bg_sidebar": "#1e293b",      # sidebar

    # Metin
    "text": "#f1f5f9",            # ana metin (açık beyaz)
    "text_sec": "#94a3b8",        # ikincil metin
    "text_muted": "#64748b",      # soluk metin
    "text_faint": "#475569",      # disabled

    # Çizgiler
    "border": "#334155",          # genel kenarlık
    "border_light": "#1e293b",    # ince ayraç
    "border_focus": "#3b82f6",    # focus kenarlık

    # Accent
    "accent": "#3b82f6",          # elektrik mavisi
    "accent_hover": "#2563eb",    # hover
    "accent_pale": "#1e3a5f",     # rozet bg
    "accent_glow": "#3b82f620",   # glow efekti

    # Durum
    "success": "#22c55e",
    "success_bg": "#14532d",
    "warning": "#f59e0b",
    "warning_bg": "#713f12",
    "danger": "#ef4444",
    "danger_bg": "#7f1d1d",

    # Tablo
    "table_header": "#0f172a",
    "table_zebra": "#1a2744",
    "table_hover": "#253552",
}


ANA_STIL = f"""
/* GENEL ============================================================ */
QWidget {{
    background-color: {RENKLER['bg']};
    color: {RENKLER['text']};
    font-family: "Segoe UI", "Inter", "Helvetica Neue", sans-serif;
    font-size: 13px;
}}

QMainWindow {{
    background-color: {RENKLER['bg']};
}}

QToolTip {{
    background-color: {RENKLER['bg_card']};
    color: {RENKLER['text']};
    border: 1px solid {RENKLER['border']};
    padding: 7px 12px;
    border-radius: 6px;
    font-size: 11px;
}}

/* SIDEBAR ========================================================== */
#Sidebar {{
    background-color: {RENKLER['bg_sidebar']};
    border-right: 1px solid {RENKLER['border']};
}}

#MastheadBaslik {{
    color: {RENKLER['text']};
    background: transparent;
    border: none;
    font-weight: 800;
    font-size: 20px;
    letter-spacing: 0.5px;
}}

#MastheadAlt {{
    color: {RENKLER['text_muted']};
    background: transparent;
    border: none;
    font-size: 9px;
    letter-spacing: 2px;
    font-weight: 600;
    text-transform: uppercase;
}}

#MenuBaslik {{
    color: {RENKLER['text_muted']};
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    background: transparent;
    border: none;
}}

QPushButton#MenuButon {{
    background-color: transparent;
    color: {RENKLER['text_sec']};
    text-align: left;
    padding-left: 24px;
    padding-right: 24px;
    border: none;
    border-left: 3px solid transparent;
    border-radius: 0;
    font-size: 13px;
    font-weight: 500;
}}

QPushButton#MenuButon:hover {{
    background-color: {RENKLER['bg_hover']};
    color: {RENKLER['text']};
}}

QPushButton#MenuButon:checked {{
    background-color: {RENKLER['accent_pale']};
    color: {RENKLER['accent']};
    font-weight: 700;
    border-left: 3px solid {RENKLER['accent']};
}}

#KullaniciKart {{
    background-color: {RENKLER['bg']};
    border: 1px solid {RENKLER['border']};
    border-radius: 8px;
}}

#KullaniciKart QLabel {{
    background: transparent;
    border: none;
}}

#KullaniciAd {{
    color: {RENKLER['text']};
    font-weight: 700;
    font-size: 12px;
}}

#KullaniciDurum {{
    color: {RENKLER['text_muted']};
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}}

#PlanRozet {{
    background-color: {RENKLER['accent']};
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 3px 9px;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1px;
    min-width: 50px;
}}

/* SAYFA BAŞLIKLARI ================================================ */
#SayfaBaslik {{
    color: {RENKLER['text']};
    background: transparent;
    border: none;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -0.5px;
}}

#SayfaAltBaslik {{
    color: {RENKLER['text_sec']};
    background: transparent;
    border: none;
    font-size: 13px;
    font-weight: 400;
}}

/* KARTLAR ========================================================= */
#Kart {{
    background-color: {RENKLER['bg_card']};
    border: 1px solid {RENKLER['border']};
    border-radius: 10px;
}}

#Kart QLabel {{
    background: transparent;
    border: none;
}}

#KartBaslik {{
    color: {RENKLER['text']};
    font-size: 16px;
    font-weight: 700;
    background: transparent;
    border: none;
}}

#KartAltBaslik {{
    color: {RENKLER['text_sec']};
    font-size: 12px;
    background: transparent;
    border: none;
}}

/* BUTONLAR ======================================================== */
QPushButton {{
    background-color: {RENKLER['bg_card']};
    color: {RENKLER['text']};
    border: 1px solid {RENKLER['border']};
    padding-left: 18px;
    padding-right: 18px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
}}

QPushButton:hover {{
    background-color: {RENKLER['bg_hover']};
    border: 1px solid {RENKLER['text_muted']};
}}

QPushButton:disabled {{
    background-color: {RENKLER['bg']};
    color: {RENKLER['text_faint']};
    border: 1px solid {RENKLER['border_light']};
}}

QPushButton#PrimaryButon {{
    background-color: {RENKLER['accent']};
    color: #ffffff;
    border: 1px solid {RENKLER['accent']};
}}

QPushButton#PrimaryButon:hover {{
    background-color: {RENKLER['accent_hover']};
    border: 1px solid {RENKLER['accent_hover']};
}}

QPushButton#HayaletButon {{
    background-color: transparent;
    color: {RENKLER['text_sec']};
    border: 1px solid {RENKLER['border']};
}}

QPushButton#HayaletButon:hover {{
    background-color: {RENKLER['bg_hover']};
    color: {RENKLER['text']};
    border: 1px solid {RENKLER['text_muted']};
}}

QPushButton#TehlikeButon {{
    background-color: transparent;
    color: {RENKLER['danger']};
    border: 1px solid {RENKLER['border']};
}}

QPushButton#TehlikeButon:hover {{
    background-color: {RENKLER['danger']};
    color: #ffffff;
    border: 1px solid {RENKLER['danger']};
}}

QPushButton#KucukIkincilButon {{
    background-color: {RENKLER['bg']};
    color: {RENKLER['text']};
    border: 1px solid {RENKLER['border']};
    padding-left: 12px;
    padding-right: 12px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.5px;
    border-radius: 5px;
}}

QPushButton#KucukIkincilButon:hover {{
    background-color: {RENKLER['accent']};
    color: #ffffff;
    border: 1px solid {RENKLER['accent']};
}}

QPushButton#KucukTehlikeButon {{
    background-color: transparent;
    color: {RENKLER['danger']};
    border: 1px solid {RENKLER['border']};
    padding-left: 12px;
    padding-right: 12px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.5px;
    border-radius: 5px;
}}

QPushButton#KucukTehlikeButon:hover {{
    background-color: {RENKLER['danger']};
    color: #ffffff;
    border: 1px solid {RENKLER['danger']};
}}

/* FORM ALANLARI =================================================== */
QLineEdit, QSpinBox, QDateTimeEdit, QComboBox, QTextEdit {{
    background-color: {RENKLER['bg_input']};
    border: 1px solid {RENKLER['border']};
    border-radius: 6px;
    padding-left: 12px;
    padding-right: 12px;
    color: {RENKLER['text']};
    selection-background-color: {RENKLER['accent']};
    selection-color: #ffffff;
    font-size: 13px;
}}

QLineEdit:focus, QSpinBox:focus, QDateTimeEdit:focus,
QComboBox:focus, QTextEdit:focus {{
    border: 1px solid {RENKLER['accent']};
    background-color: {RENKLER['bg_card']};
}}

QLineEdit:hover, QSpinBox:hover, QDateTimeEdit:hover,
QComboBox:hover, QTextEdit:hover {{
    border: 1px solid {RENKLER['text_muted']};
}}

#AramaInput {{
    background-color: {RENKLER['bg_input']};
    border: 1px solid {RENKLER['border']};
    padding-left: 16px;
    padding-right: 16px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
}}

#AramaInput:focus {{
    border: 1px solid {RENKLER['accent']};
}}

QSpinBox::up-button, QSpinBox::down-button,
QDateTimeEdit::up-button, QDateTimeEdit::down-button {{
    background-color: transparent;
    border: none;
    width: 16px;
}}

QComboBox::drop-down {{
    border: none;
    width: 28px;
    background: transparent;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {RENKLER['text_sec']};
    margin-right: 12px;
    width: 0;
    height: 0;
}}

QComboBox QAbstractItemView {{
    background-color: {RENKLER['bg_card']};
    border: 1px solid {RENKLER['border']};
    border-radius: 6px;
    selection-background-color: {RENKLER['accent']};
    selection-color: #ffffff;
    color: {RENKLER['text']};
    padding: 4px;
    outline: 0;
}}

QComboBox QAbstractItemView::item {{
    padding: 8px 10px;
    border-radius: 4px;
    min-height: 22px;
}}

QComboBox QAbstractItemView::item:hover {{
    background-color: {RENKLER['bg_hover']};
}}

QLabel#FormEtiket {{
    color: {RENKLER['text_sec']};
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    background: transparent;
    border: none;
}}

/* TABLOLAR ======================================================== */
QTableWidget {{
    background-color: {RENKLER['bg_card']};
    border: 1px solid {RENKLER['border']};
    border-radius: 10px;
    gridline-color: transparent;
    color: {RENKLER['text']};
    selection-background-color: transparent;
    outline: 0;
    alternate-background-color: {RENKLER['table_zebra']};
}}

QTableWidget::item {{
    padding-left: 8px;
    padding-right: 8px;
    border: none;
    border-bottom: 1px solid {RENKLER['border']};
    background-color: transparent;
    color: {RENKLER['text']};
}}

QTableWidget::item:selected {{
    background-color: {RENKLER['accent_pale']};
    color: {RENKLER['text']};
}}

QTableWidget::item:hover {{
    background-color: {RENKLER['table_hover']};
}}

QHeaderView::section {{
    background-color: {RENKLER['table_header']};
    color: {RENKLER['text_muted']};
    padding-top: 12px;
    padding-bottom: 12px;
    padding-left: 14px;
    padding-right: 14px;
    border: none;
    border-bottom: 1px solid {RENKLER['border']};
    font-weight: 700;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}}

QTableCornerButton::section {{
    background-color: {RENKLER['table_header']};
    border: none;
}}

/* SCROLLBAR ======================================================= */
QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    border: none;
    margin: 4px 2px 4px 2px;
}}

QScrollBar::handle:vertical {{
    background: {RENKLER['text_faint']};
    border-radius: 4px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {RENKLER['text_muted']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
    background: none;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 8px;
    border: none;
    margin: 2px 4px 2px 4px;
}}

QScrollBar::handle:horizontal {{
    background: {RENKLER['text_faint']};
    border-radius: 4px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {RENKLER['text_muted']};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
    background: none;
}}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}

/* DİYALOG ========================================================= */
QDialog {{
    background-color: {RENKLER['bg']};
}}

QMessageBox {{
    background-color: {RENKLER['bg_card']};
}}

QMessageBox QLabel {{
    color: {RENKLER['text']};
    font-size: 13px;
    background: transparent;
    border: none;
}}

QMessageBox QPushButton {{
    min-width: 90px;
}}

/* DİĞER =========================================================== */
QFrame#Ayirici {{
    background-color: {RENKLER['border']};
    max-height: 1px;
    min-height: 1px;
    border: none;
}}

QFrame#AyiriciInce {{
    background-color: {RENKLER['border']};
    max-height: 1px;
    min-height: 1px;
    border: none;
}}
"""
