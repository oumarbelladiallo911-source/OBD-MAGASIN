[app]
title = OBD VISION
package.name = obdvision
package.domain = org.dien.sanou
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0.0
icon.filename = %(source.dir)s/logo.png
# Les dépendances indispensables (Kivy et FPDF pour tes impressions)
requirements = python3,kivy==2.3.0,fpdf

orientation = portrait
fullscreen = 1

# Permissions pour sauvegarder et ouvrir les fichiers PDF sans internet
android.permissions = android.permission.WRITE_EXTERNAL_STORAGE, android.permission.READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
