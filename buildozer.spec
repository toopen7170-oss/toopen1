[app]
title = PristonTale
package.name = pristontale
package.domain = org.toopen7170
source.dir = .
source.include_exts = py,png,jpg,ttf,kv
version = 1.0.0
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,android

# 리소스 경로 및 아이콘 설정 고정
source.include_patterns = assets/*,images/*
icon.filename = icon.png
presplash.filename = bg.png

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 34.0.0
android.accept_sdk_license = True

# 갤러리 연동 및 폴더 접근 권한 업데이트 완료
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, READ_MEDIA_IMAGES

[buildozer]
log_level = 2
warn_on_root = 1
