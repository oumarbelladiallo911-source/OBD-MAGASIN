[app]
title = OBD VISION
package.name = obdvision
package.domain = org.olien.samou
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0.0
icon.filename = logo.png

requirements = python3,kivy==2.3.1

orientation = portrait
fullscreen = 1

android.accept_sdk_license = True
android.permissions = android.permission.WRITE_EXTERNAL_STORAGE, android.permission.READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.archs = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
