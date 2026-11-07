[app]
title = OBD VISION
package.name = obdvision
package.domain = org.dien.sanou
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0.0
icon.filename = %(source.dir)s/logo.png

# Dépendances requises
requirements = python3,kivy==2.3.0,fpdf,sqlite3

orientation = portrait
fullscreen = 1

# Force l'acceptation automatique des licences dans le fichier de config
android.accept_sdk_license = True

# Permissions de stockage pour les PDF sans internet
android.permissions = android.permission.WRITE_EXTERNAL_STORAGE, android.permission.READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25.2.9519653
android.ndk_api = 21
android.archs = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
