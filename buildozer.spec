[app]
title = RPG_Final_Manager
package.name = rpg.manager.toopen
package.domain = org.toopen
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# [제1원칙 고정] NDK r26b 및 Android API 34 호환 설정
android.api = 34
android.minapi = 21
android.ndk = 26b
android.ndk_api = 21
android.archs = arm64-v8a

# [빌드 무결성 보강]
p4a.branch = master
android.skip_update_dependencies = False
android.copy_libs = 1

# [데이터 및 권한]
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,requests,openssl
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET, CAMERA, READ_MEDIA_IMAGES

[buildozer]
log_level = 2
warn_on_root = 1
