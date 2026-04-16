[app]
title = PristonTale
package.name = pristontale
package.domain = org.toopen7170
source.dir = .
source.include_exts = py,png,jpg,ttf,kv
source.include_patterns = font.ttf, bg.png, icon.png
version = 1.0.2
requirements = python3,kivy==2.3.0,pillow,android
orientation = portrait
fullscreen = 1
icon.filename = icon.png
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, READ_MEDIA_IMAGES
[buildozer]
log_level = 2
warn_on_root = 1
