[app]
# (보존) 앱 기본 정보
title = PristonTale
package.name = pristontale
package.domain = org.toopen7170

# (수정) 리소스 포함 및 버전 상향 (harfbuzz 오류 해결용)
source.dir = .
source.include_exts = py,png,jpg,ttf,kv
source.include_patterns = font.ttf, bg.png, icon.png
version = 1.0.7

# (추가) 필수 요구사항
requirements = python3,kivy==2.3.0,pillow,android

orientation = portrait
fullscreen = 1
icon.filename = icon.png

# (핵심) GitHub Actions 컴파일러 충돌(Broken pipe) 방지 설정
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
android.ndk = 26b
android.ndk_api = 21

# 서버 환경 변수 충돌 차단
android.ndk_path = 
android.sdk_path = 
android.skip_update = False
android.accept_sdk_license = True

# (핵심) 최신 안드로이드 권한 (사진 업로드 대응)
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO

android.release = False
android.debug = True

[buildozer]
log_level = 2
warn_on_root = 1

[p4a]
# 최신 툴체인 안정성 확보
p4a.branch = master
