[app]
title = RPG_Master_Manager
package.name = rpg.manager.toopen
package.domain = org.toopen
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# [환경 절연] Android API 34 및 NDK r26b 강제 고정 (v27 침습 차단)
android.api = 34
android.minapi = 21
android.ndk = 26b
android.ndk_api = 21
android.archs = arm64-v8a

# [빌드 안정화] harfbuzz Broken pipe 방지 및 필수 라이브러리
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,requests,openssl
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET, CAMERA, READ_MEDIA_IMAGES

# [환경 절연 시스템] 서버 환경 변수 무시 설정
android.skip_update_dependencies = False
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1
