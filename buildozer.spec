[app]
title = RPG_Final_Manager
package.name = rpg.manager.toopen
package.domain = org.toopen
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# [제1원칙 고정] NDK r26b 및 API 34 설정
android.api = 34
android.minapi = 21
android.ndk = 26b
android.ndk_api = 21
android.archs = arm64-v8a

# [보강 설정] p4a 브랜치 고정으로 컴파일 안정성 확보
p4a.branch = master

# [목록 무결성] 필수 종속성
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,requests,openssl
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET, CAMERA, READ_MEDIA_IMAGES

# [빌드 안정화]
android.skip_update_dependencies = False
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1
