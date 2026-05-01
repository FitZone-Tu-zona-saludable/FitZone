# fitzone.spec — Configuración para PyInstaller
# Uso: pyinstaller fitzone.spec
# Genera el ejecutable en: dist/FitZone/FitZone.exe

import os
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=[
        # Archivos JSON de datos
        ('data/*.json', 'data'),
        # Assets (logo, imágenes)
        ('src/assets', 'src/assets'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtWidgets',
        'PySide6.QtGui',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'pytest'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FitZone',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # Sin consola negra al ejecutar
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,              # Reemplazar con: icon='src/assets/fitzone.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FitZone',
)
