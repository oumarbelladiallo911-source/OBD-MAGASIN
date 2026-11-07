[app]

# (str) Title of your application
title = DIEN SANOU

# (str) Package name (en minuscules, sans espaces ni caractères spéciaux)
package.name = diensanou

# (str) Package domain (needed for android packaging)
package.domain = org.diensanou

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (on s'assure d'inclure les fichiers .png)
source.include_exts = py,png,jpg,kv,atlas,json,txt

# (str) Icon of the application (le fichier à la racine de ton projet)
icon.filename = logo.png

# IMPORTANT : Uniquement Kivy et Python3 pour le mode 100% hors-ligne
requirements = python3,kivy

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# ----------------------------------
# Android specific profiles
# ----------------------------------

# (bool) Indicate if the application should be fullscreen or not
fullname = DIEN SANOU

# (list) Permissions. Laissée vide pour garantir le fonctionnement sans internet
android.permissions = 

# (int) Target Android API
android.api = 34

# (int) Minimum API required (Android 8.0+)
android.minapi = 26

# (bool) Use copy-libs instead of variable encryption
android.copy_libs = 1

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk
