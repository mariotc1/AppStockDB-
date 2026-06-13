# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec para AppStockDB — modo --onedir
#
# La API corre en Docker (local o cloud). El bundle solo incluye el frontend.
# Antes de empaquetar, actualiza .env con la URL de producción:
#   API_BASE_URL=https://tu-api-en-produccion.com
#
# Uso:
#   pyinstaller launcher.spec
#
# Resultado: dist/AppStockDB/  ← comprimir en zip y distribuir

import os

block_cipher = None

PROJECT_ROOT = os.path.abspath('.')
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')

added_files = [
    # Recursos visuales
    (os.path.join(PROJECT_ROOT, 'images'),                          'images'),
    (os.path.join(FRONTEND_DIR, 'themes', 'dark.qss'),  os.path.join('frontend', 'themes')),
    (os.path.join(FRONTEND_DIR, 'themes', 'light.qss'), os.path.join('frontend', 'themes')),
    # Config de la app (preferencia de tema)
    (os.path.join(PROJECT_ROOT, 'config'),                          'config'),
    # URL de la API de producción
    (os.path.join(PROJECT_ROOT, '.env'),                            '.'),
    # Vídeos de ayuda
    (os.path.join(PROJECT_ROOT, 'videos'),                          'videos'),
]

# Solo necesitamos el frontend — Flask/MySQL corren en el servidor
hidden_imports = [
    'PyQt5',
    'PyQt5.QtWidgets',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtMultimedia',
    'PyQt5.QtMultimediaWidgets',
    'PyQt5.sip',
    'requests',
    'dotenv',
    'email.mime.text',
    'email.mime.multipart',
    'email.mime.image',
    'smtplib',
]

a = Analysis(
    ['launcher.py'],
    pathex=[PROJECT_ROOT, FRONTEND_DIR],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'flask', 'werkzeug', 'mysql', 'bcrypt', 'pandas',
        'sphinx', 'docutils', 'alabaster', 'babel', 'pyinstaller',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AppStockDB',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AppStockDB',
)
