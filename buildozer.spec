[app]
title = DIEN SANOU
package.name = obdvisionfinal
package.domain = com.obd.vision
source.dir = .
source.main = main.py
version = 2.0
requirements = python3,kivy==2.3.0
icon.filename = %(source.dir)s/logo.png
orientation = portrait
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreements = True

[buildozer]
log_level = 2
warn_on_root = 1
