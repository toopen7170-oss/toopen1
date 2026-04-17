[app]
# (보존) 앱 기본 정보
title = PristonTale
package.name = pristontale
package.domain = org.toopen7170

# (수정) 리소스 포함 및 버전업 (Broken pipe 해결용)
source.dir = .
source.include_exts = py,png,jpg,ttf,kv
source.include_patterns = font.ttf, bg.png, icon.png
version = 1.0.6

# (추가) 필수 요구사항
requirements = python3,kivy==2.3.0,pillow,android

orientation = portrait
fullscreen = 1
icon.filename = icon.png

# (수정) GitHub Actions 빌드 환경 최적화 (NDK r26b 고정)
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
android.ndk = 26b
android.ndk_api = 21
android.ndk_path = 
android.sdk_path = 

android.skip_update = False
android.accept_sdk_license = True

# (추가) 최신 안드로이드 권한 설정
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO

android.release = False
android.debug = True

[buildozer]
log_level = 2
warn_on_root = 1

[p4a]
