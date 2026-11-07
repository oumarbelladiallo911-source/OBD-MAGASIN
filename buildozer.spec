[app]

# (str) Title of your application
title = DIEN SANOU

# (str) Package name
package.name = diensanou

# (str) Package domain
package.domain = org.diensanou

# (str) Source code where the main.py lives
source.dir = .

# OBLIGATOIRE : Sans ça, Buildozer plante dès la seconde 0
version = 0.1

# (list) Source files to include (bien inclure le logo)
source.include_exts = py,png,jpg,kv,atlas,json,txt

# (str) Icon of the application
icon.filename = logo.png

# Version pure sans internet
requirements = python3,kivy

# (str) Supported orientations
orientation = portrait

# ----------------------------------
# Android specific profiles
# ----------------------------------

fullname = DIEN SANOU

# Mode hors-ligne strict (Pas de permission Internet demandée)
android.permissions = 

# API cible stable pour GitHub Actions
android.api = 33
android.minapi = 21

# Paramètre technique pour éviter les erreurs de compilation de libs externes
android.copy_libs = 1
android.debug_artifact = apk
