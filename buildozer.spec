[app]

# (1) 앱 기본 정보
title = PristonTale
package.name = pristontale
package.domain = org.toopen7170

# (2) 소스 및 리소스 포함 (폰트 깨짐 방지 핵심)
source.dir = .
source.include_exts = py,png,jpg,ttf,kv
source.include_patterns = font.ttf, bg.png, icon.png, assets/*
version = 1.0.5

# (3) 필수 요구 라이브러리
requirements = python3,kivy==2.3.0,pillow,android

# (4) 아이콘 및 로딩 화면
icon.filename = icon.png
presplash.filename = bg.png

# (5) 화면 설정 (S26 울트라 최적화)
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a

# (6) 안드로이드 API 레벨 (최신 API 34 대응)
android.api = 34
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 34.0.0
android.accept_sdk_license = True

# (7) 권한 설정 (사진 업로드 및 저장 무결점 활성화)
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, READ_MEDIA_IMAGES

# (8) 빌드 최적화
android.release_artifact = aab
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1
