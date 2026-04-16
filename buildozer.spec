[app]

# (핵심) 앱 식별 정보
title = PristonTale
package.name = pristontale
package.domain = org.toopen7170

# (핵심) 리소스 포함 (font, bg, icon 필수 포함)
source.dir = .
source.include_exts = py,png,jpg,ttf,kv
source.include_patterns = font.ttf, bg.png, icon.png

# (중요) 버전 - 1.0.5 (빌드 실패 후 갱신용)
version = 1.0.5

# (중요) 필수 라이브러리
requirements = python3,kivy==2.3.0,pillow,android

# (설정) 화면 방향
orientation = portrait
fullscreen = 1

# (중요) 아이콘 파일
icon.filename = icon.png

# (설정) 아키텍처 (S26 Ultra 최적화)
android.archs = arm64-v8a

# (핵심) 안드로이드 API 설정
android.api = 34
android.minapi = 21
# (중정정) NDK 버전을 명확히 명시하여 Broken pipe 방지
android.ndk = 26b
android.ndk_api = 21

# (중요) GitHub Actions 환경 최적화 설정
android.skip_update = False
android.accept_sdk_license = True
android.logcat_filters = *:S python:D

# (핵심) 권한 설정 (안드로이드 14 최신 규격)
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO

# (설정) 빌드 모드
android.release = False
android.debug = True

[buildozer]
# 빌드 로그 상세도 (오류 추적용)
log_level = 2
warn_on_root = 1

[p4a]
# Python for Android 빌드 옵션
# p4a.branch = master
