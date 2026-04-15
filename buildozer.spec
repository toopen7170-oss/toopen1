[app]
title = PristonTale
package.name = pristontale
package.domain = org.toopen7170
source.dir = .
source.include_exts = py,png,jpg,ttf,kv
version = 1.0.0
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,android

# 리소스 설정
source.include_patterns = assets/*,images/*
icon.filename = icon.png
presplash.filename = bg.png

# 디스플레이 및 빌드 사양 (S26 울트라 최적화)
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
# NDK 버전 고정으로 빌드 오류 원천 차단
android.ndk = 25b

# 권한 설정
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, READ_MEDIA_IMAGES

[buildozer]
log_level = 2
warn_on_root = 1
