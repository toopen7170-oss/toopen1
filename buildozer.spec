[app]

title = PristonTale
package.name = pt1
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 1.0

# 🔥 안정 조합
requirements = python3,kivy,requests,plyer

orientation = portrait
fullscreen = 1

# 🔥 절대 충돌 안나는 고정값
android.api = 34
android.minapi = 24
android.ndk = 25b
android.build_tools_version = 34.0.0
android.archs = arm64-v8a

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# ✅ 아이콘 / 배경
icon.filename = icon.png
presplash.filename = presplash.png

log_level = 2