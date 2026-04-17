[app]
title = PristonTale
package.name = pristontale
package.domain = org.toopen7170
source.dir = .
source.include_exts = py,png,jpg,ttf,kv
source.include_patterns = font.ttf, bg.png, icon.png
version = 1.1.2

# 빌드 및 실행 오류 화면 표시와 권한 설정을 위한 패키지
requirements = python3,kivy==2.3.0,pillow,android

orientation = portrait
fullscreen = 1
icon.filename = icon.png

# NDK v27 충돌 방지 및 r26b 고정 설정
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
android.ndk = 26b
android.ndk_api = 21
android.ndk_path = 
android.sdk_path = 

# 안드로이드 14(API 34) 사진/카메라 권한 전수 검증 적용
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, READ_MEDIA_IMAGES

android.release = False
android.debug = True

[buildozer]
log_level = 2
warn_on_root = 1

[p4a]
p4a.branch = master
