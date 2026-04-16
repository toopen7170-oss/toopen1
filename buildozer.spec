[app]

# (정정) 앱 이름 및 패키지 설정
title = PristonTale
package.name = pristontale
package.domain = org.toopen7170

# (정정) 소스코드 위치 및 포함 확장자
source.dir = .
source.include_exts = py,png,jpg,ttf,kv
source.include_patterns = font.ttf, bg.png, icon.png

# (중요) 버전 정보 - 리소스(아이콘 등) 갱신을 위해 1.0.4로 상향
version = 1.0.4

# (중요) 필수 라이브러리 - 이미지 처리를 위한 pillow 포함
requirements = python3,kivy==2.3.0,pillow,android

# (정정) 화면 방향 및 전체화면 설정
orientation = portrait
fullscreen = 1

# (중요) 아이콘 파일 설정 - icon.png가 소스 폴더에 있어야 함
icon.filename = icon.png

# (정정) 안드로이드 아키텍처 설정 (S26 Ultra 최적화)
android.archs = arm64-v8a

# (중요) S26 Ultra 및 최신 안드로이드 보안 정책 적용
android.api = 34
android.minapi = 21
android.ndk = 26b
android.skip_update = False
android.accept_sdk_license = True

# (중요) 사진 촬영 및 이미지 저장 권한 (최신 API 34 규격)
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, READ_MEDIA_IMAGES, READ_MEDIA_VIDEO

# (정정) 빌드 모드 및 로그 레벨
android.release = False
android.debug = True

[buildozer]
# 빌드 과정 상세 출력 (오류 추적용)
log_level = 2
warn_on_root = 1

#-----------------------------------------------------------------------------
# 아래 설정은 기본값을 유지하며 최적화된 상태입니다.
#-----------------------------------------------------------------------------

[p4a]
# Python for Android 설정
# p4a.branch = master
