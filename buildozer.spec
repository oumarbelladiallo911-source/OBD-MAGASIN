[app]
title = OBD VISION PHONE FINAL
package.name = obdvisionfinal
package.domain = com.obd.vision
source.dir = .
source.include_exts = py,png,jpg,kv
version = 2.0
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
icon.filename = %(source.dir)s/logo.png
permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license_agreement = True
android.archs = arm64-v8a, armeabi-v7a
p4a.bootstrap = sdl2