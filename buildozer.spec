[app]

# (보존) 앱 기본 정보
title = PristonTale
package.name = pristontale
package.domain = org.toopen7170

# (교정) 소스 포함 설정 및 버전 상향 (캐시 충돌 방지)
source.dir = .
source.include_exts = py,png,jpg,ttf,kv
source.include_patterns = font.ttf, bg.png, icon.png
version = 1.0.9

# (핵심) 빌드 및 실행 오류 화면 표시를 위한 필수 패키지
requirements = python3,kivy==2.3.0,pillow,android

orientation = portrait
fullscreen = 1
icon.filename = icon.png

# (핵심) GitHub Actions 서버 NDK v27 충돌 해결을 위한 전수 검증 설정
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
android.ndk = 26b
android.ndk_api = 21

# 서버 환경 변수가 Buildozer 설정을 덮어쓰지 못하도록 강제 초기화
android.ndk_path = 
android.sdk_path = 
android.skip_update = False
android.accept_sdk_license = True

# (추가) 안드로이드 최신 권한 (실시간 오류 및 사진 기능 대응)
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO

# 빌드 형식 설정
android.release = False
android.debug = True

[buildozer]
# 빌드 중 발생하는 모든 로그를 상세히 출력 (오류 추적용)
log_level = 2
warn_on_root = 1

[p4a]
# 최신 툴체인 및 하프버즈(harfbuzz) 컴파일 오류 수정 브랜치 사용
p4a.branch = master
