[app]
title = Nexus IPTV
package.name = nexusiptv
package.domain = org.adil1821
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# ICI : On force l'utilisation stricte de python3==3.10.11
requirements = python3,kivy,urllib3,openssl

orientation = portrait
fullscreen = 1
android.permissions = INTERNET

# Paramètres de compatibilité Android
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.private_storage = True
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
