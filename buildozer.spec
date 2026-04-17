[app]
title = RPG_Final_Manager
package.name = rpg.manager.toopen
package.domain = org.toopen
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# [제1원칙 고정] NDK r26b 및 API 34
android.api = 34
android.minapi = 21
android.ndk = 26b
android.ndk_api = 21
android.archs = arm64-v8a

# [빌드 안정화] p4a 브랜치 고정 및 불필요한 캐시 방지
p4a.branch = master
android.skip_update_dependencies = False
android.copy_libs = 1

# [목록 무결성]
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,requests,openssl
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET, CAMERA, READ_MEDIA_IMAGES

[buildozer]
log_level = 2
warn_on_root = 1
