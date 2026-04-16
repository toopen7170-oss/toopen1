[app]

# (핵심) 앱 식별 정보 - 기존 토대 유지
title = PristonTale
package.name = pristontale
package.domain = org.toopen7170

# (핵심) 리소스 포함 설정 (py, png, jpg, ttf, kv 파일 전수 포함)
source.dir = .
source.include_exts = py,png,jpg,ttf,kv
source.include_patterns = font.ttf, bg.png, icon.png

# (중요) 버전 - 1.0.5 (Broken pipe 오류 해결 및 리소스 강제 갱신용)
version = 1.0.5

# (중요) 필수 라이브러리 (이미지 처리를 위한 pillow 및 android 라이브러리 포함)
requirements = python3,kivy==2.3.0,pillow,android

# (설정) 화면 모드 및 방향
orientation = portrait
fullscreen = 1

# (중요) 아이콘 파일명 지정
icon.filename = icon.png

# (설정) 안드로이드 아키텍처 (S26 Ultra 및 최신 기기 최적화)
android.archs = arm64-v8a

# (핵심) 안드로이드 API 및 SDK 설정 (GitHub Actions 환경 최적화)
android.api = 34
android.minapi = 21
android.ndk = 26b
android.ndk_api = 21
android.skip_update = False
android.accept_sdk_license = True

# (핵심) 최신 안드로이드 보안 정책 권한 (사진 업로드 및 카메라 기능 대응)
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO

# (설정) 빌드 모드 및 로그 상세도
android.release = False
android.debug = True

[buildozer]
# 빌드 과정 상세 출력 (오류 발생 시 정밀 추적용)
log_level = 2
warn_on_root = 1

#-----------------------------------------------------------------------------
# 아래 설정은 기본값을 유지하며 최적화된 상태입니다.
#-----------------------------------------------------------------------------

[p4a]
# Python for Android 설정
# p4a.branch = master
