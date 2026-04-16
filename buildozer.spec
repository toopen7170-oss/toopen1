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
# 배경이미지(bg.png), 폰트(font.ttf), 아이콘(icon.png)을 명시적으로 포함
source.include_patterns = font.ttf, bg.png, icon.png

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# 자가 진단 및 이미지 처리를 위한 pillow 포함
requirements = python3,kivy==2.3.0,pillow,android

# (str) Custom source folders for requirements
# 쓰지 않음

# (str) Presplash of the application
presplash.filename = bg.png

# (str) Icon of the application
icon.filename = icon.png

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
# services = NAME:ENTRYPOINT_PY

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
# 사진 및 미디어 접근을 위한 필수 권한 설정
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA, READ_MEDIA_IMAGES

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
# android.ndk = 25b

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
# android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
# android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
# android.ant_path =

# (list) Android architectures to build for (S26 Ultra 최적화)
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (default False)
android.allow_backup = True

# (str) The Android margin to use for the presplash
# android.presplash_lottie = 

# (list) The Android styles to apply to the activities
# android.style = 

#
# Python for android (p4a) specific
#

# (str) python-for-android branch to use, defaults to master
# p4a.branch = master


#
# Buildozer section
#

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifacts, add %s for the name of the package
# build_dir = ./.buildozer

# (str) Path to bin directory
# bin_dir = ./bin
