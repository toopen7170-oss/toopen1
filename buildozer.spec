[app]

# (str) Title of your application
title = PristonTale

# (str) Package name
package.name = pristontale

# (str) Package domain (needed for android packaging)
package.domain = org.toopen7170

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,ttf,kv

# (list) List of inclusions using pattern matching
# 배경이미지(bg.png), 폰트(font.ttf), 아이콘(icon.png) 포함 확인 완료
source.include_patterns = font.ttf, bg.png, icon.png

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# 사진 및 자가진단 시스템을 위한 pillow와 android 모듈 포함
requirements = python3,kivy==2.3.0,pillow,android

# (str) Presplash of the application
# 시작 화면 배경 설정
presplash.filename = bg.png

# (str) Icon of the application
icon.filename = icon.png

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
# 사진 접근, 외부 저장소 읽기/쓰기, 카메라 권한 완벽 반영
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, READ_MEDIA_IMAGES

# (int) Target Android API (안드로이드 13 대응)
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (list) Android architectures to build for (S26 Ultra arm64 최적화)
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (default False)
android.allow_backup = True

#
# Buildozer section
#

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
