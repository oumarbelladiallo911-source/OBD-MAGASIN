[app]
title = DIEN SANOU
package.name = diensanou
package.domain = org.diensanou
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0
requirements = python3,kivy==2.3.1
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True
android.archs = arm64-v8a,armeabi-v7a
android.allow_backup = True
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
p4a.branch = v2024.01.21
p4a.bootstrap = sdl2
[buildozer]
log_level = 2
warn_on_root = 1
