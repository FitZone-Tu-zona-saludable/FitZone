"""
theme.py
========
Sistema de diseño centralizado de FitZone (estilo "Moderno verde/oscuro").

Toda vista de Alex debe importar desde aquí los colores, tipografías y la
hoja de estilos QSS global. Esto garantiza coherencia visual y facilita
mantener la marca FitZone si en el futuro cambia algún color.

Uso:
    from frontend.resources.theme import apply_theme, COLORS

    app = QApplication(sys.argv)
    apply_theme(app)

Autor: Alex - Interfaz visual e integración (Sprint 2).
"""

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

# ---------------------------------------------------------------------------
# Paleta de marca FitZone
# ---------------------------------------------------------------------------
COLORS = {
    "bg":            "#0F1A17",   # Fondo principal (verde casi negro)
    "bg_alt":        "#152521",   # Paneles / sidebar
    "surface":       "#1C312B",   # Tarjetas
    "surface_hi":    "#244039",   # Tarjeta hover / inputs
    "border":        "#2E4A42",
    "primary":       "#21C07A",   # Verde fitness vibrante
    "primary_hover": "#1AA968",
    "primary_dim":   "#0E6B45",
    "text":          "#E8F1ED",
    "text_muted":    "#9DB3AB",
    "danger":        "#E5484D",
    "warning":       "#F5A524",
    "info":          "#3B82F6",
    "success":       "#21C07A",
}

FONT_FAMILY = "Segoe UI, Inter, Roboto, sans-serif"


# ---------------------------------------------------------------------------
# Hoja de estilos global (QSS)
# ---------------------------------------------------------------------------
def _qss() -> str:
    c = COLORS
    return f"""
    QWidget {{
        background-color: {c['bg']};
        color: {c['text']};
        font-family: {FONT_FAMILY};
        font-size: 14px;
    }}

    /* ----- Tipografía utilitaria ----- */
    QLabel#H1     {{ font-size: 26px; font-weight: 700; color: {c['text']}; }}
    QLabel#H2     {{ font-size: 20px; font-weight: 600; color: {c['text']}; }}
    QLabel#Muted  {{ color: {c['text_muted']}; }}
    QLabel#Brand  {{ font-size: 22px; font-weight: 800; color: {c['primary']};
                     letter-spacing: 2px; }}

    /* ----- Tarjeta ----- */
    QFrame#Card {{
        background-color: {c['surface']};
        border: 1px solid {c['border']};
        border-radius: 14px;
    }}
    QFrame#Sidebar {{
        background-color: {c['bg_alt']};
        border-right: 1px solid {c['border']};
    }}

    /* ----- Inputs ----- */
    QLineEdit, QComboBox, QDateEdit, QTimeEdit, QSpinBox,
    QDoubleSpinBox, QTextEdit, QPlainTextEdit {{
        background-color: {c['surface_hi']};
        border: 1px solid {c['border']};
        border-radius: 8px;
        padding: 8px 10px;
        color: {c['text']};
        selection-background-color: {c['primary']};
    }}
    QLineEdit:focus, QComboBox:focus, QDateEdit:focus,
    QTimeEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
        border: 1px solid {c['primary']};
    }}
    QComboBox::drop-down {{ border: none; width: 22px; }}

    /* ----- Botones ----- */
    QPushButton {{
        background-color: {c['surface_hi']};
        color: {c['text']};
        border: 1px solid {c['border']};
        padding: 9px 16px;
        border-radius: 8px;
        font-weight: 600;
    }}
    QPushButton:hover  {{ background-color: {c['surface']}; border-color: {c['primary']}; }}
    QPushButton:pressed{{ background-color: {c['bg_alt']}; }}

    QPushButton#Primary {{
        background-color: {c['primary']};
        color: #062017;
        border: none;
    }}
    QPushButton#Primary:hover  {{ background-color: {c['primary_hover']}; }}
    QPushButton#Primary:pressed{{ background-color: {c['primary_dim']}; color: white; }}

    QPushButton#Danger {{
        background-color: {c['danger']}; color: white; border: none;
    }}

    QPushButton#NavItem {{
        text-align: left;
        padding: 11px 16px;
        background: transparent;
        border: none;
        border-left: 3px solid transparent;
        border-radius: 0px;
        font-weight: 500;
        color: {c['text_muted']};
    }}
    QPushButton#NavItem:hover  {{ color: {c['text']}; background: {c['surface']}; }}
    QPushButton#NavItem:checked{{
        color: {c['primary']};
        background: {c['surface']};
        border-left: 3px solid {c['primary']};
    }}

    /* ----- Tablas ----- */
    QTableWidget, QTableView {{
        background-color: {c['surface']};
        border: 1px solid {c['border']};
        border-radius: 10px;
        gridline-color: {c['border']};
        selection-background-color: {c['primary_dim']};
    }}
    QHeaderView::section {{
        background-color: {c['bg_alt']};
        color: {c['text_muted']};
        padding: 8px;
        border: none;
        border-bottom: 1px solid {c['border']};
        font-weight: 600;
    }}

    /* ----- Alertas ----- */
    QFrame#AlertSuccess {{
        background-color: rgba(33,192,122,0.12);
        border: 1px solid {c['primary']};
        border-radius: 10px;
    }}
    QFrame#AlertWarning {{
        background-color: rgba(245,165,36,0.12);
        border: 1px solid {c['warning']};
        border-radius: 10px;
    }}
    QFrame#AlertDanger {{
        background-color: rgba(229,72,77,0.12);
        border: 1px solid {c['danger']};
        border-radius: 10px;
    }}

    QScrollBar:vertical {{
        background: {c['bg']}; width: 10px; margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {c['surface_hi']}; border-radius: 5px; min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{ background: {c['primary_dim']}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    """


def apply_theme(app: QApplication) -> None:
    """Aplica la hoja de estilos global y la tipografía base a la app."""
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(_qss())
